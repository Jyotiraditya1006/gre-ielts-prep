import secrets
import re
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from backend.database import get_db
from backend import models, schemas
from backend.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


def normalize_phone(phone: str) -> str:
    """Normalize phone number to digits with leading plus if international."""
    if not phone:
        return ""
    cleaned = re.sub(r"[^\d+]", "", phone.strip())
    # If 10 digits without country code, default to +91
    if re.match(r"^\d{10}$", cleaned):
        return "+91" + cleaned
    if not cleaned.startswith("+") and len(cleaned) >= 10:
        return "+" + cleaned
    return cleaned


@router.post("/register", response_model=schemas.Token)
async def register(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    clean_phone = normalize_phone(user_data.phone_number) if user_data.phone_number else None
    
    # Check if email, username, or phone already exists
    conds = [
        models.User.email == user_data.email,
        models.User.username == user_data.username
    ]
    if clean_phone:
        conds.append(models.User.phone_number == clean_phone)
        
    result = await db.execute(select(models.User).where(or_(*conds)))
    existing = result.scalar_one_or_none()
    if existing:
        if clean_phone and existing.phone_number == clean_phone:
            raise HTTPException(status_code=400, detail="Mobile phone number is already registered")
        if existing.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email address is already registered")
        raise HTTPException(status_code=400, detail="Username is already taken")
    
    user = models.User(
        email=user_data.email,
        username=user_data.username,
        phone_number=clean_phone,
        hashed_password=hash_password(user_data.password),
        target_exam=user_data.target_exam or "both",
        target_score=user_data.target_score
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    token = create_access_token({"sub": str(user.id)})
    return schemas.Token(
        access_token=token,
        token_type="bearer",
        user=schemas.UserOut.model_validate(user)
    )


@router.post("/login", response_model=schemas.Token)
async def login(credentials: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    identifier = credentials.email.strip()
    norm_phone = normalize_phone(identifier)
    
    # Check by email, username, or phone
    result = await db.execute(select(models.User).where(
        or_(
            models.User.email == identifier,
            models.User.username == identifier,
            models.User.phone_number == norm_phone
        )
    ))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email, phone number, or password"
        )
    
    token = create_access_token({"sub": str(user.id)})
    return schemas.Token(
        access_token=token,
        token_type="bearer",
        user=schemas.UserOut.model_validate(user)
    )


@router.post("/send-otp", response_model=schemas.OTPResponse)
async def send_otp(req: schemas.SendOTPRequest, db: AsyncSession = Depends(get_db)):
    """
    Sends a 6-digit verification OTP to the user's mobile phone number.
    Supports both 'login' and 'forgot_password' flows.
    """
    phone = normalize_phone(req.phone_number)
    if not phone or len(phone) < 10:
        raise HTTPException(status_code=400, detail="Please enter a valid 10-digit mobile phone number")
        
    # If forgot password, ensure user actually exists
    if req.purpose == "forgot_password":
        res = await db.execute(select(models.User).where(models.User.phone_number == phone))
        user = res.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"No account found associated with phone number {phone}. Please check or register."
            )
            
    # Generate cryptographic 6-digit OTP
    otp = f"{secrets.randbelow(900000) + 100000}"
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Store in database
    otp_record = models.OTPVerification(
        phone_number=phone,
        otp_code=otp,
        purpose=req.purpose,
        expires_at=expires_at
    )
    db.add(otp_record)
    await db.commit()
    
    # Simulated SMS gateway dispatch log (pluggable with Twilio/Fast2SMS/AWS SNS)
    print(f"\n=======================================================")
    print(f"📩 [SMS GATEWAY SIMULATION] To: {phone}")
    print(f"💬 Message: Your PrepAce verification code is: {otp}. Valid for 5 minutes. Do not share.")
    print(f"=======================================================\n")
    
    # Return masked phone and demo_otp for instant seamless testing
    masked_phone = phone[:3] + "******" + phone[-4:] if len(phone) > 7 else phone
    return schemas.OTPResponse(
        status="sent",
        message=f"6-digit verification code sent via SMS to {masked_phone}",
        phone_number=phone,
        demo_otp=otp,
        expires_in_seconds=300
    )


@router.post("/verify-otp-login", response_model=schemas.Token)
async def verify_otp_login(req: schemas.VerifyOTPLoginRequest, db: AsyncSession = Depends(get_db)):
    """Logs the user in directly with phone OTP."""
    phone = normalize_phone(req.phone_number)
    now = datetime.utcnow()
    
    # Find matching valid OTP
    res = await db.execute(
        select(models.OTPVerification)
        .where(
            models.OTPVerification.phone_number == phone,
            models.OTPVerification.otp_code == req.otp.strip(),
            models.OTPVerification.purpose == "login",
            models.OTPVerification.is_used == False,
            models.OTPVerification.expires_at > now
        )
        .order_by(models.OTPVerification.created_at.desc())
    )
    record = res.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP code. Please request a new one.")
        
    # Mark OTP as used
    record.is_used = True
    
    # Check if user already exists with this phone number
    user_res = await db.execute(select(models.User).where(models.User.phone_number == phone))
    user = user_res.scalar_one_or_none()
    
    if not user:
        # Auto-create profile for this phone number
        short_num = phone[-6:]
        auto_username = f"user_{short_num}_{secrets.randbelow(9999)}"
        auto_email = f"{short_num}_{secrets.token_hex(3)}@student.prepace.com"
        user = models.User(
            email=auto_email,
            username=auto_username,
            phone_number=phone,
            hashed_password=hash_password(secrets.token_urlsafe(16)),
            target_exam="both"
        )
        db.add(user)
        
    await db.commit()
    await db.refresh(user)
    
    token = create_access_token({"sub": str(user.id)})
    return schemas.Token(
        access_token=token,
        token_type="bearer",
        user=schemas.UserOut.model_validate(user)
    )


@router.post("/reset-password-otp", response_model=schemas.Token)
async def reset_password_with_otp(req: schemas.ResetPasswordWithOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verifies OTP and sets new password for user account."""
    phone = normalize_phone(req.phone_number)
    now = datetime.utcnow()
    
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters")
        
    res = await db.execute(
        select(models.OTPVerification)
        .where(
            models.OTPVerification.phone_number == phone,
            models.OTPVerification.otp_code == req.otp.strip(),
            models.OTPVerification.purpose == "forgot_password",
            models.OTPVerification.is_used == False,
            models.OTPVerification.expires_at > now
        )
        .order_by(models.OTPVerification.created_at.desc())
    )
    record = res.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")
        
    user_res = await db.execute(select(models.User).where(models.User.phone_number == phone))
    user = user_res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="No registered account found with this phone number.")
        
    # Update password and mark OTP used
    record.is_used = True
    user.hashed_password = hash_password(req.new_password)
    await db.commit()
    await db.refresh(user)
    
    token = create_access_token({"sub": str(user.id)})
    return schemas.Token(
        access_token=token,
        token_type="bearer",
        user=schemas.UserOut.model_validate(user)
    )


@router.get("/me", response_model=schemas.UserOut)
async def get_me(current_user: models.User = Depends(get_current_user)):
    return schemas.UserOut.model_validate(current_user)


@router.put("/me", response_model=schemas.UserOut)
async def update_me(
    updates: dict,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    allowed_fields = ["target_exam", "target_score", "username", "phone_number"]
    for field in allowed_fields:
        if field in updates:
            val = updates[field]
            if field == "phone_number" and val:
                val = normalize_phone(val)
            setattr(current_user, field, val)
    await db.commit()
    await db.refresh(current_user)
    return schemas.UserOut.model_validate(current_user)
