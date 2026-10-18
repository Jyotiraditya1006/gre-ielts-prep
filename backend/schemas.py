from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    target_exam: Optional[str] = "both"
    target_score: Optional[float] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    target_exam: str
    target_score: Optional[float]
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


# ── Questions ─────────────────────────────────────────────────────────────────

class QuestionOut(BaseModel):
    id: int
    exam: str
    section: str
    subsection: Optional[str]
    difficulty: str
    question_text: str
    options: Optional[List[str]]
    passage: Optional[str]
    time_limit: int
    tags: Optional[List[str]]
    class Config:
        from_attributes = True

class QuestionWithAnswer(QuestionOut):
    correct_answer: str
    explanation: Optional[str]


# ── Sessions ──────────────────────────────────────────────────────────────────

class SessionCreate(BaseModel):
    exam: str
    session_type: str
    section: Optional[str] = None
    num_questions: Optional[int] = 20

class AttemptSubmit(BaseModel):
    question_id: int
    user_answer: str
    time_spent: int

class SessionSubmit(BaseModel):
    session_id: int
    attempts: List[AttemptSubmit]

class SessionResult(BaseModel):
    session_id: int
    exam: str
    section: Optional[str]
    total_questions: int
    correct_answers: int
    score: float
    scaled_score: Optional[str]
    time_taken: int
    attempts: List[dict]
    class Config:
        from_attributes = True


# ── Analytics ─────────────────────────────────────────────────────────────────

class AnalyticsSummary(BaseModel):
    total_sessions: int
    total_questions_attempted: int
    overall_accuracy: float
    avg_time_per_question: float
    sessions_by_exam: dict
    accuracy_by_section: dict
    weak_areas: List[str]
    strong_areas: List[str]
    score_trend: List[dict]
    recent_sessions: List[dict]


# ── Flashcards ────────────────────────────────────────────────────────────────

class FlashcardOut(BaseModel):
    id: int
    exam: str
    word: str
    definition: str
    example_sentence: Optional[str]
    mnemonic: Optional[str]
    difficulty: str
    category: Optional[str]
    class Config:
        from_attributes = True

class FlashcardReview(BaseModel):
    flashcard_id: int
    rating: int  # 0=again, 1=hard, 2=good, 3=easy


# ── AI Generation ─────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    exam: str
    section: str
    difficulty: Optional[str] = "medium"
    num_questions: Optional[int] = 5
    topic: Optional[str] = None
