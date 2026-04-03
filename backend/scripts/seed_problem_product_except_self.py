"""
Seed script for the "Product of Array Except Self" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_product_except_self.py
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
        "id": "prefix_suffix_two_arrays",
        "title": "Prefix + suffix arrays",
        "pseudocode": """1. Build prefix[i] = product of nums[0..i-1]
2. Build suffix[i] = product of nums[i+1..n-1]
3. answer[i] = prefix[i] * suffix[i]
Time: O(n). Space: O(n) for prefix + suffix.""",
        "complexity": "O(n) time, O(n) space",
        "is_optimal": False,
        "notes": "Clear starter approach; easy to reason about before optimizing space.",
        "match_signals": [
            "prefix",
            "suffix",
            "left_products",
            "right_products",
        ],
        "strengths": [
            "Separates concerns cleanly; easy to verify on paper.",
        ],
        "improvements": [
            "Explain how to compress prefix/suffix into one pass to save memory.",
            "Call out integer overflow considerations even though constraints guarantee fit.",
        ],
    },
    {
        "id": "prefix_suffix_in_place",
        "title": "In-place prefix/suffix accumulation",
        "pseudocode": """1. answer[i] = product of nums[0..i-1] via forward pass
2. Maintain running suffix product and multiply into answer[i] during backward pass
Time: O(n). Space: O(1) extra (excluding answer).""",
        "complexity": "O(n) time, O(1) extra space",
        "is_optimal": True,
        "notes": "Satisfies follow-up by reusing output array.",
        "match_signals": [
            "temp",
            "running_product",
            "suffix_product",
            "forward pass",
            "backward pass",
        ],
        "strengths": [
            "Demonstrates mastery of prefix/suffix pattern while keeping extra space constant.",
            "Naturally handles zeros by accumulating products separately per pass.",
        ],
        "improvements": [
            "Mention why two zeros force all outputs to zero.",
            "Call out the need to use 64-bit temporaries in languages with risky overflow.",
        ],
    },
    {
        "id": "division_plus_zero_guard",
        "title": "Division with zero handling",
        "pseudocode": """1. Compute total product and count zeros
2. If more than one zero: answer is all zeros
3. Else fill result using division or special-case zero position
Time: O(n). Space: O(1).""",
        "complexity": "O(n) time, O(1) space",
        "is_optimal": False,
        "notes": "Disallowed per prompt but worth contrasting.",
        "match_signals": [
            "total_product",
            "division",
            "zero_count",
        ],
        "strengths": [
            "Shows awareness of alternative strategies and their constraints.",
        ],
        "improvements": [
            "Point out that division violates the problem requirement.",
            "Use it as a stepping stone to the zero-safe prefix/suffix solution.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "zero_handling",
        "title": "Zero handling strategy",
        "description": "Explain how the algorithm adapts when the array contains one or two zeros.",
        "bonus_mentions": [
            "zero count",
            "single zero vs multiple",
            "suffix accumulation",
        ],
    },
    {
        "id": "space_optimization",
        "title": "Space optimization from O(n) to O(1)",
        "description": "Discuss converting prefix/suffix arrays into in-place multiplications with two passes.",
        "bonus_mentions": [
            "reuse output array",
            "forward/backward pass",
            "rolling product",
        ],
    },
    {
        "id": "overflow_considerations",
        "title": "Overflow and data types",
        "description": "Even though constraints fit 32-bit, mention when to use wider intermediates.",
        "bonus_mentions": [
            "long long",
            "bigint (if languages differ)",
            "intermediate cast",
        ],
    },
]

PRODUCT_EXCEPT_SELF = {
    "slug": "product-of-array-except-self",
    "title": "Product of Array Except Self",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Medium",
    "description": """Given an integer array `nums`, return an array `answer` such that `answer[i]` is the product of all elements of `nums` except `nums[i]`. The product of any prefix or suffix fits in 32-bit signed integer. Do not use division and run in O(n) time.

Example 1
```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

Example 2
```
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

Constraints
- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- Output is guaranteed to fit in 32-bit signed integer

Follow-up
- Solve with O(1) extra space (excluding the output array).
""",
    "starter_code": {
        "python": """class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # Write your code here
        return []
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  productExceptSelf = function(nums) {
    // Write your code here
    return [];
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        // Write your code here
        return new int[0];
    }
}
""",
        "cpp": """class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        // Write your code here
        return {};
    }
};
""",
    },
    "reference_pseudocode": """Goal: compute output[i] = product(nums) / nums[i] without division.

1. Initialize result array with 1s
2. Forward pass: keep running_prefix; result[i] = running_prefix; running_prefix *= nums[i]
3. Backward pass: keep running_suffix; result[i] *= running_suffix; running_suffix *= nums[i]
Time: O(n). Space: O(1) extra (result excluded).
Handles zeros because prefix/suffix multiplication naturally skips nums[i].
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


def seed_product_except_self() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == PRODUCT_EXCEPT_SELF["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == PRODUCT_EXCEPT_SELF["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=PRODUCT_EXCEPT_SELF["slug"],
                title=PRODUCT_EXCEPT_SELF["title"],
                description=PRODUCT_EXCEPT_SELF["description"],
                difficulty=PRODUCT_EXCEPT_SELF["difficulty"],
                category=PRODUCT_EXCEPT_SELF["category"],
                starter_code=PRODUCT_EXCEPT_SELF["starter_code"],
                reference_pseudocode=PRODUCT_EXCEPT_SELF["reference_pseudocode"],
                reference_pseudocode_variants=PRODUCT_EXCEPT_SELF["reference_pseudocode_variants"],
                reference_talking_points=PRODUCT_EXCEPT_SELF["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Product of Array Except Self")
        else:
            problem.description = PRODUCT_EXCEPT_SELF["description"]
            problem.difficulty = PRODUCT_EXCEPT_SELF["difficulty"]
            problem.category = PRODUCT_EXCEPT_SELF["category"]
            problem.starter_code = PRODUCT_EXCEPT_SELF["starter_code"]
            problem.reference_pseudocode = PRODUCT_EXCEPT_SELF["reference_pseudocode"]
            problem.reference_pseudocode_variants = PRODUCT_EXCEPT_SELF["reference_pseudocode_variants"]
            problem.reference_talking_points = PRODUCT_EXCEPT_SELF["reference_talking_points"]
            problem.slug = PRODUCT_EXCEPT_SELF["slug"]
            db.flush()
            print("Updated problem: Product of Array Except Self")

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
    seed_product_except_self()
