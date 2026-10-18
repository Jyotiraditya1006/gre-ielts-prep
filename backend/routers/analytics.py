from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from collections import defaultdict
from backend.database import get_db
from backend import models, schemas
from backend.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=schemas.AnalyticsSummary)
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get all completed sessions
    sessions_result = await db.execute(
        select(models.TestSession)
        .where(models.TestSession.user_id == current_user.id)
        .where(models.TestSession.is_completed == True)
        .order_by(models.TestSession.completed_at)
    )
    sessions = sessions_result.scalars().all()
    
    if not sessions:
        return schemas.AnalyticsSummary(
            total_sessions=0, total_questions_attempted=0, overall_accuracy=0.0,
            avg_time_per_question=0.0, sessions_by_exam={}, accuracy_by_section={},
            weak_areas=[], strong_areas=[], score_trend=[], recent_sessions=[]
        )
    
    # Get all attempts
    attempts_result = await db.execute(
        select(models.QuestionAttempt, models.Question)
        .join(models.Question, models.QuestionAttempt.question_id == models.Question.id)
        .join(models.TestSession, models.QuestionAttempt.session_id == models.TestSession.id)
        .where(models.TestSession.user_id == current_user.id)
    )
    attempts_with_q = attempts_result.all()
    
    total_q = len(attempts_with_q)
    correct_q = sum(1 for a, q in attempts_with_q if a.is_correct)
    total_time = sum(a.time_spent for a, q in attempts_with_q if a.time_spent)
    
    # Sessions by exam
    sessions_by_exam = defaultdict(int)
    for s in sessions:
        sessions_by_exam[s.exam] += 1
    
    # Accuracy by section
    section_stats = defaultdict(lambda: {"correct": 0, "total": 0, "time": 0})
    for a, q in attempts_with_q:
        key = f"{q.exam}_{q.section}"
        section_stats[key]["total"] += 1
        section_stats[key]["time"] += a.time_spent or 0
        if a.is_correct:
            section_stats[key]["correct"] += 1
    
    accuracy_by_section = {}
    for section, stats in section_stats.items():
        if stats["total"] > 0:
            accuracy_by_section[section] = round(stats["correct"] / stats["total"] * 100, 1)
    
    # Weak/strong areas
    sorted_sections = sorted(accuracy_by_section.items(), key=lambda x: x[1])
    weak_areas = [s for s, _ in sorted_sections[:3] if accuracy_by_section.get(s, 100) < 60]
    strong_areas = [s for s, _ in reversed(sorted_sections[-3:]) if accuracy_by_section.get(s, 0) > 75]
    
    # Score trend (last 20 sessions)
    score_trend = [
        {
            "date": s.completed_at.isoformat() if s.completed_at else None,
            "score": s.score,
            "exam": s.exam,
            "section": s.section,
            "scaled_score": s.scaled_score
        }
        for s in sessions[-20:]
    ]
    
    # Recent sessions
    recent = [
        {
            "id": s.id,
            "exam": s.exam,
            "section": s.section,
            "score": s.score,
            "scaled_score": s.scaled_score,
            "total_questions": s.total_questions,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None
        }
        for s in sessions[-5:][::-1]
    ]
    
    return schemas.AnalyticsSummary(
        total_sessions=len(sessions),
        total_questions_attempted=total_q,
        overall_accuracy=round(correct_q / total_q * 100, 1) if total_q else 0.0,
        avg_time_per_question=round(total_time / total_q, 1) if total_q else 0.0,
        sessions_by_exam=dict(sessions_by_exam),
        accuracy_by_section=accuracy_by_section,
        weak_areas=weak_areas,
        strong_areas=strong_areas,
        score_trend=score_trend,
        recent_sessions=recent
    )
