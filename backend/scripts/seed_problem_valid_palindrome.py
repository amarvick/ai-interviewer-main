"""
Seed script for the "Valid Palindrome" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_valid_palindrome.py
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
        "id": "two_pointer_filter",
        "title": "Two-pointer scan with on-the-fly filtering",
        "pseudocode": """1. left = 0, right = len(s) - 1
2. While left < right:
       while left < right and not s[left].isalnum(): left += 1
       while left < right and not s[right].isalnum(): right -= 1
       if lower(s[left]) != lower(s[right]): return False
       left += 1; right -= 1
3. Return True
Time: O(n). Space: O(1).""",
        "complexity": "O(n) time, O(1) space",
        "is_optimal": True,
        "notes": "Streaming-friendly because it avoids materializing a cleaned copy.",
        "match_signals": [
            "l < r",
            "isalnum",
            "while left < right",
            "toLowerCase",
        ],
        "strengths": [
            "Processes the string in a single pass without extra buffers.",
            "Handles Unicode/alphanumeric definitions by reusing character helpers.",
        ],
        "improvements": [
            "Mention ASCII assumptions if using manual code comparisons.",
            "Call out the need to prevent index errors when skipping non-alphanumerics.",
        ],
    },
    {
        "id": "filtered_reverse_compare",
        "title": "Filter + reverse comparison",
        "pseudocode": """1. cleaned = [lower(c) for c in s if c.isalnum()]
2. Return cleaned == reversed(cleaned)
Time: O(n). Space: O(n).""",
        "complexity": "O(n) time, O(n) space",
        "is_optimal": False,
        "notes": "Easiest to reason about but uses extra memory.",
        "match_signals": [
            "filtered",
            "\"\".join",
            "cleaned == cleaned[::-1]",
        ],
        "strengths": [
            "Simple to implement correctly in high-level languages.",
        ],
        "improvements": [
            "Discuss memory impact on very long strings (2e5 characters).",
            "Highlight how to avoid intermediate string copies.",
        ],
    },
    {
        "id": "deque_stream",
        "title": "Deque streaming check",
        "pseudocode": """1. Build deque of lowercase alphanumerics
2. While len(deque) > 1:
       if deque.popleft() != deque.pop(): return False
3. Return True
Time: O(n). Space: O(n).""",
        "complexity": "O(n) time, O(n) space",
        "is_optimal": False,
        "notes": "Demonstrates use of queue data structures but unnecessary for final answer.",
        "match_signals": [
            "deque",
            "popleft",
        ],
        "strengths": [
            "Shows comfort with double-ended queues / streaming checks.",
        ],
        "improvements": [
            "Explain why this degenerates to the filtered copy approach.",
            "Mention that random access is unnecessary with two pointers.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "two_pointer_reasoning",
        "title": "Two-pointer palindrome reasoning",
        "description": "Explain why comparing mirrored characters while skipping non-alphanumerics preserves correctness and hits O(n).",
        "bonus_mentions": [
            "skip non-alphanumeric",
            "lowercase conversions",
            "short-circuit on mismatch",
        ],
    },
    {
        "id": "normalization_costs",
        "title": "Normalization vs streaming",
        "description": "Compare building a cleaned string first versus scanning in place, emphasizing memory trade-offs.",
        "bonus_mentions": [
            "cleaned buffer",
            "O(1) space advantage",
            "large input constraints",
        ],
    },
    {
        "id": "ascii_vs_unicode",
        "title": "ASCII assumptions",
        "description": "Discuss why the problem defines printable ASCII but the technique can extend to Unicode by adjusting the `isalnum` predicate.",
        "bonus_mentions": [
            "locale awareness",
            "isalnum semantics",
            "unicode normalization",
        ],
    },
]

VALID_PALINDROME = {
    "slug": "valid-palindrome",
    "title": "Valid Palindrome",
    "category": "Two Pointers",
    "difficulty": "Easy",
    "description": """A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string `s`, return `True` if it is a palindrome, or `False` otherwise.

Example 1
```
Input: "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

Example 2
```
Input: "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
```

Example 3
```
Input: " "
Output: true
Explanation: After removing non-alphanumeric characters we get an empty string, which is a palindrome.
```

Constraints
- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.
""",
    "starter_code": {
        "python": """class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Write your code here
        return False
""",
        "javascript": """class Solution {
  /**
   * @param {string} s
   * @return {boolean}
   */
  isPalindrome = function(s) {
    // Write your code here
    return false;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public boolean isPalindrome(String s) {
        // Write your code here
        return false;
    }
}
""",
        "cpp": """class Solution {
public:
    bool isPalindrome(string s) {
        // Write your code here
        return false;
    }
};
""",
    },
    "reference_pseudocode": """Goal: compare alphanumeric characters from both ends ignoring case.

1. left = 0, right = len(s) - 1
2. While left < right:
       while left < right and not s[left].isalnum(): left += 1
       while left < right and not s[right].isalnum(): right -= 1
       if left < right and s[left].lower() != s[right].lower(): return False
       left += 1; right -= 1
3. Return True

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


def seed_valid_palindrome() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == VALID_PALINDROME["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == VALID_PALINDROME["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=VALID_PALINDROME["slug"],
                title=VALID_PALINDROME["title"],
                description=VALID_PALINDROME["description"],
                difficulty=VALID_PALINDROME["difficulty"],
                category=VALID_PALINDROME["category"],
                starter_code=VALID_PALINDROME["starter_code"],
                reference_pseudocode=VALID_PALINDROME["reference_pseudocode"],
                reference_pseudocode_variants=VALID_PALINDROME["reference_pseudocode_variants"],
                reference_talking_points=VALID_PALINDROME["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Valid Palindrome")
        else:
            problem.description = VALID_PALINDROME["description"]
            problem.difficulty = VALID_PALINDROME["difficulty"]
            problem.category = VALID_PALINDROME["category"]
            problem.starter_code = VALID_PALINDROME["starter_code"]
            problem.reference_pseudocode = VALID_PALINDROME["reference_pseudocode"]
            problem.reference_pseudocode_variants = VALID_PALINDROME["reference_pseudocode_variants"]
            problem.reference_talking_points = VALID_PALINDROME["reference_talking_points"]
            problem.slug = VALID_PALINDROME["slug"]
            db.flush()
            print("Updated problem: Valid Palindrome")

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
    seed_valid_palindrome()
