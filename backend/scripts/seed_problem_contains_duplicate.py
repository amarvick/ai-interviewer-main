"""
Seed script for the "Contains Duplicate" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_contains_duplicate.py
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
        "id": "hash_set_seen",
        "title": "Single-pass hash set",
        "pseudocode": """1. Initialize empty set seen
2. For each value num in nums:
     a. If num is in seen: return True
     b. Otherwise add num to seen
3. Return False (no duplicates)
Time: O(n). Space: O(n) in worst case.""",
        "complexity": "O(n) time, O(n) space",
        "is_optimal": True,
        "notes": "Works regardless of ordering; short-circuits on first duplicate.",
        "match_signals": [
            "set(",
            "HashSet",
            "unordered_set",
            "seen.add",
            "containsKey",
        ],
        "strengths": [
            "Detects duplicates in a single pass with early exit.",
            "Handles negative numbers and large value ranges without extra branching.",
        ],
        "improvements": [
            "Call out memory cost when the array has no duplicates.",
            "Mention that this pattern generalizes to streaming duplicate detection.",
        ],
    },
    {
        "id": "sort_and_scan",
        "title": "Sort then scan",
        "pseudocode": """1. Sort nums
2. For i from 1..n-1:
       if nums[i] == nums[i-1]: return True
3. Return False
Time: O(n log n). Space: O(1) if sort in place.""",
        "complexity": "O(n log n) time, O(1) extra space (if sort in place)",
        "is_optimal": False,
        "notes": "Easier to reason about but slower than hashing.",
        "match_signals": [
            "sorted(",
            "sort(",
            "Arrays.sort",
            "std::sort",
        ],
        "strengths": [
            "Simple to implement with minimal auxiliary memory.",
        ],
        "improvements": [
            "Explain why sorting mutates order and costs O(n log n).",
            "Mention when sorting is acceptable (e.g., output order doesn't matter).",
        ],
    },
    {
        "id": "brute_force_nested",
        "title": "Nested loop brute force",
        "pseudocode": """1. For each i from 0..n-1:
       For each j from i+1..n-1:
           if nums[i] == nums[j]: return True
2. Return False
Time: O(n^2). Space: O(1).""",
        "complexity": "O(n^2) time, O(1) space",
        "is_optimal": False,
        "notes": "Baseline approach; useful talk track for optimization.",
        "match_signals": [
            "for i in range",
            "for (int i",
            "while (i <",
        ],
        "strengths": [
            "Straightforward to reason about for very small inputs.",
        ],
        "improvements": [
            "Discuss why it fails to scale to 10^5 elements.",
            "Use it to motivate hash-based or sorting optimization.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "hash_set_tradeoff",
        "title": "Hash set versus memory",
        "description": "Explain why hashing gets O(n) time and when the extra memory is acceptable or not.",
        "bonus_mentions": [
            "space-speed trade-off",
            "early exit",
            "streaming duplicate detection",
        ],
    },
    {
        "id": "sorting_side_effects",
        "title": "Sorting side effects",
        "description": "Discuss how sorting changes order, costs O(n log n), and when that is fine versus harmful.",
        "bonus_mentions": [
            "in-place sort",
            "original order",
            "O(n log n) vs O(n)",
        ],
    },
    {
        "id": "frequency_map_extensions",
        "title": "Counting/frequency extensions",
        "description": "Talk about extending the pattern to count occurrences or find the first repeated value index pair.",
        "bonus_mentions": [
            "map counts",
            "first repeat index",
            "k-duplicates",
        ],
    },
]

CONTAINS_DUPLICATE = {
    "slug": "contains-duplicate",
    "title": "Contains Duplicate",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Easy",
    "description": """Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct.

Example 1
```
Input: nums = [1, 2, 3, 1]
Output: true
```

Example 2
```
Input: nums = [1, 2, 3, 4]
Output: false
```

Example 3
```
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
```

Constraints
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
""",
    "starter_code": {
        "python": """class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # Write your code here
        return False
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  containsDuplicate = function(nums) {
    // Write your code here
    return false;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        // Write your code here
        return false;
    }
}
""",
        "cpp": """class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        // Write your code here
        return false;
    }
};
""",
    },
    "reference_pseudocode": """Goal: detect if any value appears twice.

1. Initialize empty set seen
2. For each num in nums:
       if num in seen: return True
       seen.add(num)
3. Return False
Time: O(n) with hashing. Space: O(n) worst-case.
Alternative: sort and scan consecutive elements (O(n log n) time, O(1) extra space).
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
    "meta_50",
)


def seed_contains_duplicate() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == CONTAINS_DUPLICATE["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == CONTAINS_DUPLICATE["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=CONTAINS_DUPLICATE["slug"],
                title=CONTAINS_DUPLICATE["title"],
                description=CONTAINS_DUPLICATE["description"],
                difficulty=CONTAINS_DUPLICATE["difficulty"],
                category=CONTAINS_DUPLICATE["category"],
                starter_code=CONTAINS_DUPLICATE["starter_code"],
                reference_pseudocode=CONTAINS_DUPLICATE["reference_pseudocode"],
                reference_pseudocode_variants=CONTAINS_DUPLICATE["reference_pseudocode_variants"],
                reference_talking_points=CONTAINS_DUPLICATE["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Contains Duplicate")
        else:
            problem.description = CONTAINS_DUPLICATE["description"]
            problem.difficulty = CONTAINS_DUPLICATE["difficulty"]
            problem.category = CONTAINS_DUPLICATE["category"]
            problem.starter_code = CONTAINS_DUPLICATE["starter_code"]
            problem.reference_pseudocode = CONTAINS_DUPLICATE["reference_pseudocode"]
            problem.reference_pseudocode_variants = CONTAINS_DUPLICATE["reference_pseudocode_variants"]
            problem.reference_talking_points = CONTAINS_DUPLICATE["reference_talking_points"]
            problem.slug = CONTAINS_DUPLICATE["slug"]
            db.flush()
            print("Updated problem: Contains Duplicate")

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

            db.add(ProblemListProblem(problem_list_id=list_id, problem_id=problem.id))
            linked += 1

        db.commit()
        print(f"Done. Linked to lists: {linked}, Existing links skipped: {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_contains_duplicate()
