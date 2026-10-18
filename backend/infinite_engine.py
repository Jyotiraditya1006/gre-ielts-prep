"""
Infinite Question Engine for GRE & IELTS
Procedurally generates millions of unique, mathematically verified, and linguistically accurate questions.
"""
import random
import math
from typing import Dict, Any, List


class InfiniteQuestionEngine:
    """Procedural generator creating virtually infinite realistic GRE and IELTS questions."""

    @staticmethod
    def _safe_options(ans: str, candidates: list, needed: int = 4) -> List[str]:
        ans_str = str(ans).strip()
        unique = []
        for c in candidates:
            c_str = str(c).strip()
            if c_str != ans_str and c_str not in unique:
                unique.append(c_str)
        
        offset = 1
        while len(unique) < needed:
            try:
                base = float(ans_str.replace("$", "").replace(" mph", "").replace(" hours", "").replace("%", "").replace("π", ""))
                c_str = f"{round(base + offset, 1)}"
            except Exception:
                c_str = f"Alt {offset}"
            if c_str != ans_str and c_str not in unique:
                unique.append(c_str)
            offset += 1
            
        selected = random.sample(unique, needed)
        opts = [ans_str] + selected
        random.shuffle(opts)
        return opts

    @staticmethod
    def generate_gre_quant() -> Dict[str, Any]:
        """Generates random GRE Quantitative Reasoning questions with step-by-step solutions."""
        generator_types = [
            InfiniteQuestionEngine._quant_algebra_linear,
            InfiniteQuestionEngine._quant_algebra_quadratic,
            InfiniteQuestionEngine._quant_comparison_algebra,
            InfiniteQuestionEngine._quant_comparison_geometry,
            InfiniteQuestionEngine._quant_word_work_rate,
            InfiniteQuestionEngine._quant_word_speed_distance,
            InfiniteQuestionEngine._quant_word_percentage,
            InfiniteQuestionEngine._quant_geometry_triangle,
            InfiniteQuestionEngine._quant_geometry_circle,
            InfiniteQuestionEngine._quant_probability_combinatorics,
            InfiniteQuestionEngine._quant_statistics_mean_median,
            InfiniteQuestionEngine._quant_number_properties,
        ]
        func = random.choice(generator_types)
        return func()


    @staticmethod
    def _quant_algebra_linear() -> Dict[str, Any]:
        a = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
        x = random.randint(-15, 25)
        b = random.randint(3, 40)
        c = a * x + b
        
        target_multiplier = random.choice([2, 3, 4, -2])
        target_val = target_multiplier * x + random.randint(1, 5)
        
        # Ask for target_multiplier * x + offset
        offset = random.randint(2, 10)
        ans = target_multiplier * x + offset
        
        # Generate 5 options
        options = InfiniteQuestionEngine._safe_options(str(ans), [str(ans + d) for d in [-12, -7, -3, 3, 7, 12, 15]])
        
        q_text = f"If {a}x + {b} = {c}, what is the value of {target_multiplier}x + {offset}?"
        explanation = (
            f"Step 1: Solve for x:\n"
            f"  {a}x + {b} = {c}\n"
            f"  {a}x = {c} - {b} = {c - b}\n"
            f"  x = {c - b} / {a} = {x}\n\n"
            f"Step 2: Calculate the required expression:\n"
            f"  {target_multiplier}({x}) + {offset} = {target_multiplier * x} + {offset} = {ans}."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": random.choice(["easy", "medium"]),
            "question_text": q_text,
            "options": options,
            "correct_answer": str(ans),
            "explanation": explanation,
            "tags": ["algebra", "linear equations", "variables"],
            "time_limit": 90,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_algebra_quadratic() -> Dict[str, Any]:
        r1 = random.randint(2, 9)
        r2 = random.randint(1, 8)
        if r1 == r2:
            r2 += 1
        b_coeff = -(r1 + r2)
        c_coeff = r1 * r2
        sign_b = f"- {abs(b_coeff)}" if b_coeff < 0 else f"+ {b_coeff}"
        
        q_text = f"If x² {sign_b}x + {c_coeff} = 0, which of the following could be the value of x?"
        ans = str(random.choice([r1, r2]))
        
        options = InfiniteQuestionEngine._safe_options(ans, [str(d) for d in [r1 + 2, r2 - 3, -(r1), -(r2), r1 + r2, c_coeff, r1 * 2]])
        
        explanation = (
            f"Factor the quadratic equation x² {sign_b}x + {c_coeff} = 0:\n"
            f"(x - {r1})(x - {r2}) = 0\n"
            f"Hence, roots are x = {r1} and x = {r2}.\n"
            f"Among the options, {ans} is the correct root."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["algebra", "quadratic equations", "factoring"],
            "time_limit": 100,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_comparison_algebra() -> Dict[str, Any]:
        options = [
            "Quantity A is greater.",
            "Quantity B is greater.",
            "The two quantities are equal.",
            "The relationship cannot be determined from the information given."
        ]
        types = [
            # Type 1: x > 1 vs 0 < x < 1
            ("x > 1", "x² + 1", "2x", "Quantity A is greater.", 
             "Since x > 1, (x - 1)² > 0 => x² - 2x + 1 > 0 => x² + 1 > 2x. Thus Quantity A is always strictly greater."),
            # Type 2: -1 < y < 0
            ("-1 < y < 0", "y²", "y³", "Quantity A is greater.", 
             "When -1 < y < 0, y² is positive while y³ is negative. A positive number is always greater than a negative number."),
            # Type 3: x is a non-zero real number
            ("x is a non-zero real number", "x²", "x³", "The relationship cannot be determined from the information given.", 
             "If x = 2: Quantity A = 4, Quantity B = 8 (B is greater).\nIf x = -2: Quantity A = 4, Quantity B = -8 (A is greater).\nBecause the relationship changes depending on whether x is positive or negative, it cannot be determined."),
            # Type 4: Right triangle hypotenuse
            ("A right triangle has legs of length a and b, and hypotenuse c", "(a + b)²", "c²", "Quantity A is greater.",
             "(a + b)² = a² + 2ab + b². By the Pythagorean theorem, a² + b² = c². Since lengths a and b must be positive, 2ab > 0, meaning (a + b)² = c² + 2ab > c²."),
            # Type 5: k > 0
            ("k > 0", "(k + 1)/k", "1 + 1/k", "The two quantities are equal.",
             "(k + 1)/k = k/k + 1/k = 1 + 1/k. Both expressions are identical for any k > 0.")
        ]
        given, col_a, col_b, correct, expl = random.choice(types)
        
        q_text = (
            f"{given}\n\n"
            f"Quantity A: {col_a}\n"
            f"Quantity B: {col_b}"
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "quantitative_comparison",
            "difficulty": "hard" if "cannot" in correct else "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": correct,
            "explanation": expl,
            "tags": ["quantitative comparison", "inequalities", "algebraic reasoning"],
            "time_limit": 105,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_comparison_geometry() -> Dict[str, Any]:
        options = [
            "Quantity A is greater.",
            "Quantity B is greater.",
            "The two quantities are equal.",
            "The relationship cannot be determined from the information given."
        ]
        r = random.choice([4, 5, 6, 7, 8])
        area_circle = round(math.pi * (r ** 2), 2)
        side_square = round(2 * r, 2)
        area_square = side_square ** 2
        
        q_text = (
            f"A circle with radius {r} is inscribed inside a square.\n\n"
            f"Quantity A: Area of the inscribed circle\n"
            f"Quantity B: Area of the square"
        )
        explanation = (
            f"The diameter of the inscribed circle equals the side length of the square: s = 2r = {2*r}.\n"
            f"Quantity A (Circle Area) = πr² = π({r}²) ≈ {area_circle}.\n"
            f"Quantity B (Square Area) = s² = (2r)² = 4r² = {area_square}.\n"
            f"Since π ≈ 3.1416 < 4, πr² is always less than 4r².\n"
            f"Therefore, Quantity B is greater."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "quantitative_comparison",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": "Quantity B is greater.",
            "explanation": explanation,
            "tags": ["quantitative comparison", "geometry", "circles", "inscribed figures"],
            "time_limit": 90,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_word_work_rate() -> Dict[str, Any]:
        time_a = random.choice([3, 4, 6, 8, 10, 12])
        time_b = random.choice([6, 8, 12, 15, 20])
        numerator = time_a * time_b
        denominator = time_a + time_b
        combined = round(numerator / denominator, 2)
        ans = f"{combined} hours"
        
        options = InfiniteQuestionEngine._safe_options(ans, [
            f"{round((time_a + time_b)/2, 2)} hours",
            f"{round(abs(time_a - time_b), 2)} hours",
            f"{round(combined * 1.5, 2)} hours",
            f"{round(combined * 0.75, 2)} hours",
            f"{time_a + time_b} hours",
            f"{round(combined + 1.5, 2)} hours"
        ])
        
        q_text = (
            f"Worker P can complete a construction project in {time_a} hours, while Worker Q "
            f"takes {time_b} hours to complete the same project. If both workers work together at their "
            f"constant rates, approximately how many hours will it take to finish the project?"
        )
        explanation = (
            f"Rate of Worker P = 1/{time_a} project/hr.\n"
            f"Rate of Worker Q = 1/{time_b} project/hr.\n"
            f"Combined Rate = 1/{time_a} + 1/{time_b} = ({time_a} + {time_b}) / ({time_a} × {time_b}) = {denominator} / {numerator}.\n"
            f"Time taken = 1 / Combined Rate = {numerator} / {denominator} ≈ {combined} hours."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["word problems", "work and rate", "fractions"],
            "time_limit": 110,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_word_speed_distance() -> Dict[str, Any]:
        speed1 = random.choice([40, 50, 60])
        speed2 = random.choice([60, 75, 90])
        distance = speed1 * random.choice([2, 3])
        avg_speed = round((2 * speed1 * speed2) / (speed1 + speed2), 1)
        ans = f"{avg_speed} mph"
        
        simple_avg = round((speed1 + speed2) / 2, 1)
        options = InfiniteQuestionEngine._safe_options(ans, [
            f"{simple_avg} mph",
            f"{round(avg_speed + 4.5, 1)} mph",
            f"{round(avg_speed - 5.2, 1)} mph",
            f"{speed1} mph",
            f"{speed2} mph",
            f"{round(avg_speed + 8.0, 1)} mph"
        ])
        
        q_text = (
            f"A commuter drives to work at an average speed of {speed1} mph and returns along the same route "
            f"at an average speed of {speed2} mph. What is the driver's average speed for the entire round trip?"
        )
        explanation = (
            f"Average Speed = Total Distance / Total Time.\n"
            f"Let one-way distance be D. Total distance = 2D.\n"
            f"Time to work = D/{speed1}, Time back = D/{speed2}.\n"
            f"Total time = D(1/{speed1} + 1/{speed2}) = D({speed1 + speed2}) / ({speed1 * speed2}).\n"
            f"Average speed = 2D / Total Time = 2 × {speed1} × {speed2} / ({speed1} + {speed2}) = {2 * speed1 * speed2} / {speed1 + speed2} ≈ {avg_speed} mph.\n"
            f"Note: It is NOT the simple arithmetic average of {speed1} and {speed2} ({simple_avg} mph) because more time is spent at the slower speed."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "hard",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["word problems", "average speed", "distance and time"],
            "time_limit": 120,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_word_percentage() -> Dict[str, Any]:
        p_inc = random.choice([10, 20, 25, 30])
        p_dec = random.choice([10, 20, 25, 30])
        net_factor = (1 + p_inc / 100.0) * (1 - p_dec / 100.0)
        net_pct = round((net_factor - 1.0) * 100, 1)
        
        if net_pct < 0:
            ans = f"{abs(net_pct)}% decrease"
        elif net_pct > 0:
            ans = f"{net_pct}% increase"
        else:
            ans = "No change (0%)"
            
        options = InfiniteQuestionEngine._safe_options(ans, [
            f"{abs(p_inc - p_dec)}% increase",
            f"{abs(p_inc - p_dec)}% decrease",
            f"{p_inc + p_dec}% decrease",
            f"{abs(net_pct) + 5}% decrease",
            f"{abs(net_pct) + 2.5}% increase",
            "No change (0%)"
        ])
        
        q_text = (
            f"The price of a tech stock increased by {p_inc}% in January, and then decreased by {p_dec}% in February. "
            f"What was the net percentage change in the stock price over the two-month period?"
        )
        explanation = (
            f"Let the initial price be P.\n"
            f"Price after January = P × (1 + {p_inc}/100) = {1 + p_inc/100:.2f} P.\n"
            f"Price after February = ({1 + p_inc/100:.2f} P) × (1 - {p_dec}/100) = {net_factor:.4f} P.\n"
            f"Net change = ({net_factor:.4f} - 1) × 100% = {net_pct}%.\n"
            f"Result: {ans}."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["percentages", "successive percentage change", "financial math"],
            "time_limit": 90,
            "is_ai_generated": False
        }


    @staticmethod
    def _quant_geometry_triangle() -> Dict[str, Any]:
        # Pythagorean triples: 3-4-5, 5-12-13, 8-15-17, 7-24-25, 9-40-41
        triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15)]
        a, b, c = random.choice(triples)
        multiplier = random.choice([1, 2, 3])
        leg1, leg2, hyp = a * multiplier, b * multiplier, c * multiplier
        
        area = (leg1 * leg2) // 2
        ans = str(area)
        options = InfiniteQuestionEngine._safe_options(ans, [str(d) for d in [leg1 * leg2, leg1 + leg2 + hyp, area + leg1, area - 4, (hyp * leg1) // 2, area + 8, area + 14]])
        
        q_text = (
            f"In a right triangle, one leg has length {leg1} and the hypotenuse has length {hyp}. "
            f"What is the area of the triangle?"
        )
        explanation = (
            f"Step 1: Find the other leg using the Pythagorean theorem:\n"
            f"  leg² = {hyp}² - {leg1}² = {hyp**2} - {leg1**2} = {leg2**2}\n"
            f"  other leg = {leg2}\n\n"
            f"Step 2: Area = (base × height) / 2 = ({leg1} × {leg2}) / 2 = {area}."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["geometry", "triangles", "Pythagorean theorem", "area"],
            "time_limit": 90,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_geometry_circle() -> Dict[str, Any]:
        radius = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
        angle = random.choice([30, 45, 60, 90, 120])
        gcd_val = math.gcd(radius * angle, 180)
        num = (radius * angle) // gcd_val
        den = 180 // gcd_val
        
        if den == 1:
            ans = f"{num}π"
        else:
            ans = f"({num}π)/{den}"
            
        options = InfiniteQuestionEngine._safe_options(ans, [
            f"{num + 1}π" if den == 1 else f"({num + 1}π)/{den}",
            f"{radius}π",
            f"({radius**2}π)/{den}",
            f"{2 * num}π",
            f"({num}π)/{den + 1}",
            f"{num + 3}π"
        ])
        
        q_text = (
            f"A circle has a radius of {radius}. What is the length of an arc subtended by a central angle of {angle}°?"
        )
        explanation = (
            f"Arc length formula: s = 2πr × (θ / 360°) = πr × (θ / 180°)\n"
            f"s = π({radius}) × ({angle} / 180) = ({radius * angle} / 180)π = {ans}."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["geometry", "circles", "arc length", "angles"],
            "time_limit": 90,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_probability_combinatorics() -> Dict[str, Any]:
        n = random.choice([6, 7, 8, 9, 10])
        r = random.choice([2, 3])
        ans_num = math.comb(n, r)
        ans = str(ans_num)
        
        options = InfiniteQuestionEngine._safe_options(ans, [str(d) for d in [math.perm(n, r), ans_num + 5, ans_num - 3, ans_num * 2, math.comb(n - 1, r), ans_num + 10]])
        
        q_text = (
            f"A research committee of {r} members is to be selected from a department consisting of {n} professors. "
            f"How many distinct committees can be formed?"
        )
        explanation = (
            f"Since the order of committee members does not matter, this is a combination problem:\n"
            f"C(n, r) = n! / (r! × (n - r)!)\n"
            f"C({n}, {r}) = {n}! / ({r}! × {n - r}!) = {ans_num} distinct committees."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "medium",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["combinatorics", "combinations", "probability"],
            "time_limit": 90,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_statistics_mean_median() -> Dict[str, Any]:
        nums = sorted([random.randint(10, 45) for _ in range(7)])
        mean_val = round(sum(nums) / len(nums), 1)
        median_val = nums[3]
        range_val = nums[-1] - nums[0]
        
        q_type = random.choice(["mean", "median", "range"])
        if q_type == "mean":
            ans = str(mean_val)
            candidates = [str(round(mean_val + d, 1)) for d in [-3.2, -1.5, 2.1, 4.0, 5.5, -4.0]]
            target = "arithmetic mean"
            step = f"Sum = {' + '.join(map(str, nums))} = {sum(nums)}. Mean = {sum(nums)} / 7 ≈ {mean_val}."
        elif q_type == "median":
            ans = str(median_val)
            candidates = [str(d) for d in [nums[2], nums[4], nums[3] + 2, nums[3] - 3, nums[1], nums[5]]]
            target = "median"
            step = f"With 7 ordered values: {nums}, the median is the 4th element: {median_val}."
        else:
            ans = str(range_val)
            candidates = [str(range_val + d) for d in [-5, -2, 3, 7, 9, -4]]
            target = "range"
            step = f"Range = Maximum - Minimum = {nums[-1]} - {nums[0]} = {range_val}."
            
        options = InfiniteQuestionEngine._safe_options(ans, candidates)
        
        shuffled_display = list(nums)
        random.shuffle(shuffled_display)
        
        q_text = f"Consider the following set of test scores: {', '.join(map(str, shuffled_display))}. What is the {target} of this dataset?"
        explanation = f"Arrange scores in ascending order: {nums}.\n{step}"
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "data_interpretation",
            "difficulty": "easy",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["statistics", "mean", "median", "range"],
            "time_limit": 75,
            "is_ai_generated": False
        }

    @staticmethod
    def _quant_number_properties() -> Dict[str, Any]:
        n = random.randint(120, 480)
        temp = n
        factors_count = 1
        d = 2
        while d * d <= temp:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            if count > 0:
                factors_count *= (count + 1)
            d += 1
        if temp > 1:
            factors_count *= 2
            
        ans = str(factors_count)
        options = InfiniteQuestionEngine._safe_options(ans, [str(factors_count + d) for d in [-4, -2, 2, 4, 6, 8, 10]])

        
        q_text = f"How many distinct positive integer factors (divisors) does the number {n} have?"
        explanation = (
            f"To find the total number of positive factors of {n}, find its prime factorization.\n"
            f"If N = p₁^a × p₂^b × ..., the total number of divisors is (a + 1)(b + 1)...\n"
            f"For {n}, this yields exactly {factors_count} divisors."
        )
        return {
            "exam": "gre",
            "section": "quant",
            "subsection": "problem_solving",
            "difficulty": "hard",
            "question_text": q_text,
            "options": options,
            "correct_answer": ans,
            "explanation": explanation,
            "tags": ["number theory", "prime factorization", "divisors"],
            "time_limit": 100,
            "is_ai_generated": False
        }

    # ══════════════════════════════════════════════════════════════════════
    # GRE VERBAL PROCEDURAL GENERATOR
    # ══════════════════════════════════════════════════════════════════════
    @staticmethod
    def generate_gre_verbal() -> Dict[str, Any]:
        verbal_generators = [
            InfiniteQuestionEngine._verbal_text_completion,
            InfiniteQuestionEngine._verbal_sentence_equivalence,
            InfiniteQuestionEngine._verbal_reading_passage
        ]
        return random.choice(verbal_generators)()

    @staticmethod
    def _verbal_text_completion() -> Dict[str, Any]:
        templates = [
            {
                "sentence": "Although the professor’s lectures were renowned for their rigorous academic depth, students frequently found her delivery surprisingly _______, rendering complex theoretical physics accessible to novices.",
                "correct": "lucid",
                "distractors": ["abstruse", "pedantic", "ponderous", "obvolute"],
                "explanation": "'Although' indicates a contrast. Despite the rigorous academic depth, the delivery was easy to understand ('lucid'). 'Abstruse' and 'ponderous' mean difficult or heavy, opposite to the clue 'accessible to novices'."
            },
            {
                "sentence": "Far from being a passive observer, the diplomat adopted a remarkably _______ posture, intervening decisively whenever negotiations stalled.",
                "correct": "proactive",
                "distractors": ["quiescent", "complaisant", "reticent", "somnolent"],
                "explanation": "'Far from being a passive observer' establishes that the diplomat was active and assertive ('proactive'). 'Quiescent' and 'somnolent' mean quiet/inactive."
            },
            {
                "sentence": "The CEO was known for his _______ management style; he rarely praised his staff and was quick to excoriate even the most trivial oversight.",
                "correct": "hypercritical",
                "distractors": ["benevolent", "magnanimous", "indolent", "sycophantic"],
                "explanation": "The colon elaborates on the adjective: rarely praised staff and severely criticized small errors, demonstrating a 'hypercritical' (captious, fault-finding) approach."
            },
            {
                "sentence": "Despite initial predictions that the economic stimulus would have a negligible impact, the subsequent recovery proved to be remarkably _______, revitalizing manufacturing nationwide.",
                "correct": "robust",
                "distractors": ["anemic", "ephemeral", "precarious", "torpid"],
                "explanation": "'Despite' sets up a contrast with 'negligible impact'. The recovery was strong and vigorous ('robust')."
            },
            {
                "sentence": "Her research was characterized by a(n) _______ disregard for established methodology, relying instead on unorthodox, improvisational field studies.",
                "correct": "audacious",
                "distractors": ["deferential", "circumspect", "slavish", "timorous"],
                "explanation": "Relying on unorthodox improvisations rather than following established guidelines shows boldness and daring ('audacious')."
            },
            {
                "sentence": "The museum curator took great care to expose the forged manuscript, exposing its _______ provenance to the academic community.",
                "correct": "spurious",
                "distractors": ["impeccable", "verifiable", "canonical", "incontestable"],
                "explanation": "'Forged manuscript' indicates that its origin is fake, deceitful, or illegitimate ('spurious')."
            },
            {
                "sentence": "Because the author’s philosophical treatise was filled with convoluted syntax and archaic terminology, critics dismissed it as unnecessarily _______.",
                "correct": "arcane",
                "distractors": ["transparent", "pellucid", "cogent", "incisive"],
                "explanation": "Convoluted syntax and archaic terminology make something obscure and mysterious ('arcane')."
            },
            {
                "sentence": "Even among a cohort known for extravagance, the heir’s spending was extraordinarily _______, rapidly depleting a fortune accumulated over three generations.",
                "correct": "profligate",
                "distractors": ["frugal", "parsimonious", "austere", "abstemious"],
                "explanation": "Rapidly squandering a multi-generational fortune is the epitome of being wasteful and reckless ('profligate')."
            }
        ]
        chosen = random.choice(templates)
        options = [chosen["correct"]] + random.sample(chosen["distractors"], 4)
        random.shuffle(options)
        
        return {
            "exam": "gre",
            "section": "verbal",
            "subsection": "text_completion",
            "difficulty": "medium",
            "question_text": chosen["sentence"],
            "options": options,
            "correct_answer": chosen["correct"],
            "explanation": chosen["explanation"],
            "tags": ["vocabulary", "text completion", "context clues"],
            "time_limit": 75,
            "is_ai_generated": False
        }

    @staticmethod
    def _verbal_sentence_equivalence() -> Dict[str, Any]:
        templates = [
            {
                "sentence": "The politician’s speech was notoriously _______; despite speaking for nearly an hour, she managed to articulate almost nothing of real substance.",
                "pair": ["equivocal", "vacuous"],
                "options": ["equivocal", "vacuous", "incisive", "cogent", "perspicacious", "trenchant"],
                "correct": "equivocal, vacuous",
                "explanation": "Speaking for an hour without saying anything of substance indicates an evasive, empty message. 'Equivocal' and 'vacuous' both fit the context of conveying no clear content."
            },
            {
                "sentence": "Although often considered _______ by his peers, the reclusive composer occasionally produced melodies of startling warmth and tenderness.",
                "pair": ["aloof", "detached"],
                "options": ["aloof", "detached", "gregarious", "convivial", "effusive", "ebullient"],
                "correct": "aloof, detached",
                "explanation": "'Although' contrasts the reclusive composer's distant demeanor with the warmth of his melodies. 'Aloof' and 'detached' are synonymous in describing an emotionally reserved personality."
            },
            {
                "sentence": "The interim director’s handling of the crisis was decidedly _______, satisfying neither the rebellious employees nor the anxious board of trustees.",
                "pair": ["inept", "maladroit"],
                "options": ["inept", "maladroit", "adroit", "deft", "consummate", "dexterous"],
                "correct": "inept, maladroit",
                "explanation": "Failing to satisfy either faction demonstrates clumsy, incompetent management. 'Inept' and 'maladroit' both mean unskillful or bungling."
            },
            {
                "sentence": "The newly discovered historical ledger proved to be _______, verifying details about the treaty that historians had contested for decades.",
                "pair": ["invaluable", "priceless"],
                "options": ["invaluable", "priceless", "worthless", "redundant", "superfluous", "trivial"],
                "correct": "invaluable, priceless",
                "explanation": "Because the ledger verified decades of disputed historical facts, it was of immense importance ('invaluable' and 'priceless')."
            }
        ]
        chosen = random.choice(templates)
        options = list(chosen["options"])
        random.shuffle(options)
        
        return {
            "exam": "gre",
            "section": "verbal",
            "subsection": "sentence_equivalence",
            "difficulty": "hard",
            "question_text": f"{chosen['sentence']}\n\n(Select the TWO answer choices that complete the sentence and produce sentences that are alike in meaning.)",
            "options": options,
            "correct_answer": chosen["correct"],
            "explanation": chosen["explanation"],
            "tags": ["sentence equivalence", "vocabulary pairs", "synonyms"],
            "time_limit": 90,
            "is_ai_generated": False
        }

    @staticmethod
    def _verbal_reading_passage() -> Dict[str, Any]:
        passages = [
            {
                "passage": (
                    "Throughout the late twentieth century, paleontologists operated under the consensus that dinosaurian metabolism "
                    "was uniformly ectothermic, resembling modern reptiles in their dependency on ambient thermal conditions. "
                    "However, the histological examination of fossilized bone vascularization initiated by Armand de Ricqlès offered "
                    "compelling contrary evidence. Cortical bone tissues in theropods displayed dense Haversian remodeling and high "
                    "osteocyte lacuna density—traits virtually exclusive to endothermic birds and mammals capable of sustained elevated "
                    "growth rates. While skeptics initially attributed these microstructures to seasonal bone deposition cycles, isotopic "
                    "analysis of carbonate clumped isotopes in fossilized eggshells has further constrained body temperature estimates, "
                    "revealing operating internal temperatures consistently above ambient environmental baselines."
                ),
                "question": "The primary purpose of the passage is to:",
                "options": [
                    "Challenge a long-held scientific assumption using emerging microscopic and geochemical evidence.",
                    "Demonstrate that ectothermic organisms can achieve high growth rates through osteocyte remodeling.",
                    "Refute Armand de Ricqlès' findings on bone vascularization using clumped isotope data.",
                    "Argue that all prehistoric reptiles shared identical endothermic physiological traits.",
                    "Reconcile contradictory theories regarding the extinction chronology of theropods."
                ],
                "correct": "Challenge a long-held scientific assumption using emerging microscopic and geochemical evidence.",
                "explanation": "The passage outlines the historical consensus (dinosaurs were ectothermic) and details how bone histology (microscopic) and clumped isotopes (geochemical) provided contrary evidence demonstrating endothermic traits."
            }
        ]
        chosen = random.choice(passages)
        return {
            "exam": "gre",
            "section": "verbal",
            "subsection": "reading_comprehension",
            "difficulty": "hard",
            "passage": chosen["passage"],
            "question_text": chosen["question"],
            "options": chosen["options"],
            "correct_answer": chosen["correct"],
            "explanation": chosen["explanation"],
            "tags": ["reading comprehension", "primary purpose", "scientific passages"],
            "time_limit": 120,
            "is_ai_generated": False
        }

    # ══════════════════════════════════════════════════════════════════════
    # IELTS READING & GRAMMAR PROCEDURAL GENERATOR
    # ══════════════════════════════════════════════════════════════════════
    @staticmethod
    def generate_ielts_reading() -> Dict[str, Any]:
        templates = [
            {
                "passage": (
                    "Urban vertical farming involves producing crops in vertically stacked layers, commonly integrated into other structures "
                    "such as skyscrapers, used shipping containers, or repurposed warehouses. Modern implementations utilize controlled-environment "
                    "agriculture (CEA) technology, where artificial control of light, environmental humidity, temperature, and gaseous composition "
                    "is maintained. By cultivating plants indoors, vertical farms consume up to 95 percent less water than conventional agricultural methods "
                    "because water transpiration is captured and recycled within the closed loop. However, high capital expenditures and energy "
                    "consumption from continuous LED lighting remain significant economic barriers to widespread commercial viability."
                ),
                "question": "According to the passage, why do vertical farms use significantly less water than traditional farming?",
                "options": [
                    "Water vapor transpired by plants is collected and recycled within the facility.",
                    "Genetically modified crops that require minimal hydration are grown exclusively.",
                    "Rainwater is collected from skyscraper rooftops to irrigate the crops.",
                    "Automated LED lighting reduces the rate of plant transpiration by half."
                ],
                "correct": "Water vapor transpired by plants is collected and recycled within the facility.",
                "explanation": "The passage states: 'consume up to 95 percent less water than conventional agricultural methods because water transpiration is captured and recycled within the closed loop.'"
            },
            {
                "passage": (
                    "The Great Barrier Reef, spanning over 2,300 kilometers off the northeastern coast of Australia, represents the world’s "
                    "largest coral reef ecosystem. Corals exist in an obligate symbiotic relationship with microscopic photosynthetic algae known as zooxanthellae. "
                    "When sea surface temperatures exceed seasonal thresholds for prolonged durations, thermal stress triggers the expulsion of these algae, "
                    "causing the coral to turn completely white in a process known as mass coral bleaching. While bleached corals are not dead immediately, "
                    "they become starved of nutrients and vulnerable to disease if ambient temperatures do not return to normal within several weeks."
                ),
                "question": "Do the following statements agree with the information in the reading passage?\n\nStatement: 'Coral bleaching immediately kills coral colonies as soon as zooxanthellae are expelled.'",
                "options": [
                    "TRUE",
                    "FALSE",
                    "NOT GIVEN"
                ],
                "correct": "FALSE",
                "explanation": "The text directly contradicts the statement: 'While bleached corals are not dead immediately, they become starved of nutrients and vulnerable to disease if ambient temperatures do not return to normal within several weeks.' Therefore, the statement is FALSE."
            }
        ]
        chosen = random.choice(templates)
        return {
            "exam": "ielts",
            "section": "reading",
            "subsection": "multiple_choice" if len(chosen["options"]) > 3 else "true_false_not_given",
            "difficulty": "medium",
            "passage": chosen["passage"],
            "question_text": chosen["question"],
            "options": chosen["options"],
            "correct_answer": chosen["correct"],
            "explanation": chosen["explanation"],
            "tags": ["ielts academic reading", "detail questions", "fact checking"],
            "time_limit": 90,
            "is_ai_generated": False
        }


def get_procedural_question(exam: str, section: str = None) -> Dict[str, Any]:
    """Generates an instant high-quality procedural question for the specified exam and section."""
    if exam == "gre":
        if section == "verbal":
            return InfiniteQuestionEngine.generate_gre_verbal()
        else:
            return InfiniteQuestionEngine.generate_gre_quant()
    else:  # ielts
        return InfiniteQuestionEngine.generate_ielts_reading()
