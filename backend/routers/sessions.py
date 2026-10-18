from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _calculate_gre_scaled_score(section: str, accuracy: float) -> str:
    """Approximate GRE scaled score based on accuracy."""
    if section == "verbal":
        min_s, max_s = 130, 170
    elif section == "quant":
        min_s, max_s = 130, 170
    elif section == "awa":
        min_s, max_s = 0, 6
        score = round(accuracy / 100 * 6 * 2) / 2  # 0.5 increments
        return f"{score}/6.0"
    else:
        return None
    
    scaled = round(min_s + (accuracy / 100) * (max_s - min_s))
    return f"{scaled}/170"


def _calculate_ielts_band(accuracy: float) -> str:
    """Approximate IELTS band score."""
    band = round((accuracy / 100) * 9 * 2) / 2  # 0.5 increments
    band = max(0, min(9, band))
    return f"{band}/9.0"


@router.post("/start", response_model=dict)
async def start_session(
    req: schemas.SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    session = models.TestSession(
        user_id=current_user.id,
        exam=req.exam,
        session_type=req.session_type,
        section=req.section,
        total_questions=req.num_questions or 20
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {"session_id": session.id, "message": "Session started"}


@router.post("/submit", response_model=schemas.SessionResult)
async def submit_session(
    submission: schemas.SessionSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get session
    result = await db.execute(select(models.TestSession).where(
        models.TestSession.id == submission.session_id,
        models.TestSession.user_id == current_user.id
    ))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Process each attempt
    correct = 0
    total_time = 0
    attempt_results = []
    
    for attempt_data in submission.attempts:
        # Get the question
        q_result = await db.execute(select(models.Question).where(
            models.Question.id == attempt_data.question_id
        ))
        question = q_result.scalar_one_or_none()
        
        is_correct = False
        if question:
            # For essay questions, mark as attempted (manual review needed)
            if question.correct_answer in ["essay", "spoken_response", "letter"]:
                is_correct = True  # Auto-pass essay questions
            else:
                is_correct = attempt_data.user_answer.strip().lower() == question.correct_answer.strip().lower()
        
        if is_correct:
            correct += 1
        total_time += attempt_data.time_spent
        
        attempt = models.QuestionAttempt(
            session_id=session.id,
            question_id=attempt_data.question_id,
            user_answer=attempt_data.user_answer,
            is_correct=is_correct,
            time_spent=attempt_data.time_spent
        )
        db.add(attempt)
        
        if question:
            attempt_results.append({
                "question_id": question.id,
                "question_text": question.question_text[:100] + "...",
                "user_answer": attempt_data.user_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation,
                "time_spent": attempt_data.time_spent
            })
    
    # Calculate score
    total = len(submission.attempts)
    accuracy = (correct / total * 100) if total > 0 else 0
    
    # Calculate scaled score
    scaled_score = None
    if session.exam == "gre" and session.section:
        scaled_score = _calculate_gre_scaled_score(session.section, accuracy)
    elif session.exam == "ielts":
        scaled_score = _calculate_ielts_band(accuracy)
    
    # Update session
    session.correct_answers = correct
    session.total_questions = total
    session.score = round(accuracy, 1)
    session.scaled_score = scaled_score
    session.time_taken = total_time
    session.is_completed = True
    session.completed_at = datetime.utcnow()
    
    await db.commit()
    
    return schemas.SessionResult(
        session_id=session.id,
        exam=session.exam,
        section=session.section,
        total_questions=total,
        correct_answers=correct,
        score=round(accuracy, 1),
        scaled_score=scaled_score,
        time_taken=total_time,
        attempts=attempt_results
    )


@router.get("/history")
async def get_session_history(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.TestSession)
        .where(models.TestSession.user_id == current_user.id)
        .where(models.TestSession.is_completed == True)
        .order_by(models.TestSession.completed_at.desc())
        .limit(50)
    )
    sessions = result.scalars().all()
    
    return [
        {
            "id": s.id,
            "exam": s.exam,
            "section": s.section,
            "session_type": s.session_type,
            "score": s.score,
            "scaled_score": s.scaled_score,
            "total_questions": s.total_questions,
            "correct_answers": s.correct_answers,
            "time_taken": s.time_taken,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None
        }
        for s in sessions
    ]
