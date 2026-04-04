"""
Seed script for the "3Sum" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_three_sum.py
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
        "id": "sort_and_two_pointers",
        "title": "Sort + two-pointer scan",
        "pseudocode": """1. Sort nums ascending
2. results = []
3. For i from 0..n-3:
       if i > 0 and nums[i] == nums[i-1]: continue
       left = i + 1, right = n - 1
       while left < right:
           total = nums[i] + nums[left] + nums[right]
           if total == 0:
               add [nums[i], nums[left], nums[right]] to results
               left += 1; right -= 1
               skip duplicate nums[left] and nums[right]
           elif total < 0:
               left += 1
           else:
               right -= 1
4. Return results
Time: O(n^2). Space: O(1) extra (ignoring output).""",
        "complexity": "O(n^2) time, O(1) space",
        "is_optimal": True,
        "notes": "Best-known approach within constraints; deduplication is the tricky part.",
        "match_signals": [
            "sort",
            "left < right",
            "skip duplicates",
            "sum == 0",
        ],
        "strengths": [
            "Meets n ≤ 3000 constraint comfortably.",
            "Clear reasoning for duplicate skipping ensures unique triplets.",
        ],
        "improvements": [
            "Call out integer overflow risk in Java/C++ when adding three values near ±1e5.",
            "Mention early exits when nums[i] > 0 or when last values are negative.",
        ],
    },
    {
        "id": "hash_set_two_sum_extension",
        "title": "Hash-based two-sum extension per pivot",
        "pseudocode": """For each i, run two-sum on suffix using hash set to find pairs summing to -nums[i]. De-duplicate using sets of triplets.
Time: O(n^2) time, O(n) space.""",
        "complexity": "O(n^2) time, O(n) space",
        "is_optimal": False,
        "notes": "Alternative approach but deduplication is harder and constant factors higher.",
        "match_signals": [
            "seen set",
            "-nums[i]",
            "two sum",
        ],
        "strengths": [
            "Shows ability to adapt 2Sum to 3Sum.",
        ],
        "improvements": [
            "Explain how to avoid duplicate triplets when using sets.",
            "Discuss additional memory overhead.",
        ],
    },
    {
        "id": "brute_force_triple",
        "title": "Brute-force triple loops",
        "pseudocode": """Check every i<j<k, collect triplets that sum to zero using a set.
Time: O(n^3).""",
        "complexity": "O(n^3) time, O(n) space",
        "is_optimal": False,
        "notes": "Only feasible for very small arrays; good to mention as a baseline.",
        "match_signals": [
            "for i in range(n-2)",
            "for j in range(i+1, n-1)",
            "for k in range(j+1, n)",
        ],
        "strengths": [
            "Straightforward to implement.",
        ],
        "improvements": [
            "Use it to motivate sort + two-pointer optimization.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "duplicate_management",
        "title": "Handling duplicates",
        "description": "Explain why you must skip repeated pivots and skip repeated left/right values after finding a triplet.",
        "bonus_mentions": [
            "sorted order",
            "while left < right and nums[left] == nums[left-1]",
            "unique triplets requirement",
        ],
    },
    {
        "id": "complexity_bounds",
        "title": "Why O(n^2) is acceptable",
        "description": "Tie n ≤ 3000 to O(n^2) (~9e6 iterations) and contrast with O(n^3).",
        "bonus_mentions": [
            "n^2 ~ 9 million",
            "n^3 too slow",
            "two-pointer efficiency",
        ],
    },
    {
        "id": "early_exit_reasons",
        "title": "Early exits after sorting",
        "description": "Discuss optimizations like breaking when nums[i] > 0 or continuing when nums[i] + largest two < 0.",
        "bonus_mentions": [
            "sorted positives",
            "pruning negative sums",
            "micro-optimizations",
        ],
    },
]

THREE_SUM = {
    "slug": "three-sum",
    "title": "3Sum",
    "category": "Two Pointers",
    "difficulty": "Medium",
    "description": """Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` where `i < j < k` and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

Example 1
```
Input: [-1,0,1,2,-1,-4]
Output: [[-1,-1,2], [-1,0,1]]
```

Example 2
```
Input: [0,1,1]
Output: []
```

Example 3
```
Input: [0,0,0]
Output: [[0,0,0]]
```

Constraints
- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`
""",
    "starter_code": {
        "python": """class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Write your code here
        return []
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @return {number[][]}
   */
  threeSum = function(nums) {
    // Write your code here
    return [];
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        // Write your code here
        return List.of();
    }
}
""",
        "cpp": """class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        // Write your code here
        return {};
    }
};
""",
    },
    "reference_pseudocode": """Goal: enumerate all unique triplets summing to zero using sorting + two pointers.

1. Sort nums
2. results = []
3. For i from 0..n-3:
       if nums[i] > 0: break  # remaining values are >= nums[i]
       if i > 0 and nums[i] == nums[i-1]: continue
       left = i + 1, right = n - 1
       while left < right:
           total = nums[i] + nums[left] + nums[right]
           if total == 0:
               results.append([nums[i], nums[left], nums[right]])
               left += 1; right -= 1
               while left < right and nums[left] == nums[left-1]: left += 1
               while left < right and nums[right] == nums[right+1]: right -= 1
           elif total < 0:
               left += 1
           else:
               right -= 1
4. Return results

Time Complexity: O(n^2). Space Complexity: O(1) extra (output excluded).
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


def seed_three_sum() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == THREE_SUM["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == THREE_SUM["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=THREE_SUM["slug"],
                title=THREE_SUM["title"],
                description=THREE_SUM["description"],
                difficulty=THREE_SUM["difficulty"],
                category=THREE_SUM["category"],
                starter_code=THREE_SUM["starter_code"],
                reference_pseudocode=THREE_SUM["reference_pseudocode"],
                reference_pseudocode_variants=THREE_SUM["reference_pseudocode_variants"],
                reference_talking_points=THREE_SUM["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: 3Sum")
        else:
            problem.description = THREE_SUM["description"]
            problem.difficulty = THREE_SUM["difficulty"]
            problem.category = THREE_SUM["category"]
            problem.starter_code = THREE_SUM["starter_code"]
            problem.reference_pseudocode = THREE_SUM["reference_pseudocode"]
            problem.reference_pseudocode_variants = THREE_SUM["reference_pseudocode_variants"]
            problem.reference_talking_points = THREE_SUM["reference_talking_points"]
            problem.slug = THREE_SUM["slug"]
            db.flush()
            print("Updated problem: 3Sum")

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
    seed_three_sum()
