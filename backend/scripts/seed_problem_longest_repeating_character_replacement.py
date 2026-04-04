"""
Seed script for the "Longest Repeating Character Replacement" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_longest_repeating_character_replacement.py
"""

from pathlib import Path
import sys

# Ensure "app" package is importable when running as a script path.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.database import Base, SessionLocal, engine
from app.db.models import Problem, ProblemList, ProblemListProblem
import app.db.models  # noqa: F401


REFERENCE_VARIANTS = [
    {
        "id": "sliding_window_frequency",
        "title": "Sliding window with max frequency tracking",
        "pseudocode": """1. left = 0, counts = array[26] = 0, best = 0, max_freq = 0
2. For right in range(len(s)):
       counts[s[right]] += 1
       max_freq = max(max_freq, counts[s[right]])
       while (right - left + 1) - max_freq > k:
           counts[s[left]] -= 1
           left += 1
       best = max(best, right - left + 1)
3. Return best
Time: O(n). Space: O(1).""",
        "complexity": "O(n) time, O(1) space",
        "is_optimal": True,
        "notes": "Tracks the most frequent char in the current window instead of recomputing every shrink.",
        "match_signals": [
            "right - left + 1",
            "max_freq",
            "counts[",
            "while (window - max_freq) > k",
        ],
        "strengths": [
            "Explains why max_freq can stay stale because window only shrinks when needed.",
            "Handles n up to 10^5 easily.",
        ],
        "improvements": [
            "Mention resetting max_freq is optional; stale value only makes window harder to grow, not incorrect.",
            "Call out assumption that input letters are uppercase A-Z (26 bucket).",
        ],
    },
    {
        "id": "brute_force_for_each_char",
        "title": "Check longest window per anchor character",
        "pseudocode": """For each letter in 'A'..'Z', walk string counting replacements needed to keep that letter dominant.
Time: O(26 * n).""",
        "complexity": "O(26n) time, O(1) space",
        "is_optimal": False,
        "notes": "Acceptable but slower; shows understanding of constraint-driven enumeration.",
        "match_signals": [
            "for target in range(26)",
            "expand window per char",
        ],
        "strengths": [
            "Demonstrates another way to reason about replacement budget.",
        ],
        "improvements": [
            "Explain why double loops still linear due to fixed alphabet.",
            "Contrast with single-pass approach.",
        ],
    },
    {
        "id": "binary_search_window",
        "title": "Binary search answer length with feasibility check",
        "pseudocode": """Binary search length L and check via sliding window if any substring needs <= k replacements to become uniform.
Time: O(n log n).""",
        "complexity": "O(n log n) time, O(1) space",
        "is_optimal": False,
        "notes": "Shows advanced thinking but unnecessary given monotonic window solution.",
        "match_signals": [
            "binary search on length",
            "feasible(L)",
        ],
        "strengths": [
            "Highlights monotonic property for alternate solution.",
        ],
        "improvements": [
            "Point out added log factor and complexity of feasibility routine.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "window_replacement_budget",
        "title": "Window size minus max frequency reasoning",
        "description": "Explain why replacements needed equals window length minus the count of the most frequent character.",
        "bonus_mentions": [
            "dominant character",
            "budget <= k",
            "skip recomputation",
        ],
    },
    {
        "id": "stale_max_freq",
        "title": "Why stale max frequency is safe",
        "description": "Clarify that max_freq only ever increases, and an overestimate simply delays shrinking without affecting correctness.",
        "bonus_mentions": [
            "monotonic max",
            "only shrink when needed",
            "amortized O(n)",
        ],
    },
    {
        "id": "alphabet_constraints",
        "title": "Leveraging limited alphabet",
        "description": "Highlight that uppercase ASCII letters let us use fixed-size arrays over dictionaries, improving constants.",
        "bonus_mentions": [
            "26 bucket array",
            "O(1) space",
            "extend to full ASCII/Unicode if needed",
        ],
    },
]

LONGEST_REPEATING = {
    "slug": "longest-repeating-character-replacement",
    "title": "Longest Repeating Character Replacement",
    "category": "Sliding Window",
    "difficulty": "Medium",
    "description": """You are given a string `s` consisting of uppercase English letters and an integer `k`. You may replace any character in `s` with any other letter at most `k` times. Return the length of the longest substring containing the same letter you can achieve.

Example 1
```
Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace two 'A' with 'B' to get "BBBB".
```

Example 2
```
Input: s = "AABABBA", k = 1
Output: 4
Explanation: Replace the middle 'A' with 'B' to form "AABBBBA".
```

Constraints
- `1 <= s.length <= 10^5`
- `s` consists of uppercase English letters.
- `0 <= k <= s.length`
""",
    "starter_code": {
        "python": """class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Write your code here
        return 0
""",
        "javascript": """class Solution {
  /**
   * @param {string} s
   * @param {number} k
   * @return {number}
   */
  characterReplacement = function(s, k) {
    // Write your code here
    return 0;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int characterReplacement(String s, int k) {
        // Write your code here
        return 0;
    }
}
""",
        "cpp": """class Solution {
public:
    int characterReplacement(string s, int k) {
        // Write your code here
        return 0;
    }
};
""",
    },
    "reference_pseudocode": """Goal: maintain a sliding window where replacements needed <= k.

1. counts[26] = 0, left = 0, max_freq = 0, best = 0
2. For right from 0..len(s)-1:
       idx = ord(s[right]) - ord('A')
       counts[idx] += 1
       max_freq = max(max_freq, counts[idx])
       while (right - left + 1) - max_freq > k:
           counts[ord(s[left]) - ord('A')] -= 1
           left += 1
       best = max(best, right - left + 1)
3. Return best

Time Complexity: O(n). Space Complexity: O(1).
""",
    "reference_pseudocode_variants": REFERENCE_VARIANTS,
    "reference_talking_points": REFERENCE_TALKING_POINTS,
}

TARGET_LIST_IDS = (
    "blind_75",
    "taro_75",
    "neetcode_150",
    "grind_169",
    "google_50",
)


def seed_longest_repeating_character_replacement() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == LONGEST_REPEATING["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == LONGEST_REPEATING["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=LONGEST_REPEATING["slug"],
                title=LONGEST_REPEATING["title"],
                description=LONGEST_REPEATING["description"],
                difficulty=LONGEST_REPEATING["difficulty"],
                category=LONGEST_REPEATING["category"],
                starter_code=LONGEST_REPEATING["starter_code"],
                reference_pseudocode=LONGEST_REPEATING["reference_pseudocode"],
                reference_pseudocode_variants=LONGEST_REPEATING["reference_pseudocode_variants"],
                reference_talking_points=LONGEST_REPEATING["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Longest Repeating Character Replacement")
        else:
            problem.description = LONGEST_REPEATING["description"]
            problem.difficulty = LONGEST_REPEATING["difficulty"]
            problem.category = LONGEST_REPEATING["category"]
            problem.starter_code = LONGEST_REPEATING["starter_code"]
            problem.reference_pseudocode = LONGEST_REPEATING["reference_pseudocode"]
            problem.reference_pseudocode_variants = LONGEST_REPEATING["reference_pseudocode_variants"]
            problem.reference_talking_points = LONGEST_REPEATING["reference_talking_points"]
            problem.slug = LONGEST_REPEATING["slug"]
            db.flush()
            print("Updated problem: Longest Repeating Character Replacement")

        linked = 0
        skipped = 0
        for list_id in TARGET_LIST_IDS:
            problem_list = db.query(ProblemList).filter(ProblemList.id == list_id).first()
            if problem_list is None:
                continue

            existing_link = (
                db.query(ProblemListProblem)
                .filter(
                    ProblemListProblem.problem_list_id == list_id,
                    ProblemListProblem.problem_id == problem.id,
                )
                .first()
            )

            if existing_link:
                skipped += 1
                continue

            db.add(
                ProblemListProblem(
                    problem_list_id=list_id,
                    problem_id=problem.id,
                )
            )
            linked += 1

        db.commit()
        print(f"Done. Linked to lists: {linked}, Existing links skipped: {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_longest_repeating_character_replacement()
