import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from backend.database import init_db
from backend.routers import auth, questions, sessions, analytics, flashcards
from backend import models
from backend.database import AsyncSessionLocal
from backend.question_bank import get_all_seed_questions, get_all_flashcards


async def seed_database():
    """Seed the database with initial questions and flashcards."""
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select, func
        
        # Check if already seeded
        result = await db.execute(select(func.count()).select_from(models.Question))
        count = result.scalar()
        
        if count == 0:
            print("🌱 Seeding question bank...")
            for q_data in get_all_seed_questions():
                q = models.Question(
                    exam=q_data["exam"],
                    section=q_data["section"],
                    subsection=q_data.get("subsection"),
                    difficulty=q_data.get("difficulty", "medium"),
                    question_text=q_data["question_text"],
                    options=q_data.get("options"),
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation"),
                    passage=q_data.get("passage"),
                    time_limit=q_data.get("time_limit", 90),
                    tags=q_data.get("tags", []),
                    is_ai_generated=False
                )
                db.add(q)
            await db.commit()
            print(f"✅ Seeded {len(get_all_seed_questions())} questions")
        
        # Check flashcards
        result2 = await db.execute(select(func.count()).select_from(models.Flashcard))
        fc_count = result2.scalar()
        
        if fc_count == 0:
            print("🌱 Seeding flashcards...")
            for fc_data in get_all_flashcards():
                fc = models.Flashcard(
                    exam=fc_data["exam"],
                    word=fc_data["word"],
                    definition=fc_data["definition"],
                    example_sentence=fc_data.get("example_sentence"),
                    mnemonic=fc_data.get("mnemonic"),
                    difficulty=fc_data.get("difficulty", "medium"),
                    category=fc_data.get("category")
                )
                db.add(fc)
            await db.commit()
            print(f"✅ Seeded {len(get_all_flashcards())} flashcards")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_database()
    yield


app = FastAPI(
    title="GRE & IELTS Prep Platform",
    description="Comprehensive preparation platform for GRE and IELTS exams",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(auth.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(flashcards.router, prefix="/api")

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "GRE & IELTS Prep API is running"}

# Serve frontend (must be AFTER all API routes)
frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))
    
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        # Don't catch API routes
        if full_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = os.path.join(frontend_path, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_path, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
