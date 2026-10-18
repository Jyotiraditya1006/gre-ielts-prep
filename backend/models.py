from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    target_exam = Column(String, default="both")  # gre, ielts, both
    target_score = Column(Float, nullable=True)
    
    sessions = relationship("TestSession", back_populates="user")
    flashcard_progress = relationship("FlashcardProgress", back_populates="user")


class OTPVerification(Base):
    __tablename__ = "otp_verifications"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=False)
    otp_code = Column(String, nullable=False)
    purpose = Column(String, default="login")  # 'login' or 'forgot_password'
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)



class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    exam = Column(String, nullable=False)          # gre, ielts
    section = Column(String, nullable=False)        # verbal, quant, awa, reading, writing, listening, speaking
    subsection = Column(String, nullable=True)      # e.g. text_completion, sentence_equivalence, mcq
    difficulty = Column(String, default="medium")   # easy, medium, hard
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)           # list of options for MCQ
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    passage = Column(Text, nullable=True)           # for reading comprehension
    time_limit = Column(Integer, default=60)        # seconds per question
    tags = Column(JSON, nullable=True)              # topic tags
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    attempts = relationship("QuestionAttempt", back_populates="question")


class TestSession(Base):
    __tablename__ = "test_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam = Column(String, nullable=False)
    session_type = Column(String, nullable=False)  # full_mock, topic_practice, flashcard
    section = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    score = Column(Float, nullable=True)
    scaled_score = Column(String, nullable=True)   # e.g. "320/340" for GRE
    time_taken = Column(Integer, nullable=True)    # seconds
    is_completed = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="sessions")
    attempts = relationship("QuestionAttempt", back_populates="session")


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_spent = Column(Integer, default=0)  # seconds
    attempted_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("TestSession", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")


class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    exam = Column(String, nullable=False)      # gre, ielts, both
    word = Column(String, nullable=False)
    definition = Column(Text, nullable=False)
    example_sentence = Column(Text, nullable=True)
    mnemonic = Column(Text, nullable=True)
    difficulty = Column(String, default="medium")
    category = Column(String, nullable=True)   # e.g. "high-frequency", "academic"
    
    progress = relationship("FlashcardProgress", back_populates="flashcard")


class FlashcardProgress(Base):
    __tablename__ = "flashcard_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False)
    ease_factor = Column(Float, default=2.5)    # spaced repetition
    interval = Column(Integer, default=1)        # days until next review
    repetitions = Column(Integer, default=0)
    next_review = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="flashcard_progress")
    flashcard = relationship("Flashcard", back_populates="progress")
