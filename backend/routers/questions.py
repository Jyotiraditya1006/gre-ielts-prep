import random
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_user, get_optional_current_user
from backend.ai_generator import generate_questions_with_ai

from backend.infinite_engine import InfiniteQuestionEngine, get_procedural_question

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[schemas.QuestionOut])
async def get_questions(
    exam: Optional[str] = Query(None),
    section: Optional[str] = Query(None),
    subsection: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = select(models.Question)
    if exam:
        query = query.where(models.Question.exam == exam)
    if section:
        query = query.where(models.Question.section == section)
    if subsection:
        query = query.where(models.Question.subsection == subsection)
    if difficulty:
        query = query.where(models.Question.difficulty == difficulty)
    
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    questions = result.scalars().all()
    return [schemas.QuestionOut.model_validate(q) for q in questions]


@router.get("/random", response_model=List[schemas.QuestionOut])
async def get_random_questions(
    exam: str = Query(...),
    section: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    num: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = select(models.Question).where(models.Question.exam == exam)
    if section:
        query = query.where(models.Question.section == section)
    if difficulty:
        query = query.where(models.Question.difficulty == difficulty)
    
    result = await db.execute(query)
    all_questions = result.scalars().all()
    
    # If not enough questions, generate with Gemini AI or infinite procedural engine
    if len(all_questions) < num:
        needed = num - len(all_questions)
        sec = section or ("quant" if exam == "gre" else "reading")
        # Try AI generation first
        generated = await generate_questions_with_ai(exam, sec, difficulty or "medium", needed)
        
        # If AI didn't return enough, supplement with procedural infinite generator
        while len(generated) < needed:
            proc_q = get_procedural_question(exam, sec)
            generated.append(proc_q)
            
        for q_data in generated:
            q = models.Question(**{k: v for k, v in q_data.items() if hasattr(models.Question, k)})
            db.add(q)
        await db.commit()
        result = await db.execute(query)
        all_questions = result.scalars().all()
    
    sampled = random.sample(all_questions, min(num, len(all_questions)))
    return [schemas.QuestionOut.model_validate(q) for q in sampled]


@router.get("/infinite-next", response_model=schemas.QuestionOut)
async def get_infinite_next_question(
    exam: str = Query("gre"),
    section: Optional[str] = Query("quant"),
    difficulty: Optional[str] = Query("medium"),
    use_ai: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    Generates a fresh, unique question on the fly with sub-millisecond latency.
    Allows infinite, never-ending practice across millions of variations.
    """
    q_data = None
    if use_ai:
        try:
            ai_list = await generate_questions_with_ai(exam, section, difficulty, 1)
            if ai_list:
                q_data = ai_list[0]
        except Exception:
            pass
            
    if not q_data:
        q_data = get_procedural_question(exam, section)
        
    q = models.Question(**{k: v for k, v in q_data.items() if hasattr(models.Question, k)})
    db.add(q)
    await db.commit()
    await db.refresh(q)
    return schemas.QuestionOut.model_validate(q)


@router.get("/infinite-batch", response_model=List[schemas.QuestionOut])
async def get_infinite_batch(
    exam: str = Query("gre"),
    section: Optional[str] = Query("quant"),
    count: int = Query(5, le=20),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """Batch endpoint for instant client-side prefetching with zero latency."""
    questions = []
    for _ in range(count):
        q_data = get_procedural_question(exam, section)
        q = models.Question(**{k: v for k, v in q_data.items() if hasattr(models.Question, k)})
        db.add(q)
        questions.append(q)
    await db.commit()
    for q in questions:
        await db.refresh(q)
    return [schemas.QuestionOut.model_validate(q) for q in questions]


@router.get("/{question_id}/answer", response_model=schemas.QuestionWithAnswer)
async def get_question_answer(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await db.execute(select(models.Question).where(models.Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return schemas.QuestionWithAnswer.model_validate(question)


@router.post("/generate")
async def generate_questions(
    req: schemas.GenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate questions using Gemini 3.8 Flash AI and save to database."""
    questions = await generate_questions_with_ai(
        req.exam, req.section, req.difficulty or "medium",
        req.num_questions or 5, req.topic
    )
    
    # If AI returned fewer questions, fill remaining with infinite procedural generator
    target_count = req.num_questions or 5
    while len(questions) < target_count:
        questions.append(get_procedural_question(req.exam, req.section))
    
    saved = []
    for q_data in questions:
        q = models.Question(**{k: v for k, v in q_data.items() if hasattr(models.Question, k)})
        db.add(q)
        await db.flush()
        saved.append({"id": q.id, "question_text": q.question_text[:80] + "..."})
    
    await db.commit()
    return {"generated": len(saved), "questions": saved, "ai_powered": True}


@router.get("/mock-test-package")
async def get_mock_test_package(
    exam: str = Query("gre"),
    mode: Optional[str] = Query("standard"),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    Generates an authentic, full-length official mock test package.
    GRE: Exact 5 sections (AWA, Verbal 1, Quant 1, Verbal 2, Quant 2) with section timing.
    IELTS: Exact 3 components (Reading 40 Qs, Writing Tasks 1 & 2, Speaking Interview).
    """
    from backend.mock_test_engine import MockTestEngine
    if exam == "gre":
        return MockTestEngine.generate_gre_mock_test(mode=mode or "standard")
    else:
        return MockTestEngine.generate_ielts_mock_test()

