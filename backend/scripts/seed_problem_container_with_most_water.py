"""
Seed script for the "Container With Most Water" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_container_with_most_water.py
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
        "id": "two_pointer_shrink",
        "title": "Two-pointer shrink from ends (optimal)",
        "pseudocode": """1. left = 0, right = len(height) - 1, best = 0
2. While left < right:
       width = right - left
       best = max(best, width * min(height[left], height[right]))
       if height[left] < height[right]:
           left += 1
       else:
           right -= 1
3. Return best
Time: O(n). Space: O(1).""",
        "complexity": "O(n) time, O(1) space",
        "is_optimal": True,
        "notes": "Moves the pointer on the shorter wall because doing so is the only way to potentially increase area.",
        "match_signals": [
            "left < right",
            "while",
            "min(height[left], height[right])",
            "width =",
        ],
        "strengths": [
            "Linear scan satisfies n ≤ 1e5 constraint comfortably.",
            "Explains the greedy proof and termination logic.",
        ],
        "improvements": [
            "Clarify why moving the taller wall cannot increase area when the shorter wall limits height.",
            "Mention potential overflow if multiplying ints without casting (in C++/Java).",
        ],
    },
    {
        "id": "brute_force_pairs",
        "title": "Brute-force check every pair",
        "pseudocode": """1. best = 0
2. For i from 0..n-2:
       For j from i+1..n-1:
           best = max(best, (j - i) * min(height[i], height[j]))
3. Return best
Time: O(n^2).""",
        "complexity": "O(n^2) time, O(1) space",
        "is_optimal": False,
        "notes": "Baseline reasoning, but infeasible for n up to 10^5.",
        "match_signals": [
            "for i in range",
            "for (int i",
            "nested loops",
        ],
        "strengths": [
            "Simple to reason about and validate small examples.",
        ],
        "improvements": [
            "Use it to motivate the two-pointer optimization.",
            "Address timeouts explicitly.",
        ],
    },
    {
        "id": "priority_queue_edges",
        "title": "Priority queue / sorting edges",
        "pseudocode": """1. Sort indices by height descending
2. Track min and max index seen so far, compute areas
Time: O(n log n).""",
        "complexity": "O(n log n) time, O(n) space",
        "is_optimal": False,
        "notes": "An alternate heuristic that is slower than two pointers but interviewers may accept if justified.",
        "match_signals": [
            "sorted_pairs",
            "priority queue",
            "max heap",
        ],
        "strengths": [
            "Shows creative thinking with ordering by height.",
        ],
        "improvements": [
            "Explain why it still misses O(n) requirement.",
            "Clarify correctness proof (maintaining furthest indices).",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "two_pointer_proof",
        "title": "Why the greedy two-pointer move works",
        "description": "Walk through the argument that the shorter side bounds the area, so only advancing that pointer can find a larger container.",
        "bonus_mentions": [
            "shorter side limits height",
            "width shrinks each iteration",
            "complete coverage of search space",
        ],
    },
    {
        "id": "constraint_driven_complexity",
        "title": "Constraints demand O(n)",
        "description": "Connect n up to 1e5 with the need to avoid O(n^2), referencing how the pointers scan once.",
        "bonus_mentions": [
            "n=100k",
            "nested loops -> timeout",
            "linear scan proof",
        ],
    },
    {
        "id": "overflow_and_types",
        "title": "Handling large products",
        "description": "Call out that widths up to 1e5 and heights up to 1e4 fit in 32-bit ints but languages like C++/Java may need 64-bit temporaries.",
        "bonus_mentions": [
            "use long long",
            "cast to long",
            "safe multiplication",
        ],
    },
]

CONTAINER_MOST_WATER = {
    "slug": "container-with-most-water",
    "title": "Container With Most Water",
    "category": "Two Pointers",
    "difficulty": "Medium",
    "description": """You are given an integer array `height` of length `n`. Draw n vertical lines such that the endpoints of the `i`-th line are `(i, 0)` and `(i, height[i])`.

Find two lines that, together with the x-axis, form a container that can store the most water, and return the maximum amount of water the container can store. The container cannot be slanted.

Example 1
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
```

Example 2
```
Input: height = [1,1]
Output: 1
```

Constraints
- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`
""",
    "starter_code": {
        "python": """class Solution:
    def maxArea(self, height: List[int]) -> int:
        # Write your code here
        return 0
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} height
   * @return {number}
   */
  maxArea = function(height) {
    // Write your code here
    return 0;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int maxArea(int[] height) {
        // Write your code here
        return 0;
    }
}
""",
        "cpp": """class Solution {
public:
    int maxArea(vector<int>& height) {
        // Write your code here
        return 0;
    }
};
""",
    },
    "reference_pseudocode": """Goal: maximize area = (right - left) * min(height[left], height[right]).

1. left = 0, right = len(height) - 1, best = 0
2. While left < right:
       width = right - left
       area = width * min(height[left], height[right])
       best = max(best, area)
       if height[left] <= height[right]:
           left += 1
       else:
           right -= 1
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


def seed_container_with_most_water() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == CONTAINER_MOST_WATER["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == CONTAINER_MOST_WATER["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=CONTAINER_MOST_WATER["slug"],
                title=CONTAINER_MOST_WATER["title"],
                description=CONTAINER_MOST_WATER["description"],
                difficulty=CONTAINER_MOST_WATER["difficulty"],
                category=CONTAINER_MOST_WATER["category"],
                starter_code=CONTAINER_MOST_WATER["starter_code"],
                reference_pseudocode=CONTAINER_MOST_WATER["reference_pseudocode"],
                reference_pseudocode_variants=CONTAINER_MOST_WATER["reference_pseudocode_variants"],
                reference_talking_points=CONTAINER_MOST_WATER["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Container With Most Water")
        else:
            problem.description = CONTAINER_MOST_WATER["description"]
            problem.difficulty = CONTAINER_MOST_WATER["difficulty"]
            problem.category = CONTAINER_MOST_WATER["category"]
            problem.starter_code = CONTAINER_MOST_WATER["starter_code"]
            problem.reference_pseudocode = CONTAINER_MOST_WATER["reference_pseudocode"]
            problem.reference_pseudocode_variants = CONTAINER_MOST_WATER["reference_pseudocode_variants"]
            problem.reference_talking_points = CONTAINER_MOST_WATER["reference_talking_points"]
            problem.slug = CONTAINER_MOST_WATER["slug"]
            db.flush()
            print("Updated problem: Container With Most Water")

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
    seed_container_with_most_water()
