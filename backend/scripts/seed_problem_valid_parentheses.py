"""
Seed script for the "Valid Parentheses" problem.

Run:
    python backend/scripts/seed_problem_valid_parentheses.py
"""

from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.database import Base, SessionLocal, engine
from app.db.models import Problem, ProblemList, ProblemListProblem
import app.db.models  # noqa: F401


REFERENCE_VARIANTS = [
    {
        "id": "stack_matching",
        "title": "Stack-based matching (optimal)",
        "pseudocode": """1. stack = []
2. pairs = {')': '(', ']': '[', '}': '{'}
3. For char in s:
       if char in '([{':
           stack.append(char)
       else:
           if not stack or stack.pop() != pairs[char]:
               return False
4. Return len(stack) == 0
Time: O(n). Space: O(n).""",
        "complexity": "O(n) time, O(n) space",
        "is_optimal": True,
        "notes": "Classic stack approach ensuring nesting order.",
        "match_signals": [
            "stack",
            "pairs",
            "append/pop",
        ],
        "strengths": [
            "Handles all three bracket types uniformly.",
        ],
        "improvements": [
            "Mention early exit if remaining characters < stack size (optional micro-optimization).",
        ],
    },
    {
        "id": "replace_pairs",
        "title": "Iteratively remove matched pairs",
        "pseudocode": """Repeat replace '()', '[]', '{}' with '' until no change; valid if string empty.
Time: O(k * n).""",
        "complexity": "O(n^2) worst-case",
        "is_optimal": False,
        "notes": "Simpler to reason but inefficient for n up to 10^4.",
        "match_signals": [
            "while '()' in s",
            "s = s.replace",
        ],
        "strengths": [
            "Short code for quick prototypes.",
        ],
        "improvements": [
            "Explain time complexity and why stack is preferred.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "stack_invariant",
        "title": "Stack invariant",
        "description": "Explain that stack holds unmatched opens, ensuring every close matches the most recent open.",
        "bonus_mentions": [
            "LIFO",
            "nested structure",
        ],
    },
    {
        "id": "early_exit",
        "title": "Early exit on mismatch",
        "description": "Call out that we can exit immediately when encountering a bad closing bracket.",
        "bonus_mentions": [
            "invalid close",
            "empty stack",
        ],
    },
]

VALID_PARENTHESES = {
    "slug": "valid-parentheses",
    "title": "Valid Parentheses",
    "category": "Stack",
    "difficulty": "Easy",
    "description": """Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

Rules:
1. Open brackets must be closed by the same type of bracket.
2. Open brackets must be closed in the correct order.
3. Every close bracket must have a corresponding open bracket of the same type.

Examples
```
Input: "()"
Output: true

Input: "()[]{}"
Output: true

Input: "(]"
Output: false
```

Constraints
- `1 <= s.length <= 10^4`
- `s` consists only of parentheses characters.
""",
    "starter_code": {
        "python": """class Solution:
    def isValid(self, s: str) -> bool:
        # Write your code here
        return False
""",
        "javascript": """class Solution {
  /**
   * @param {string} s
   * @return {boolean}
   */
  isValid = function(s) {
    // Write your code here
    return false;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public boolean isValid(String s) {
        // Write your code here
        return false;
    }
}
""",
        "cpp": """class Solution {
public:
    bool isValid(string s) {
        // Write your code here
        return false;
    }
};
""",
    },
    "reference_pseudocode": """Use a stack to match brackets:

stack = []
pairs = {')': '(', ']': '[', '}': '{'}
for char in s:
    if char in pairs.values():
        stack.append(char)
    else:
        if not stack or stack.pop() != pairs[char]:
            return False
return not stack
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


def seed_valid_parentheses() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == VALID_PARENTHESES["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == VALID_PARENTHESES["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=VALID_PARENTHESES["slug"],
                title=VALID_PARENTHESES["title"],
                description=VALID_PARENTHESES["description"],
                difficulty=VALID_PARENTHESES["difficulty"],
                category=VALID_PARENTHESES["category"],
                starter_code=VALID_PARENTHESES["starter_code"],
                reference_pseudocode=VALID_PARENTHESES["reference_pseudocode"],
                reference_pseudocode_variants=VALID_PARENTHESES["reference_pseudocode_variants"],
                reference_talking_points=VALID_PARENTHESES["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Valid Parentheses")
        else:
            problem.description = VALID_PARENTHESES["description"]
            problem.difficulty = VALID_PARENTHESES["difficulty"]
            problem.category = VALID_PARENTHESES["category"]
            problem.starter_code = VALID_PARENTHESES["starter_code"]
            problem.reference_pseudocode = VALID_PARENTHESES["reference_pseudocode"]
            problem.reference_pseudocode_variants = VALID_PARENTHESES["reference_pseudocode_variants"]
            problem.reference_talking_points = VALID_PARENTHESES["reference_talking_points"]
            problem.slug = VALID_PARENTHESES["slug"]
            db.flush()
            print("Updated problem: Valid Parentheses")

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
    seed_valid_parentheses()
