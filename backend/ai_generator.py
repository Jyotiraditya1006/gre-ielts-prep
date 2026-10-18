"""
AI question generation using Gemini API.
Falls back to seed questions if API key is not configured.
"""
import json
import httpx
from backend.config import settings


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"


QUESTION_PROMPTS = {
    "gre_verbal": """Generate {num} GRE Verbal Reasoning questions of {difficulty} difficulty{topic_str}.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string
- "subsection": one of ["text_completion", "sentence_equivalence", "reading_comprehension"]
- "options": array of 5 strings (for text_completion/sentence_equivalence) or null for reading_comp passage questions
- "correct_answer": string (the exact answer)
- "explanation": string (brief explanation)
- "passage": string or null (only for reading_comprehension)
- "tags": array of strings

Focus on graduate-level vocabulary, logical reasoning, and reading comprehension.""",

    "gre_quant": """Generate {num} GRE Quantitative Reasoning questions of {difficulty} difficulty{topic_str}.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string  
- "subsection": one of ["problem_solving", "quantitative_comparison", "data_interpretation"]
- "options": array of 5 strings
- "correct_answer": string
- "explanation": string (show full working)
- "tags": array of strings

Cover: algebra, geometry, statistics, number theory, word problems.""",

    "gre_awa": """Generate {num} GRE Analytical Writing Assessment prompts of {difficulty} difficulty.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string (the full essay prompt)
- "subsection": one of ["analyze_an_issue", "analyze_an_argument"]
- "options": null
- "correct_answer": "essay"
- "explanation": string (key points to address, scoring criteria)
- "tags": array of strings""",

    "ielts_reading": """Generate {num} IELTS Academic Reading questions of {difficulty} difficulty{topic_str}.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string
- "subsection": one of ["true_false_not_given", "matching_headings", "multiple_choice", "sentence_completion", "summary_completion"]
- "passage": string (relevant passage text, 150-300 words)
- "options": array of 4-5 strings
- "correct_answer": string
- "explanation": string
- "tags": array of strings""",

    "ielts_writing": """Generate {num} IELTS Writing task prompts of {difficulty} difficulty{topic_str}.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string (full task description)
- "subsection": one of ["task_1_academic", "task_2", "task_1_general"]
- "options": null
- "correct_answer": "essay"
- "explanation": string (band descriptors guidance, key points)
- "tags": array of strings""",

    "ielts_speaking": """Generate {num} IELTS Speaking questions/cue cards of {difficulty} difficulty{topic_str}.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string (full speaking task with bullet points if Part 2)
- "subsection": one of ["part_1", "part_2", "part_3"]
- "options": null
- "correct_answer": "spoken_response"
- "explanation": string (tips, sample language, what examiners look for)
- "tags": array of strings""",

    "ielts_listening": """Generate {num} IELTS Listening section practice questions of {difficulty} difficulty{topic_str}.
Return ONLY a valid JSON array. Each object must have:
- "question_text": string (the question or sentence completion prompt)
- "passage": string (the audio transcript/dialogue context, 100-200 words)
- "subsection": one of ["form_completion", "multiple_choice", "matching", "map_labeling", "sentence_completion"]
- "options": array of 4 strings or null if short answer
- "correct_answer": string
- "explanation": string (explaining where in the transcript the answer is found)
- "tags": array of strings""",
}



async def generate_questions_with_ai(exam: str, section: str, difficulty: str, num: int, topic: str = None) -> list:
    """Generate questions using Gemini API."""
    if not settings.GEMINI_API_KEY:
        return []
    
    prompt_key = f"{exam}_{section}"
    prompt_template = QUESTION_PROMPTS.get(prompt_key)
    if not prompt_template:
        return []
    
    topic_str = f" on the topic of {topic}" if topic else ""
    prompt = prompt_template.format(num=num, difficulty=difficulty, topic_str=topic_str)
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 4096,
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            
            # Extract JSON from markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            questions = json.loads(text)
            
            # Add metadata
            for q in questions:
                q["exam"] = exam
                q["section"] = section
                q["difficulty"] = difficulty
                q["is_ai_generated"] = True
                q["time_limit"] = _get_time_limit(section, q.get("subsection", ""))
            
            return questions
    except Exception as e:
        print(f"AI generation error: {e}")
        return []


def _get_time_limit(section: str, subsection: str) -> int:
    """Return appropriate time limit in seconds."""
    limits = {
        "verbal": 90,
        "quant": 120,
        "awa": 1800,
        "reading": 90,
        "writing": 2400 if "task_2" in subsection else 1200,
        "speaking": 120 if "part_2" in subsection else (60 if "part_1" in subsection else 240),
    }
    return limits.get(section, 90)
