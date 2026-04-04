"""
Seed script for the "Search in Rotated Sorted Array" problem.

Run:
    python scripts/seed_problem_search_rotated_sorted_array.py
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
        "id": "binary_search_identify_sorted_half",
        "title": "Binary search with sorted half detection (optimal)",
        "pseudocode": """1. left = 0, right = len(nums) - 1
2. While left <= right:
       mid = (left + right) // 2
       if nums[mid] == target: return mid
       if nums[left] <= nums[mid]:  # left half sorted
           if nums[left] <= target < nums[mid]:
               right = mid - 1
           else:
               left = mid + 1
       else:  # right half sorted
           if nums[mid] < target <= nums[right]:
               left = mid + 1
           else:
               right = mid - 1
3. Return -1
Time: O(log n). Space: O(1).""",
        "complexity": "O(log n) time, O(1) space",
        "is_optimal": True,
        "notes": "Classic approach for rotated arrays with unique values.",
        "match_signals": [
            "nums[left] <= nums[mid]",
            "sorted half",
            "left <= right",
        ],
        "strengths": [
            "Meets O(log n) requirement and handles arbitrary rotation.",
        ],
        "improvements": [
            "Call out how to adapt when duplicates exist (requires extra checks).",
        ],
    },
    {
        "id": "pivot_then_binary_search",
        "title": "Find pivot then binary search",
        "pseudocode": """1. Identify pivot via binary search (minimum index)
2. Binary search on appropriate half.
Time: O(log n).""",
        "complexity": "O(log n) time, O(1) space",
        "is_optimal": False,
        "notes": "Two-step approach; useful alternative but slightly more code.",
        "match_signals": [
            "find pivot",
            "two binary search",
        ],
        "strengths": [
            "Demonstrates decomposition strategy.",
        ],
        "improvements": [
            "Discuss trade-offs vs single-pass detection.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "sorted_half_reasoning",
        "title": "Reasoning about sorted halves",
        "description": "Explain why one half of the array is always sorted and how that guides the binary search decision.",
        "bonus_mentions": [
            "distinct values",
            "rotation pivot",
        ],
    },
    {
        "id": "edge_cases_length_one",
        "title": "Edge cases (length 1, no rotation)",
        "description": "Highlight handling of n=1 and arrays that were not rotated at all.",
        "bonus_mentions": [
            "left == right",
            "nums[left] == target",
        ],
    },
]

SEARCH_ROTATED = {
    "slug": "search-in-rotated-sorted-array",
    "title": "Search in Rotated Sorted Array",
    "category": "Binary Search",
    "difficulty": "Medium",
    "description": """Given an ascending sorted array `nums` that may be rotated at an unknown pivot, search for `target` and return its index, or `-1` if not found. All elements are unique and O(log n) time is required.

Example 1
```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

Example 2
```
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

Example 3
```
Input: nums = [1], target = 0
Output: -1
```

Constraints
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values are unique.
- Array is ascending sorted then rotated.
- `-10^4 <= target <= 10^4`.
""",
    "starter_code": {
        "python": """class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Write your code here
        return -1
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number}
   */
  search = function(nums, target) {
    // Write your code here
    return -1;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int search(int[] nums, int target) {
        // Write your code here
        return -1;
    }
}
""",
        "cpp": """class Solution {
public:
    int search(vector<int>& nums, int target) {
        // Write your code here
        return -1;
    }
};
""",
    },
    "reference_pseudocode": """Binary search with sorted half detection:

left = 0
right = len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
    if nums[left] <= nums[mid]:  # left half sorted
        if nums[left] <= target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    else:  # right half sorted
        if nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
return -1
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


def seed_search_rotated() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == SEARCH_ROTATED["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == SEARCH_ROTATED["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=SEARCH_ROTATED["slug"],
                title=SEARCH_ROTATED["title"],
                description=SEARCH_ROTATED["description"],
                difficulty=SEARCH_ROTATED["difficulty"],
                category=SEARCH_ROTATED["category"],
                starter_code=SEARCH_ROTATED["starter_code"],
                reference_pseudocode=SEARCH_ROTATED["reference_pseudocode"],
                reference_pseudocode_variants=SEARCH_ROTATED["reference_pseudocode_variants"],
                reference_talking_points=SEARCH_ROTATED["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Search in Rotated Sorted Array")
        else:
            problem.description = SEARCH_ROTATED["description"]
            problem.difficulty = SEARCH_ROTATED["difficulty"]
            problem.category = SEARCH_ROTATED["category"]
            problem.starter_code = SEARCH_ROTATED["starter_code"]
            problem.reference_pseudocode = SEARCH_ROTATED["reference_pseudocode"]
            problem.reference_pseudocode_variants = SEARCH_ROTATED["reference_pseudocode_variants"]
            problem.reference_talking_points = SEARCH_ROTATED["reference_talking_points"]
            problem.slug = SEARCH_ROTATED["slug"]
            db.flush()
            print("Updated problem: Search in Rotated Sorted Array")

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
    seed_search_rotated()
