"""
Seed script for the "Two Sum" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_two_sum.py
"""

from pathlib import Path
import sys

# Ensure "app" package is importable when running as a script path.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.database import Base, SessionLocal, engine
from app.db.models import Problem, ProblemList, ProblemListProblem
import app.db.models  # noqa: F401  # ensure all models are registered before create_all


TWO_SUM = {
    "title": "Two Sum",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Easy",
    "description": """Given an array of integers `nums` and an integer `target`, return indices `i` and `j` such that `nums[i] + nums[j] == target`. 

You may assume that exactly one valid pair exists and you may not use the same element twice.

You can return the answer in any order.


Example 1
```
Input: nums = [1, 2, 3, 6], target = 7
Output: [0, 3]
```

Example 2
```
Input: nums = [7, 3, 8, 2], target = 11
Output: [1, 2]
```

Example 3
```
Input: nums = [2, 2], target = 4
Output: [0, 1]
```

Constraints
- `2 <= nums.length <= 1000`
- `-10^7 <= nums[i] <= 10^7`
- `-10^7 <= target <= 10^7`
""",
    "starter_code": {
        "python": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number[]}
   */
  twoSum = function(nums, target) {
      
  };
}

// Please don’t remove below line of code
module.exports = { Solution };
""",
        "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        
    }
}
""",
        "cpp": """class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        
    }
};
""",
    },
    "reference_pseudocode": """Goal: Find indices of two numbers that sum to target; assume exactly one valid pair.

1. Initialize map seen_indices = {}  // value -> index
2. For each index i and value num in nums:
     a. complement = target - num
     b. If complement exists in seen_indices:
           return [seen_indices[complement], i]
     c. Otherwise store seen_indices[num] = i
3. If loop ends without return, no valid pair (should not happen per constraints).
Time: O(n). Space: O(n) for hash map.
Edge cases to discuss: negative numbers, duplicates, large arrays.
Cases to discuss IF the interviewer wants: what happens if we don't have a valid pair, or if we have less than two items. These kinds of questions that can push the interviewer to think a little more.
""",
}

# Add this problem to these existing seeded lists when they exist.
TARGET_LIST_IDS = ("blind_75", "taro_75", "neetcode_150", "google_50", "meta_50", "amazon_50", "apple_30", "microsoft_30")


def seed_two_sum() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = db.query(Problem).filter(Problem.title == TWO_SUM["title"]).first()

        if problem is None:
            problem = Problem(
                title=TWO_SUM["title"],
                description=TWO_SUM["description"],
                difficulty=TWO_SUM["difficulty"],
                category=TWO_SUM["category"],
                starter_code=TWO_SUM["starter_code"],
                reference_pseudocode=TWO_SUM["reference_pseudocode"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Two Sum")
        else:
            problem.description = TWO_SUM["description"]
            problem.difficulty = TWO_SUM["difficulty"]
            problem.category = TWO_SUM["category"]
            problem.starter_code = TWO_SUM["starter_code"]
            problem.reference_pseudocode = TWO_SUM["reference_pseudocode"]
            db.flush()
            print("Updated problem: Two Sum")

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
    seed_two_sum()
