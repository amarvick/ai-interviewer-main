"""
Seed script for the "Find Minimum in Rotated Sorted Array" problem.

Run:
    python scripts/seed_problem_find_min_rotated_sorted_array.py
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
        "id": "binary_search_pivot",
        "title": "Binary search for pivot (optimal)",
        "pseudocode": """1. left = 0, right = len(nums) - 1
2. While left < right:
       mid = (left + right) // 2
       if nums[mid] > nums[right]:
           left = mid + 1
       else:
           right = mid
3. Return nums[left]
Time: O(log n). Space: O(1).""",
        "complexity": "O(log n) time, O(1) space",
        "is_optimal": True,
        "notes": "Leverages sorted halves with rotation pivot; handles strictly increasing unique numbers.",
        "match_signals": [
            "while left < right",
            "nums[mid] > nums[right]",
            "right = mid",
        ],
        "strengths": [
            "Clean binary search reasoning and meets O(log n) requirement.",
        ],
        "improvements": [
            "Clarify behavior when array is already sorted (no rotation).",
        ],
    },
    {
        "id": "linear_scan",
        "title": "Linear scan for minimum",
        "pseudocode": """Return min(nums) using a loop.
Time: O(n).""",
        "complexity": "O(n) time, O(1) space",
        "is_optimal": False,
        "notes": "Only for baseline or follow-up when duplicates appear.",
        "match_signals": [
            "min(",
            "for num in nums",
        ],
        "strengths": [
            "Simple but does not satisfy required complexity.",
        ],
        "improvements": [
            "Use to motivate binary search requirement.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "pivot_logic",
        "title": "Why compare mid to right",
        "description": "Explain that if nums[mid] > nums[right], the minimum must be to the right of mid; otherwise to the left including mid.",
        "bonus_mentions": [
            "rotated sorted array",
            "monotonic halves",
        ],
    },
    {
        "id": "already_sorted_case",
        "title": "Handling no rotation",
        "description": "Call out that if nums[left] <= nums[right], you can return nums[left] immediately.",
        "bonus_mentions": [
            "early exit",
            "k rotations where k % n == 0",
        ],
    },
]

FIND_MIN_ROTATED = {
    "slug": "find-minimum-in-rotated-sorted-array",
    "title": "Find Minimum in Rotated Sorted Array",
    "category": "Binary Search",
    "difficulty": "Medium",
    "description": """Given an ascending sorted array `nums` that is rotated between 1 and `n` times, find the minimum element. `nums` contains unique integers.

Example 1
```
Input: nums = [3,4,5,1,2]
Output: 1
```

Example 2
```
Input: nums = [4,5,6,7,0,1,2]
Output: 0
```

Example 3
```
Input: nums = [11,13,15,17]
Output: 11
```

Constraints
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All integers are unique.
- Array is rotated between 1 and n times.
- Must run in O(log n).
""",
    "starter_code": {
        "python": """class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Write your code here
        return 0
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  findMin = function(nums) {
    // Write your code here
    return 0;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int findMin(int[] nums) {
        // Write your code here
        return 0;
    }
}
""",
        "cpp": """class Solution {
public:
    int findMin(vector<int>& nums) {
        // Write your code here
        return 0;
    }
};
""",
    },
    "reference_pseudocode": """Binary search for pivot:

left = 0
right = len(nums) - 1
while left < right:
    mid = (left + right) // 2
    if nums[mid] > nums[right]:
        left = mid + 1
    else:
        right = mid
return nums[left]
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


def seed_find_min_rotated() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == FIND_MIN_ROTATED["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == FIND_MIN_ROTATED["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=FIND_MIN_ROTATED["slug"],
                title=FIND_MIN_ROTATED["title"],
                description=FIND_MIN_ROTATED["description"],
                difficulty=FIND_MIN_ROTATED["difficulty"],
                category=FIND_MIN_ROTATED["category"],
                starter_code=FIND_MIN_ROTATED["starter_code"],
                reference_pseudocode=FIND_MIN_ROTATED["reference_pseudocode"],
                reference_pseudocode_variants=FIND_MIN_ROTATED["reference_pseudocode_variants"],
                reference_talking_points=FIND_MIN_ROTATED["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Find Minimum in Rotated Sorted Array")
        else:
            problem.description = FIND_MIN_ROTATED["description"]
            problem.difficulty = FIND_MIN_ROTATED["difficulty"]
            problem.category = FIND_MIN_ROTATED["category"]
            problem.starter_code = FIND_MIN_ROTATED["starter_code"]
            problem.reference_pseudocode = FIND_MIN_ROTATED["reference_pseudocode"]
            problem.reference_pseudocode_variants = FIND_MIN_ROTATED["reference_pseudocode_variants"]
            problem.reference_talking_points = FIND_MIN_ROTATED["reference_talking_points"]
            problem.slug = FIND_MIN_ROTATED["slug"]
            db.flush()
            print("Updated problem: Find Minimum in Rotated Sorted Array")

        linked = skipped = 0
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
            db.add(ProblemListProblem(problem_list_id=list_id, problem_id=problem.id))
            linked += 1

        db.commit()
        print(f"Done. Linked to lists: {linked}, Existing links skipped: {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_find_min_rotated()
