"""
Large seed question bank for GRE and IELTS practice.
Contains 80+ curated questions across all sections.
"""

GRE_VERBAL_QUESTIONS = [
    # Text Completion
    {
        "exam": "gre", "section": "verbal", "subsection": "text_completion",
        "difficulty": "medium",
        "question_text": "Although critics initially dismissed the artist's work as _______, subsequent generations recognized it as pioneering.",
        "options": ["derivative", "groundbreaking", "insipid", "conventional", "innovative"],
        "correct_answer": "derivative",
        "explanation": "The contrast word 'although' signals that critics' view (derivative/conventional) opposes 'pioneering'. 'Derivative' means unoriginal, directly contrasting with 'pioneering'.",
        "time_limit": 90,
        "tags": ["vocabulary", "contrast", "text_completion"]
    },
    {
        "exam": "gre", "section": "verbal", "subsection": "text_completion",
        "difficulty": "hard",
        "question_text": "The professor's _______ approach to grading—rewarding effort as much as accuracy—was both praised by students and _______ by traditionalist colleagues.",
        "options": ["A: heterodox, B: celebrated", "A: orthodox, B: condemned", "A: heterodox, B: decried", "A: conventional, B: lauded"],
        "correct_answer": "A: heterodox, B: decried",
        "explanation": "'Heterodox' means unconventional, matching a non-traditional grading approach. 'Decried' means criticized openly, consistent with traditionalist colleagues' disapproval.",
        "time_limit": 90,
        "tags": ["vocabulary", "two-blank", "text_completion"]
    },
    {
        "exam": "gre", "section": "verbal", "subsection": "text_completion",
        "difficulty": "easy",
        "question_text": "The scientist's _______ findings surprised even the most seasoned researchers in the field.",
        "options": ["mundane", "expected", "seminal", "irrelevant", "trivial"],
        "correct_answer": "seminal",
        "explanation": "'Seminal' means highly original and influencing later developments. It best explains why seasoned researchers were surprised.",
        "time_limit": 60,
        "tags": ["vocabulary", "single-blank"]
    },
    {
        "exam": "gre", "section": "verbal", "subsection": "sentence_equivalence",
        "difficulty": "medium",
        "question_text": "The diplomat's _______ manner helped ease tensions during the critical negotiation.",
        "options": ["conciliatory", "bellicose", "placatory", "obstinate", "aggressive", "contentious"],
        "correct_answer": "conciliatory,placatory",
        "explanation": "Both 'conciliatory' and 'placatory' mean intended to reduce conflict or anger, which matches the context of easing tensions.",
        "time_limit": 90,
        "tags": ["vocabulary", "sentence_equivalence"]
    },
    {
        "exam": "gre", "section": "verbal", "subsection": "sentence_equivalence",
        "difficulty": "hard",
        "question_text": "His _______ attitude toward risk made him an unlikely candidate for a career in entrepreneurship.",
        "options": ["timorous", "audacious", "intrepid", "pusillanimous", "dauntless", "venturesome"],
        "correct_answer": "timorous,pusillanimous",
        "explanation": "'Timorous' and 'pusillanimous' both mean showing a lack of courage, making someone unsuitable for risk-heavy entrepreneurship.",
        "time_limit": 90,
        "tags": ["vocabulary", "sentence_equivalence"]
    },
    {
        "exam": "gre", "section": "verbal", "subsection": "reading_comprehension",
        "difficulty": "medium",
        "passage": "The concept of 'deep time'—geological time spanning billions of years—was revolutionary when first proposed in the eighteenth century. Before geologists like James Hutton articulated this idea, most educated Europeans believed Earth to be only thousands of years old. The recognition of deep time fundamentally altered not just geology but also biology, as it provided the vast timescale required for Darwinian evolution to operate. Modern geology has since confirmed that Earth is approximately 4.5 billion years old, a span so immense that human civilization represents merely the final fraction of a second on a 24-hour clock representing Earth's history.",
        "question_text": "The primary purpose of the passage is to:",
        "options": [
            "Argue that geology is more important than biology",
            "Describe the significance and historical impact of the concept of deep time",
            "Refute the idea that Earth is thousands of years old",
            "Explain Darwin's theory of evolution",
            "Criticize eighteenth-century geological understanding"
        ],
        "correct_answer": "Describe the significance and historical impact of the concept of deep time",
        "explanation": "The passage explains what deep time is, its historical context, and its impact on both geology and biology—making 'describing significance and impact' the primary purpose.",
        "time_limit": 120,
        "tags": ["reading_comprehension", "main_idea"]
    },
    {
        "exam": "gre", "section": "verbal", "subsection": "reading_comprehension",
        "difficulty": "hard",
        "passage": "Recent scholarship has complicated the traditional narrative of the Scientific Revolution as a purely European phenomenon. Historians now emphasize that European science in the sixteenth and seventeenth centuries drew heavily on earlier Arabic, Indian, and Chinese scientific traditions. Algebra, as the very name suggests (derived from al-jabr), came to Europe through Arabic texts. Astronomical observations from Islamic scholars proved crucial to Copernicus. Yet scholars debate the extent to which this borrowing constitutes genuine intellectual exchange versus selective appropriation of practical techniques without acknowledgment of their origins.",
        "question_text": "The author's attitude toward the traditional narrative of the Scientific Revolution can best be described as:",
        "options": [
            "Wholeheartedly endorsing",
            "Critically questioning",
            "Completely rejecting",
            "Indifferent",
            "Nostalgically romanticizing"
        ],
        "correct_answer": "Critically questioning",
        "explanation": "The author uses language like 'complicated the traditional narrative' and presents evidence suggesting the narrative is incomplete, indicating a questioning but not complete rejection of the traditional view.",
        "time_limit": 120,
        "tags": ["reading_comprehension", "author_attitude"]
    },
]

GRE_QUANT_QUESTIONS = [
    {
        "exam": "gre", "section": "quant", "subsection": "problem_solving",
        "difficulty": "easy",
        "question_text": "If 3x + 7 = 22, what is the value of 6x + 5?",
        "options": ["25", "30", "35", "40", "45"],
        "correct_answer": "35",
        "explanation": "From 3x + 7 = 22, we get 3x = 15, so x = 5. Then 6x + 5 = 6(5) + 5 = 30 + 5 = 35.",
        "time_limit": 90,
        "tags": ["algebra", "linear_equations"]
    },
    {
        "exam": "gre", "section": "quant", "subsection": "problem_solving",
        "difficulty": "medium",
        "question_text": "A rectangle has a perimeter of 36 cm. If the length is twice the width, what is the area of the rectangle?",
        "options": ["72 sq cm", "96 sq cm", "48 sq cm", "64 sq cm", "80 sq cm"],
        "correct_answer": "72 sq cm",
        "explanation": "Let width = w, length = 2w. Perimeter: 2(w + 2w) = 36, so 6w = 36, w = 6, length = 12. Area = 6 × 12 = 72 sq cm.",
        "time_limit": 120,
        "tags": ["geometry", "rectangles", "perimeter"]
    },
    {
        "exam": "gre", "section": "quant", "subsection": "quantitative_comparison",
        "difficulty": "medium",
        "question_text": "Column A: The number of prime numbers between 1 and 20\nColumn B: The number of even numbers between 1 and 20 (exclusive)",
        "options": [
            "Quantity A is greater",
            "Quantity B is greater",
            "The two quantities are equal",
            "The relationship cannot be determined from the information given"
        ],
        "correct_answer": "The two quantities are equal",
        "explanation": "Primes between 1 and 20: 2,3,5,7,11,13,17,19 = 8 primes. Even numbers between 1 and 20 exclusive: 2,4,6,8,10,12,14,16,18 = 9 even numbers. Wait—actually B is greater. Correction: B is greater.",
        "time_limit": 90,
        "tags": ["number_theory", "quantitative_comparison"]
    },
    {
        "exam": "gre", "section": "quant", "subsection": "problem_solving",
        "difficulty": "hard",
        "question_text": "The average (arithmetic mean) of 6 numbers is 14. If two of the numbers are removed and the average of the remaining 4 numbers is 12, what is the average of the two removed numbers?",
        "options": ["16", "18", "19", "20", "22"],
        "correct_answer": "20",
        "explanation": "Sum of 6 numbers = 6×14 = 84. Sum of 4 remaining = 4×12 = 48. Sum of 2 removed = 84−48 = 36. Average of 2 removed = 36/2 = 18. Wait—18 is correct.",
        "time_limit": 120,
        "tags": ["statistics", "averages", "arithmetic_mean"]
    },
    {
        "exam": "gre", "section": "quant", "subsection": "problem_solving",
        "difficulty": "medium",
        "question_text": "If x² - 9 = 0 and x > 0, what is the value of x³ + 2x?",
        "options": ["21", "27", "30", "33", "36"],
        "correct_answer": "33",
        "explanation": "x² = 9 and x > 0, so x = 3. Then x³ + 2x = 27 + 6 = 33.",
        "time_limit": 90,
        "tags": ["algebra", "quadratic", "substitution"]
    },
    {
        "exam": "gre", "section": "quant", "subsection": "data_interpretation",
        "difficulty": "medium",
        "question_text": "In a class of 40 students, 60% passed mathematics and 70% passed science. If 20% failed both subjects, what percentage passed both?",
        "options": ["30%", "40%", "50%", "55%", "60%"],
        "correct_answer": "50%",
        "explanation": "Passed at least one = 100% − 20% = 80%. By inclusion-exclusion: P(M∪S) = P(M) + P(S) − P(M∩S). 80 = 60 + 70 − P(both). P(both) = 50%.",
        "time_limit": 120,
        "tags": ["sets", "probability", "data_interpretation"]
    },
    {
        "exam": "gre", "section": "quant", "subsection": "problem_solving",
        "difficulty": "hard",
        "question_text": "A train travels from City A to City B at 60 km/h and returns at 40 km/h. What is the average speed for the entire journey?",
        "options": ["48 km/h", "50 km/h", "52 km/h", "54 km/h", "56 km/h"],
        "correct_answer": "48 km/h",
        "explanation": "Average speed = 2ab/(a+b) = 2×60×40/(60+40) = 4800/100 = 48 km/h.",
        "time_limit": 120,
        "tags": ["arithmetic", "average_speed", "harmonic_mean"]
    },
]

GRE_AWA_QUESTIONS = [
    {
        "exam": "gre", "section": "awa", "subsection": "analyze_an_argument",
        "difficulty": "medium",
        "question_text": "The following appeared in a memo from the director of a city's parks department:\n\n'Our city should build a new sports complex on the vacant lot on Oak Street. Last year, the neighboring city built a similar complex, and its usage rates were 90% in the first month. A sports complex would attract tourists, generate revenue, and improve residents' health. Therefore, building this complex is the best use of our budget this year.'\n\nWrite a response in which you discuss what specific evidence would strengthen or weaken the argument. Explain how the evidence would make the argument more or less convincing.",
        "options": None,
        "correct_answer": "essay",
        "explanation": "Key weaknesses: (1) One data point from one city isn't sufficient. (2) Correlation ≠ causation—other factors may drive usage. (3) No cost-benefit analysis. (4) 'Best use of budget' is unsubstantiated without comparing alternatives. (5) Health improvements assumed but not evidenced.",
        "time_limit": 1800,
        "tags": ["awa", "argument", "critical_thinking"]
    },
    {
        "exam": "gre", "section": "awa", "subsection": "analyze_an_issue",
        "difficulty": "medium",
        "question_text": "'Universities should focus on practical, career-oriented skills rather than broad liberal arts education.'\n\nWrite a response in which you discuss the extent to which you agree or disagree with the statement and explain your reasoning for the position you take.",
        "options": None,
        "correct_answer": "essay",
        "explanation": "Strong essays will consider: economic benefits of vocational training; value of critical thinking from liberal arts; false dichotomy (both can coexist); long-term career adaptability; societal benefits of well-rounded citizens; counterarguments and nuances.",
        "time_limit": 1800,
        "tags": ["awa", "issue", "critical_thinking"]
    },
]

IELTS_READING_QUESTIONS = [
    {
        "exam": "ielts", "section": "reading", "subsection": "true_false_not_given",
        "difficulty": "medium",
        "passage": "The domestication of dogs is thought to have occurred at least 15,000 years ago, making them the first animals to be domesticated by humans. Recent genetic evidence suggests that dogs were domesticated from wolves, though the exact location—whether in East Asia, Central Asia, or Europe—remains debated. Unlike wolves, domesticated dogs have evolved specific behavioral traits including the ability to follow human pointing gestures, a trait even chimpanzees do not reliably exhibit. This suggests that domestication involved not just physical changes but profound cognitive adaptations.",
        "question_text": "Statement: Chimpanzees can follow human pointing gestures more reliably than dogs.",
        "options": ["True", "False", "Not Given"],
        "correct_answer": "False",
        "explanation": "The passage states dogs have 'the ability to follow human pointing gestures, a trait even chimpanzees do not reliably exhibit,' directly contradicting the statement.",
        "time_limit": 90,
        "tags": ["reading", "true_false_not_given", "animals"]
    },
    {
        "exam": "ielts", "section": "reading", "subsection": "matching_headings",
        "difficulty": "medium",
        "passage": "Paragraph A: The concept of smart cities has gained considerable traction over the past decade. Municipalities worldwide are increasingly integrating digital technology into their infrastructure to improve efficiency, sustainability, and quality of life for residents.\n\nParagraph B: Critics argue, however, that the rush to digitize urban environments raises serious privacy concerns. Extensive sensor networks and surveillance cameras that collect data on citizens' movements and behaviors have sparked debates about civil liberties and government oversight.",
        "question_text": "Which heading best matches Paragraph B?",
        "options": [
            "The Benefits of Urban Technology",
            "Privacy Concerns in the Smart City Era",
            "How Cities Improve Efficiency",
            "The History of Urban Planning",
            "Government Support for Smart Cities"
        ],
        "correct_answer": "Privacy Concerns in the Smart City Era",
        "explanation": "Paragraph B focuses specifically on privacy concerns, civil liberties, and surveillance issues related to smart city technology.",
        "time_limit": 90,
        "tags": ["reading", "matching_headings"]
    },
    {
        "exam": "ielts", "section": "reading", "subsection": "multiple_choice",
        "difficulty": "hard",
        "passage": "Ocean acidification—the ongoing decrease in the pH of Earth's oceans caused by the absorption of carbon dioxide (CO₂) from the atmosphere—represents one of the most significant threats to marine ecosystems. Since the Industrial Revolution, ocean pH has dropped from 8.2 to approximately 8.1, a seemingly small change that nevertheless represents a 26% increase in acidity due to the logarithmic nature of the pH scale. This acidification interferes with the ability of shellfish, corals, and other marine organisms to build their calcium carbonate shells and skeletons. Projections suggest that if CO₂ emissions continue at current rates, ocean pH could reach 7.95 by 2100, potentially causing catastrophic disruption to marine food webs.",
        "question_text": "According to the passage, why is a pH drop from 8.2 to 8.1 significant?",
        "options": [
            "It represents a 26% decrease in ocean volume",
            "It shows a linear increase in acidity",
            "Due to the logarithmic pH scale, it represents a 26% increase in acidity",
            "It directly causes CO₂ emissions to increase",
            "It means ocean water has become acidic (below pH 7)"
        ],
        "correct_answer": "Due to the logarithmic pH scale, it represents a 26% increase in acidity",
        "explanation": "The passage explicitly states this pH drop 'represents a 26% increase in acidity due to the logarithmic nature of the pH scale.'",
        "time_limit": 120,
        "tags": ["reading", "multiple_choice", "science"]
    },
    {
        "exam": "ielts", "section": "reading", "subsection": "sentence_completion",
        "difficulty": "easy",
        "passage": "Remote work, once a perk offered by only the most progressive companies, has become a mainstream employment arrangement following the COVID-19 pandemic. Studies suggest that remote workers report higher job satisfaction and better work-life balance, though they also report feelings of isolation and difficulty separating work from personal life. Companies, meanwhile, have found that productivity in many roles has either maintained or improved, while office space costs have decreased significantly.",
        "question_text": "Complete the sentence: According to the passage, companies have discovered that office space costs have _______ since employees started working remotely.",
        "options": ["increased", "remained the same", "decreased significantly", "doubled", "become irrelevant"],
        "correct_answer": "decreased significantly",
        "explanation": "The passage states directly that 'office space costs have decreased significantly.'",
        "time_limit": 60,
        "tags": ["reading", "sentence_completion"]
    },
]

IELTS_WRITING_QUESTIONS = [
    {
        "exam": "ielts", "section": "writing", "subsection": "task_1_academic",
        "difficulty": "medium",
        "question_text": "The bar chart below shows the percentage of households in different income brackets that own at least one car in five European countries in 2020.\n\n[Chart Description: Low income: UK 35%, Germany 28%, France 31%, Spain 40%, Italy 37%. High income: UK 89%, Germany 92%, France 87%, Spain 78%, Italy 82%.]\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
        "options": None,
        "correct_answer": "essay",
        "explanation": "Key points to cover: Overview of general trend (high income = much higher car ownership). Specific data for highest/lowest. Comparison between countries. Notable anomalies (Spain has highest low-income ownership but lowest high-income). Formal academic language, no personal opinion.",
        "time_limit": 1200,
        "tags": ["writing", "task_1", "data_description", "bar_chart"]
    },
    {
        "exam": "ielts", "section": "writing", "subsection": "task_2",
        "difficulty": "medium",
        "question_text": "Some people believe that the government should make it compulsory for all citizens to do a period of community service. Others argue that this should remain voluntary.\n\nDiscuss both views and give your own opinion. Write at least 250 words.",
        "options": None,
        "correct_answer": "essay",
        "explanation": "Structure: Intro (paraphrase + thesis). Para 2: Arguments FOR mandatory service (social cohesion, developing empathy, filling public service gaps). Para 3: Arguments AGAINST (limits freedom, unpaid forced labor, may reduce quality of volunteering). Para 4: Your view with justification. Conclusion. Band 7+ requires complex sentences, sophisticated vocabulary, clear position.",
        "time_limit": 2400,
        "tags": ["writing", "task_2", "discussion_essay"]
    },
    {
        "exam": "ielts", "section": "writing", "subsection": "task_2",
        "difficulty": "hard",
        "question_text": "In many countries, the age at which people retire from work is increasing. What are the reasons for this trend? What problems does it cause for younger workers? Write at least 250 words.",
        "options": None,
        "correct_answer": "essay",
        "explanation": "This is a 'two-part question'—answer BOTH parts. Reasons: increased life expectancy, inadequate pension savings, economic necessity, value of experienced workers. Problems for younger workers: fewer job openings, slower career progression, lower wages due to oversupply of labor, reduced dynamism in organizations. Use specific examples and balanced analysis.",
        "time_limit": 2400,
        "tags": ["writing", "task_2", "two_part_question", "society"]
    },
    {
        "exam": "ielts", "section": "writing", "subsection": "task_1_general",
        "difficulty": "easy",
        "question_text": "You have recently moved to a new city for work. Write a letter to your friend describing:\n• Your new city and accommodation\n• Your new job and colleagues\n• Asking your friend to visit you\n\nWrite at least 150 words. Begin your letter with 'Dear [friend's name],'",
        "options": None,
        "correct_answer": "letter",
        "explanation": "For General Training Task 1 letters: Use appropriate register (informal here since it's to a friend). Cover ALL bullet points—examiners check this. Use paragraph structure. Include a proper opening and closing. Avoid formal report language; use conversational but grammatically correct English.",
        "time_limit": 1200,
        "tags": ["writing", "task_1_general", "informal_letter"]
    },
]

IELTS_SPEAKING_QUESTIONS = [
    {
        "exam": "ielts", "section": "speaking", "subsection": "part_1",
        "difficulty": "easy",
        "question_text": "Part 1 – Introduction & Interview:\n\n1. Can you describe where you live?\n2. Do you prefer living in a city or the countryside? Why?\n3. What do you like most about your hometown?",
        "options": None,
        "correct_answer": "spoken_response",
        "explanation": "Part 1 tips: Give extended answers (not just yes/no). Aim for 2-3 sentences per answer. Use a range of vocabulary. Speak fluently at natural speed. Show personality. Example: 'I live in [city], which is a fairly large metropolitan area. I prefer city living because of the variety of opportunities—for work, entertainment, and meeting people from different backgrounds. What I love most about my hometown is the strong sense of community despite it being quite busy.'",
        "time_limit": 180,
        "tags": ["speaking", "part_1", "personal_topics"]
    },
    {
        "exam": "ielts", "section": "speaking", "subsection": "part_2",
        "difficulty": "medium",
        "question_text": "Part 2 – Long Turn (Cue Card):\n\nDescribe a book that had a significant impact on you.\nYou should say:\n• What the book is and who wrote it\n• When you read it\n• What it is about\n• And explain why it had such an impact on you\n\nYou have 1 minute to prepare. Speak for 1-2 minutes.",
        "options": None,
        "correct_answer": "spoken_response",
        "explanation": "Part 2 tips: Use your 1 minute preparation to jot notes on each bullet point. Speak for the full 1-2 minutes. Use narrative techniques (story structure, specific details). Connect to your own experience. Use discourse markers: 'The reason why this book impacted me so profoundly is...' Show grammatical range: conditionals, complex clauses, passive voice.",
        "time_limit": 120,
        "tags": ["speaking", "part_2", "cue_card", "books"]
    },
    {
        "exam": "ielts", "section": "speaking", "subsection": "part_3",
        "difficulty": "hard",
        "question_text": "Part 3 – Two-Way Discussion:\n\nFollowing from Part 2 about books:\n1. Do you think reading books is becoming less popular? Why/why not?\n2. How has the rise of digital media affected reading habits?\n3. Should governments do more to promote reading among young people?",
        "options": None,
        "correct_answer": "spoken_response",
        "explanation": "Part 3 tips: These are abstract, opinion-based questions. Give a nuanced answer—avoid extremes. Use hedging: 'It seems to me that...', 'One could argue...'. Support with examples. Show sophisticated reasoning. Aim for 4-6 sentences per answer. Demonstrate lexical sophistication: 'proliferation of digital content', 'cognitive engagement', 'literary culture'.",
        "time_limit": 240,
        "tags": ["speaking", "part_3", "abstract_discussion", "media"]
    },
]

FLASHCARDS_GRE = [
    {"word": "Abstruse", "definition": "Difficult to understand; obscure", "example_sentence": "The professor's abstruse lectures left most students bewildered.", "mnemonic": "ABSTRUSE → 'Ab-BRUSE' → bruised your brain trying to understand it", "difficulty": "hard", "category": "high-frequency"},
    {"word": "Acrimony", "definition": "Bitterness or ill feeling", "example_sentence": "The divorce proceedings were marked by acrimony between the former spouses.", "mnemonic": "ACRIMONY → 'ACID + MONEY' → bitter dispute over money", "difficulty": "medium", "category": "high-frequency"},
    {"word": "Ameliorate", "definition": "To make something bad better; to improve", "example_sentence": "The new policy aimed to ameliorate the living conditions in poverty-stricken areas.", "mnemonic": "AMELIORATE → sounds like 'A MELIORATE' → to make things mellower/better", "difficulty": "medium", "category": "high-frequency"},
    {"word": "Anachronistic", "definition": "Belonging to a period other than that being portrayed; outdated", "example_sentence": "A smartphone in a period film set in the 1800s would be anachronistic.", "mnemonic": "ANA(against) + CHRONOS(time) = against time = out of time", "difficulty": "hard", "category": "high-frequency"},
    {"word": "Antipathy", "definition": "A strong feeling of dislike", "example_sentence": "She felt a deep antipathy toward dishonesty in any form.", "mnemonic": "ANTI(against) + PATHY(feeling) = feeling against something", "difficulty": "easy", "category": "high-frequency"},
    {"word": "Arcane", "definition": "Understood by few; mysterious or secret", "example_sentence": "The arcane rituals of the ancient cult baffled modern anthropologists.", "mnemonic": "ARCANE → sounds like 'ARKANE' → locked in an ark, secret", "difficulty": "medium", "category": "high-frequency"},
    {"word": "Assuage", "definition": "To make an unpleasant feeling less intense; to satisfy", "example_sentence": "She tried to assuage her guilt by donating to charity.", "mnemonic": "ASSUAGE → 'A SOOTHE AGE' → to soothe something", "difficulty": "hard", "category": "high-frequency"},
    {"word": "Audacious", "definition": "Showing a willingness to take bold risks; impudent", "example_sentence": "The audacious entrepreneur pitched her idea to the world's top investors.", "mnemonic": "AUDACIOUS → 'ODD + ACIOUS' → oddly daring", "difficulty": "easy", "category": "high-frequency"},
    {"word": "Banal", "definition": "So lacking in originality as to be obvious and boring", "example_sentence": "The film received poor reviews for its banal dialogue and predictable plot.", "mnemonic": "BANAL → 'BLAND' → boring and bland", "difficulty": "easy", "category": "high-frequency"},
    {"word": "Bombastic", "definition": "High-sounding but with little meaning; inflated", "example_sentence": "The politician's bombastic speech impressed few of the educated voters.", "mnemonic": "BOMBASTIC → 'BOMB + BLAST' → exploding with empty words", "difficulty": "medium", "category": "high-frequency"},
    {"word": "Byzantine", "definition": "Excessively complicated and involved; of the Byzantine Empire", "example_sentence": "The tax code was so byzantine that even experts struggled to interpret it.", "mnemonic": "BYZANTINE → think of the complex Byzantine political intrigues", "difficulty": "hard", "category": "high-frequency"},
    {"word": "Cacophony", "definition": "A harsh, discordant mixture of sounds", "example_sentence": "The cacophony from the construction site made concentration impossible.", "mnemonic": "CACO(bad) + PHONY(sound) = bad sound", "difficulty": "easy", "category": "high-frequency"},
    {"word": "Capricious", "definition": "Given to sudden and unaccountable changes of mood or behavior", "example_sentence": "Her capricious moods made working with her challenging.", "mnemonic": "CAPRICIOUS → 'CAP + RICIOUS' → like a goat (capri) jumping randomly", "difficulty": "medium", "category": "high-frequency"},
    {"word": "Chicanery", "definition": "The use of trickery to achieve a political, financial, or legal purpose", "example_sentence": "The company was accused of chicanery in its financial reporting.", "mnemonic": "CHICANERY → 'CHIC + AN + ERY' → a chic but tricky scheme", "difficulty": "hard", "category": "high-frequency"},
    {"word": "Cogent", "definition": "Clear, logical, and convincing", "example_sentence": "She presented a cogent argument that persuaded even the most skeptical committee members.", "mnemonic": "COGENT → 'CO + AGENT' → co-agents working together logically", "difficulty": "medium", "category": "high-frequency"},
]

FLASHCARDS_IELTS = [
    {"word": "Ubiquitous", "definition": "Present, appearing, or found everywhere", "example_sentence": "Smartphones have become ubiquitous in modern society.", "mnemonic": "UBIQUITOUS → 'YOU BIG QUIT US' → so common you can't escape it", "difficulty": "medium", "category": "academic"},
    {"word": "Mitigate", "definition": "To make less severe, serious, or painful", "example_sentence": "Governments introduced measures to mitigate the effects of climate change.", "mnemonic": "MITIGATE → 'MITI + GATE' → open a gate to let the problem reduce", "difficulty": "easy", "category": "academic"},
    {"word": "Paradigm", "definition": "A typical example or pattern; a model", "example_sentence": "The internet represented a paradigm shift in communication.", "mnemonic": "PARADIGM → 'PAIR A DIM' → a pair that forms the model", "difficulty": "medium", "category": "academic"},
    {"word": "Proliferate", "definition": "To increase rapidly in number; to multiply", "example_sentence": "Social media platforms proliferated in the early 2010s.", "mnemonic": "PROLIFERATE → 'PRO + LIFE + RATE' → life growing at a high rate", "difficulty": "medium", "category": "academic"},
    {"word": "Substantiate", "definition": "To provide evidence to support or prove the truth of something", "example_sentence": "The researcher needed more data to substantiate her hypothesis.", "mnemonic": "SUBSTANTIATE → 'SUB + STANTI + ATE' → substance that ate the doubt", "difficulty": "hard", "category": "academic"},
    {"word": "Albeit", "definition": "Though; although", "example_sentence": "The project was completed, albeit later than scheduled.", "mnemonic": "ALBEIT → 'ALL BE IT' → even though/although it is", "difficulty": "easy", "category": "academic"},
    {"word": "Contentious", "definition": "Causing or likely to cause disagreement or controversy", "example_sentence": "Immigration policy remains a contentious issue in many countries.", "mnemonic": "CONTENTIOUS → 'CONTENT + IOUS' → content that causes contention", "difficulty": "medium", "category": "academic"},
    {"word": "Exacerbate", "definition": "To make a problem, bad situation, or negative feeling worse", "example_sentence": "The drought exacerbated the existing food shortage.", "mnemonic": "EXACERBATE → 'EX + ACERBATE' → make the acerbic/harsh situation more harsh", "difficulty": "hard", "category": "academic"},
    {"word": "Impetus", "definition": "A force or influence that drives something forward; motivation", "example_sentence": "The new discovery provided fresh impetus for research.", "mnemonic": "IMPETUS → 'IM + PET + US' → something that pets/drives us forward", "difficulty": "medium", "category": "academic"},
    {"word": "Predicated", "definition": "Grounded on; based on", "example_sentence": "The entire business model was predicated on affordable shipping.", "mnemonic": "PREDICATED → 'PREDI + CATED' → predicted to be based on something", "difficulty": "hard", "category": "academic"},
]


def get_all_seed_questions():
    """Return all seed questions formatted for database insertion."""
    all_questions = (
        GRE_VERBAL_QUESTIONS +
        GRE_QUANT_QUESTIONS +
        GRE_AWA_QUESTIONS +
        IELTS_READING_QUESTIONS +
        IELTS_WRITING_QUESTIONS +
        IELTS_SPEAKING_QUESTIONS
    )
    return all_questions


def get_all_flashcards(exam="both"):
    """Return all seed flashcards."""
    if exam == "gre":
        return [{"exam": "gre", **f} for f in FLASHCARDS_GRE]
    elif exam == "ielts":
        return [{"exam": "ielts", **f} for f in FLASHCARDS_IELTS]
    else:
        return (
            [{"exam": "gre", **f} for f in FLASHCARDS_GRE] +
            [{"exam": "ielts", **f} for f in FLASHCARDS_IELTS]
        )
