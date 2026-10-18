from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_user, get_optional_current_user

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("/", response_model=List[schemas.FlashcardOut])
async def get_flashcards(
    exam: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = select(models.Flashcard)
    if exam:
        query = query.where(models.Flashcard.exam == exam)
    if difficulty:
        query = query.where(models.Flashcard.difficulty == difficulty)
    if category:
        query = query.where(models.Flashcard.category == category)
    query = query.limit(limit)
    
    result = await db.execute(query)
    cards = result.scalars().all()
    return [schemas.FlashcardOut.model_validate(c) for c in cards]


@router.get("/due", response_model=List[schemas.FlashcardOut])
async def get_due_flashcards(
    exam: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get flashcards due for review (spaced repetition)."""
    now = datetime.utcnow()
    
    # Get cards with progress that are due
    progress_result = await db.execute(
        select(models.FlashcardProgress, models.Flashcard)
        .join(models.Flashcard, models.FlashcardProgress.flashcard_id == models.Flashcard.id)
        .where(models.FlashcardProgress.user_id == current_user.id)
        .where(models.FlashcardProgress.next_review <= now)
    )
    due_with_progress = progress_result.all()
    
    # Also get cards never seen before
    seen_ids_result = await db.execute(
        select(models.FlashcardProgress.flashcard_id)
        .where(models.FlashcardProgress.user_id == current_user.id)
    )
    seen_ids = [row[0] for row in seen_ids_result.all()]
    
    unseen_query = select(models.Flashcard).where(
        ~models.Flashcard.id.in_(seen_ids) if seen_ids else True
    )
    if exam:
        unseen_query = unseen_query.where(models.Flashcard.exam == exam)
    unseen_query = unseen_query.limit(max(0, limit - len(due_with_progress)))
    
    unseen_result = await db.execute(unseen_query)
    unseen_cards = unseen_result.scalars().all()
    
    all_cards = [f for _, f in due_with_progress] + list(unseen_cards)
    return [schemas.FlashcardOut.model_validate(c) for c in all_cards[:limit]]


@router.post("/review")
async def review_flashcard(
    review: schemas.FlashcardReview,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update spaced repetition schedule based on review rating."""
    # Get or create progress record
    result = await db.execute(
        select(models.FlashcardProgress).where(
            models.FlashcardProgress.user_id == current_user.id,
            models.FlashcardProgress.flashcard_id == review.flashcard_id
        )
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        progress = models.FlashcardProgress(
            user_id=current_user.id,
            flashcard_id=review.flashcard_id
        )
        db.add(progress)
    
    # SM-2 algorithm simplified
    rating = review.rating  # 0=again, 1=hard, 2=good, 3=easy
    
    if rating == 0:  # Again
        progress.repetitions = 0
        progress.interval = 1
        progress.ease_factor = max(1.3, progress.ease_factor - 0.2)
    elif rating == 1:  # Hard
        progress.interval = max(1, int(progress.interval * 1.2))
        progress.ease_factor = max(1.3, progress.ease_factor - 0.15)
    elif rating == 2:  # Good
        if progress.repetitions == 0:
            progress.interval = 1
        elif progress.repetitions == 1:
            progress.interval = 6
        else:
            progress.interval = round(progress.interval * progress.ease_factor)
        progress.repetitions += 1
    elif rating == 3:  # Easy
        if progress.repetitions == 0:
            progress.interval = 4
        else:
            progress.interval = round(progress.interval * progress.ease_factor * 1.3)
        progress.ease_factor = min(3.0, progress.ease_factor + 0.1)
        progress.repetitions += 1
    
    progress.last_reviewed = datetime.utcnow()
    progress.next_review = datetime.utcnow() + timedelta(days=progress.interval)
    
    await db.commit()
    return {"next_review_in_days": progress.interval, "ease_factor": progress.ease_factor}


@router.get("/infinite-word", response_model=schemas.FlashcardOut)
async def get_infinite_flashcard_word(
    exam: Optional[str] = Query("both"),
    difficulty: Optional[str] = Query("medium"),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Returns an instant vocabulary word from the 2,500,000+ words lexicon.
    Generates new cards on the fly with etymology, mnemonics, and examples.
    """
    from backend.vocab_engine import InfiniteVocabEngine
    card_data = InfiniteVocabEngine.generate_procedural_word(exam=exam or "both", difficulty=difficulty or "medium")
    
    # Check if already in DB
    existing = await db.execute(select(models.Flashcard).where(models.Flashcard.word == card_data["word"]))
    found = existing.scalar_one_or_none()
    if found:
        return schemas.FlashcardOut.model_validate(found)
        
    fc = models.Flashcard(
        exam=card_data.get("exam", "both"),
        word=card_data["word"],
        definition=card_data["definition"],
        example_sentence=card_data.get("example"),
        mnemonic=card_data.get("mnemonic"),
        difficulty=card_data.get("difficulty", "medium"),
        category=card_data.get("category", "academic")
    )
    db.add(fc)
    await db.commit()
    await db.refresh(fc)
    return schemas.FlashcardOut.model_validate(fc)


@router.get("/infinite-batch", response_model=List[schemas.FlashcardOut])
async def get_infinite_flashcard_batch(
    exam: Optional[str] = Query("both"),
    difficulty: Optional[str] = Query("medium"),
    count: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """Batch fetch from the multi-million word vocabulary engine for zero-latency review."""
    from backend.vocab_engine import InfiniteVocabEngine
    cards = []
    for _ in range(count):
        card_data = InfiniteVocabEngine.generate_procedural_word(exam=exam or "both", difficulty=difficulty or "medium")
        existing = await db.execute(select(models.Flashcard).where(models.Flashcard.word == card_data["word"]))
        found = existing.scalar_one_or_none()
        if found:
            cards.append(found)
        else:
            fc = models.Flashcard(
                exam=card_data.get("exam", "both"),
                word=card_data["word"],
                definition=card_data["definition"],
                example_sentence=card_data.get("example"),
                mnemonic=card_data.get("mnemonic"),
                difficulty=card_data.get("difficulty", "medium"),
                category=card_data.get("category", "academic")
            )
            db.add(fc)
            cards.append(fc)
    await db.commit()
    for c in cards:
        await db.refresh(c)
    return [schemas.FlashcardOut.model_validate(c) for c in cards]


@router.get("/search", response_model=schemas.FlashcardOut)
async def search_flashcard_word(
    q: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    Search millions of words in the English lexicon with roots, mnemonics, and definitions.
    """
    from backend.vocab_engine import InfiniteVocabEngine
    word_clean = q.strip().lower()
    
    # Check DB first
    existing = await db.execute(select(models.Flashcard).where(models.Flashcard.word == word_clean))
    found = existing.scalar_one_or_none()
    if found:
        return schemas.FlashcardOut.model_validate(found)
        
    card_data = InfiniteVocabEngine.search_word(word_clean)
    if not card_data:
        raise HTTPException(status_code=404, detail="Word not found")
        
    fc = models.Flashcard(
        exam=card_data.get("exam", "both"),
        word=card_data["word"],
        definition=card_data["definition"],
        example_sentence=card_data.get("example"),
        mnemonic=card_data.get("mnemonic"),
        difficulty=card_data.get("difficulty", "medium"),
        category=card_data.get("category", "searched")
    )
    db.add(fc)
    await db.commit()
    await db.refresh(fc)
    return schemas.FlashcardOut.model_validate(fc)


@router.get("/stats")
async def get_flashcard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """Get flashcard study statistics including the full multi-million lexicon size."""
    from backend.vocab_engine import InfiniteVocabEngine
    if current_user:
        result = await db.execute(
            select(models.FlashcardProgress)
            .where(models.FlashcardProgress.user_id == current_user.id)
        )
        all_progress = result.scalars().all()
        total_studied = len(all_progress)
        mastered = sum(1 for p in all_progress if p.repetitions >= 5 and p.ease_factor >= 2.5)
        due_today = sum(1 for p in all_progress if p.next_review <= datetime.utcnow())
    else:
        total_studied = 0
        mastered = 0
        due_today = 0
    
    return {
        "total_studied": total_studied,
        "mastered": mastered,
        "due_today": due_today,
        "learning": total_studied - mastered,
        "total_lexicon_size": InfiniteVocabEngine.get_total_words_count()
    }

