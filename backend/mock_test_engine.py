"""
Authentic Full Mock Test Engine for GRE and IELTS
Replicates the exact format, section timing, question types, and scoring rubrics
of the official ETS GRE General Test (Shorter GRE format) and IDP/British Council IELTS Computer-Delivered Test.
"""
import random
from typing import Dict, Any, List
from backend.infinite_engine import InfiniteQuestionEngine


AWA_PROMPTS = [
    {
        "id": 9001,
        "type": "analyze_an_issue",
        "title": "Analyze an Issue",
        "prompt": "As people rely more and more on technology to solve problems, the ability of humans to think for themselves will surely deteriorate.",
        "instructions": "Discuss the extent to which you agree or disagree with the statement and explain your reasoning for the position you take. In developing and supporting your position, you should consider ways in which the statement might or might not hold true and explain how these considerations shape your position.",
        "time_limit": 1800,  # 30 mins
        "exam": "gre",
        "section": "awa"
    },
    {
        "id": 9002,
        "type": "analyze_an_issue",
        "title": "Analyze an Issue",
        "prompt": "Governments should offer free college or university education to any student who wishes to pursue it, regardless of their financial circumstances.",
        "instructions": "Discuss the extent to which you agree or disagree with the recommendation and explain your reasoning for the position you take. In developing and supporting your position, describe specific circumstances in which adopting the recommendation would or would not be advantageous.",
        "time_limit": 1800,
        "exam": "gre",
        "section": "awa"
    },
    {
        "id": 9003,
        "type": "analyze_an_issue",
        "title": "Analyze an Issue",
        "prompt": "In any field of endeavor, it is impossible to make significant progress without first establishing a thorough mastery of past traditions and methods.",
        "instructions": "Discuss the extent to which you agree or disagree with the claim. In developing and supporting your position, address the strongest reasons or examples that could be used to challenge your position.",
        "time_limit": 1800,
        "exam": "gre",
        "section": "awa"
    }
]

IELTS_WRITING_TASKS = [
    {
        "task_1": {
            "title": "Task 1 – Visual Data Report",
            "prompt": "The table below shows the percentage of mobile phone owners using various mobile phone features in a European country between 2015 and 2023.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
            "data_visual": (
                "Feature                | 2015 | 2019 | 2023\n"
                "-----------------------|------|------|-----\n"
                "Making phone calls     | 100% |  99% |  98%\n"
                "Sending text messages  |  73% |  81% |  84%\n"
                "Browsing the Internet  |  41% |  72% |  89%\n"
                "Electronic banking     |  18% |  46% |  73%\n"
                "Playing mobile games   |  24% |  38% |  52%\n"
                "Streaming 4K video     |   8% |  29% |  61%"
            ),
            "min_words": 150,
            "suggested_time": 1200  # 20 mins
        },
        "task_2": {
            "title": "Task 2 – Discursive Academic Essay",
            "prompt": "Some people believe that unpaid community service should be a mandatory part of high school education programs (for example, working for a charity, improving the neighborhood, or teaching sports to younger children).\n\nTo what extent do you agree or disagree with this view?\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.\n\nWrite at least 250 words.",
            "min_words": 250,
            "suggested_time": 2400  # 40 mins
        }
    },
    {
        "task_1": {
            "title": "Task 1 – Process Diagram",
            "prompt": "The diagram below illustrates the process by which geothermal energy is used to produce electricity in power stations.\n\nSummarise the information by describing the sequential stages in the industrial process.\n\nWrite at least 150 words.",
            "data_visual": (
                "Stage 1: Cold water pumped 4.5 km underground into hot fractured granite.\n"
                "Stage 2: Water heated to 250°C under immense subterranean pressure.\n"
                "Stage 3: Superheated water pumped upward through production well into condenser.\n"
                "Stage 4: High-pressure steam spins turbine connected to electrical generator.\n"
                "Stage 5: Exhaust steam cooled in cooling tower, condensed to water, and reinjected."
            ),
            "min_words": 150,
            "suggested_time": 1200
        },
        "task_2": {
            "title": "Task 2 – Discursive Academic Essay",
            "prompt": "In many countries today, people are choosing to have children later in life than in previous generations.\n\nWhy is this trend occurring? Do the advantages of this trend outweigh the disadvantages for individuals and society as a whole?\n\nGive reasons for your answer and include any relevant examples.\n\nWrite at least 250 words.",
            "min_words": 250,
            "suggested_time": 2400
        }
    }
]

IELTS_SPEAKING_PARTS = [
    {
        "part_1": {
            "title": "Part 1 – Introduction and Familiar Topics (4–5 minutes)",
            "questions": [
                "What is your full name and where do you currently reside?",
                "Do you work or are you currently studying?",
                "Do you prefer living in a bustling city or in a quiet rural area? Why?",
                "How often do you read books or academic articles in your leisure time?",
                "What kind of music helps you concentrate while working or studying?"
            ]
        },
        "part_2": {
            "title": "Part 2 – Individual Long Turn (Cue Card - 3–4 minutes)",
            "prompt": (
                "Describe a challenging problem that you successfully solved using creativity or critical thinking.\n\n"
                "You should say:\n"
                "• What the specific problem was\n"
                "• How you discovered or encountered it\n"
                "• What action or strategy you took to address it\n"
                "and explain why you felt proud of solving this problem."
            ),
            "prep_time": 60,   # 1 minute prep
            "speech_time": 120 # 2 minute speech
        },
        "part_3": {
            "title": "Part 3 – Two-Way Thematic Discussion (4–5 minutes)",
            "questions": [
                "Do you think schools nowadays teach children sufficient practical problem-solving skills, or do they prioritize rote memorization?",
                "In what ways has rapid technological automation changed the types of problems professionals encounter in the workplace?",
                "Is it always preferable to solve a complex societal problem independently, or does collaboration yield superior outcomes?",
                "How can leaders encourage team members to propose unorthodox solutions without fear of failure?"
            ]
        }
    }
]


class MockTestEngine:
    """Generates authentic, ETS-identical GRE simulations and IDP/British Council IELTS tests."""

    @staticmethod
    def generate_gre_mock_test(mode: str = "standard") -> Dict[str, Any]:
        """
        Builds the exact ETS GRE Shorter Test (effective September 22, 2023):
        - Section 1: Analytical Writing (1 Analyze an Issue prompt) - 30 mins
        - Section 2: Verbal Reasoning 1 (12 Questions: TC, SE, RC) - 18 mins
        - Section 3: Quantitative Reasoning 1 (12 Questions: QC, PS, DI) - 21 mins [Calculator Allowed]
        - Section 4: Verbal Reasoning 2 (15 Questions: TC, SE, RC) - 23 mins
        - Section 5: Quantitative Reasoning 2 (15 Questions: QC, PS, DI) - 26 mins [Calculator Allowed]
        """
        awa_choice = random.choice(AWA_PROMPTS)

        # Build Section 2: Verbal 1 (12 Qs)
        verbal_1_qs = []
        for i in range(12):
            q = InfiniteQuestionEngine.generate_gre_verbal()
            q["id"] = 1000 + i
            q["section_index"] = 2
            verbal_1_qs.append(q)

        # Build Section 3: Quant 1 (12 Qs)
        quant_1_qs = []
        for i in range(12):
            q = InfiniteQuestionEngine.generate_gre_quant()
            q["id"] = 2000 + i
            q["section_index"] = 3
            quant_1_qs.append(q)

        # Build Section 4: Verbal 2 (15 Qs)
        verbal_2_qs = []
        for i in range(15):
            q = InfiniteQuestionEngine.generate_gre_verbal()
            q["id"] = 3000 + i
            q["section_index"] = 4
            verbal_2_qs.append(q)

        # Build Section 5: Quant 2 (15 Qs)
        quant_2_qs = []
        for i in range(15):
            q = InfiniteQuestionEngine.generate_gre_quant()
            q["id"] = 4000 + i
            q["section_index"] = 5
            quant_2_qs.append(q)

        sections = [
            {
                "section_number": 1,
                "title": "Analytical Writing: Analyze an Issue",
                "type": "awa",
                "duration_seconds": 1800,  # 30 mins
                "duration_minutes": 30,
                "calculator_allowed": False,
                "prompt": awa_choice
            },
            {
                "section_number": 2,
                "title": "Verbal Reasoning – Section 1",
                "type": "verbal",
                "duration_seconds": 1080,  # 18 mins
                "duration_minutes": 18,
                "calculator_allowed": False,
                "total_questions": 12,
                "questions": verbal_1_qs
            },
            {
                "section_number": 3,
                "title": "Quantitative Reasoning – Section 1",
                "type": "quant",
                "duration_seconds": 1260,  # 21 mins
                "duration_minutes": 21,
                "calculator_allowed": True,
                "total_questions": 12,
                "questions": quant_1_qs
            },
            {
                "section_number": 4,
                "title": "Verbal Reasoning – Section 2",
                "type": "verbal",
                "duration_seconds": 1380,  # 23 mins
                "duration_minutes": 23,
                "calculator_allowed": False,
                "total_questions": 15,
                "questions": verbal_2_qs
            },
            {
                "section_number": 5,
                "title": "Quantitative Reasoning – Section 2",
                "type": "quant",
                "duration_seconds": 1560,  # 26 mins
                "duration_minutes": 26,
                "calculator_allowed": True,
                "total_questions": 15,
                "questions": quant_2_qs
            }
        ]

        total_questions = 12 + 12 + 15 + 15  # 54 questions + 1 AWA essay
        total_duration = 30 + 18 + 21 + 23 + 26  # 118 mins (~1 hour 58 mins)

        return {
            "exam": "gre",
            "format_name": "Official ETS GRE General Test (Current Shorter Format)",
            "total_sections": 5,
            "total_questions": total_questions,
            "total_duration_minutes": total_duration,
            "scoring": {
                "verbal_scale": "130–170",
                "quant_scale": "130–170",
                "awa_scale": "0.0–6.0",
                "total_scale": "260–340"
            },
            "sections": sections
        }

    @staticmethod
    def generate_ielts_mock_test() -> Dict[str, Any]:
        """
        Builds the exact IDP / British Council Computer-Delivered IELTS Simulation:
        - Component 1: Academic Reading (3 Full Passages, 40 Questions total) - 60 mins
        - Component 2: Academic Writing (Task 1 Report + Task 2 Essay) - 60 mins
        - Component 3: Speaking Simulation (Parts 1, 2, 3) - 14 mins
        """
        reading_questions = []
        for i in range(40):
            q = InfiniteQuestionEngine.generate_ielts_reading()
            q["id"] = 5000 + i
            q["question_number"] = i + 1
            if i < 13:
                q["passage_index"] = 1
                q["passage_title"] = "Passage 1: Environmental Adaptations of Extreme Flora and Fauna"
            elif i < 26:
                q["passage_index"] = 2
                q["passage_title"] = "Passage 2: The Evolution of Ancient Agricultural Terracing Systems"
            else:
                q["passage_index"] = 3
                q["passage_title"] = "Passage 3: Neuroplasticity and Cognitive Resilience in Multilingualism"
            reading_questions.append(q)

        writing_package = random.choice(IELTS_WRITING_TASKS)
        speaking_package = random.choice(IELTS_SPEAKING_PARTS)

        components = [
            {
                "component_number": 1,
                "title": "IELTS Academic Reading",
                "type": "reading",
                "duration_seconds": 3600,  # 60 mins
                "duration_minutes": 60,
                "total_questions": 40,
                "passages_count": 3,
                "questions": reading_questions
            },
            {
                "component_number": 2,
                "title": "IELTS Academic Writing",
                "type": "writing",
                "duration_seconds": 3600,  # 60 mins
                "duration_minutes": 60,
                "task_1": writing_package["task_1"],
                "task_2": writing_package["task_2"]
            },
            {
                "component_number": 3,
                "title": "IELTS Speaking Simulation",
                "type": "speaking",
                "duration_seconds": 840,   # 14 mins
                "duration_minutes": 14,
                "parts": speaking_package
            }
        ]

        return {
            "exam": "ielts",
            "format_name": "Official IDP / British Council Computer-Delivered IELTS",
            "total_components": 3,
            "total_reading_questions": 40,
            "total_duration_minutes": 134,
            "scoring": {
                "reading_band": "0.0–9.0",
                "writing_band": "0.0–9.0",
                "speaking_band": "0.0–9.0",
                "overall_band": "0.0–9.0"
            },
            "components": components
        }
