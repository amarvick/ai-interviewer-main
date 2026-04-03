"""
Seed script for the "Longest Consecutive Sequence" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_longest_consecutive_sequence.py
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
        "id": "hash_set_sequence_scan",
        "title": "Hash-set sequence scan (optimal)",
        "pseudocode": """1. Put all nums into a set values
2. longest = 0
3. For each num in values:
       if num - 1 not in values:  # start of a chain
           length = 1
           while num + length in values:
               length += 1
           longest = max(longest, length)
4. Return longest
Time: O(n) average. Space: O(n).""",
        "complexity": "O(n) time (average), O(n) space",
        "is_optimal": True,
        "notes": "Only starts counting when num is the beginning of a sequence to avoid re-scanning interior elements.",
        "match_signals": [
            "set(",
            "unordered_set",
            "if num - 1 not in",
            "while current + 1 in",
        ],
        "strengths": [
            "Visits each value at most twice (insert + possible start check).",
            "Short-circuits chains by only iterating when at the start of a run.",
        ],
        "improvements": [
            "Call out why duplicates do not change complexity but require deduping via a set.",
            "Mention worst-case degenerate behavior if the hash set becomes imbalanced.",
        ],
    },
    {
        "id": "sort_and_sweep",
        "title": "Sort then sweep",
        "pseudocode": """1. If nums empty: return 0
2. Sort nums ascending
3. longest = 1, current = 1
4. For i from 1..n-1:
       if nums[i] == nums[i-1]: continue
       if nums[i] == nums[i-1] + 1:
           current += 1
           longest = max(longest, current)
       else:
           current = 1
5. Return longest
Time: O(n log n). Space: O(1) extra if sort in place.""",
        "complexity": "O(n log n) time, O(1) extra space (in-place sort)",
        "is_optimal": False,
        "notes": "Simple to reason about; often a candidate before optimizing.",
        "match_signals": [
            "sorted(",
            "sort(",
            "Arrays.sort",
        ],
        "strengths": [
            "Deterministic and easy to dry-run.",
        ],
        "improvements": [
            "Explain why sorting violates the strict O(n) requirement.",
            "Call out how to handle duplicates when sweeping.",
        ],
    },
    {
        "id": "disjoint_set_union",
        "title": "Union-Find (DSU)",
        "pseudocode": """1. Map each value to an index
2. Union an element with neighbors (num +/- 1) if present
3. Track max component size
Time: O(n α(n)). Space: O(n).""",
        "complexity": "O(n α(n)) time, O(n) space",
        "is_optimal": False,
        "notes": "Overkill for interviews but demonstrates graph thinking.",
        "match_signals": [
            "union",
            "parent",
            "find",
        ],
        "strengths": [
            "Shows ability to adapt DSU to range problems.",
        ],
        "improvements": [
            "Mention higher constant factors and complexity versus the hash-set scan.",
            "Clarify that DSU must dedupe inputs to avoid redundant unions.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "sequence_start_detection",
        "title": "Detecting sequence starts",
        "description": "Explain why only numbers without a predecessor should trigger the inner while-loop, which keeps the algorithm O(n).",
        "bonus_mentions": [
            "num - 1 not in set",
            "avoid re-counting",
            "linear time argument",
        ],
    },
    {
        "id": "hash_set_vs_sorting",
        "title": "Hashing versus sorting trade-offs",
        "description": "Compare the O(n) hashing approach with the simpler O(n log n) sorting solution, including memory and determinism considerations.",
        "bonus_mentions": [
            "deduplication",
            "space-speed trade-off",
            "constraints require linear time",
        ],
    },
    {
        "id": "handling_duplicates_and_negatives",
        "title": "Duplicates, negatives, and gaps",
        "description": "Call out that negative numbers and duplicates are naturally handled by the set, but failing to skip duplicates can inflate runtime.",
        "bonus_mentions": [
            "value ranges",
            "skip duplicates",
            "set lookup",
        ],
    },
]

LONGEST_CONSECUTIVE = {
    "slug": "longest-consecutive-sequence",
    "title": "Longest Consecutive Sequence",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Medium",
    "description": """Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must provide an algorithm that runs in O(n) time on average.

Example 1
```
Input: nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4].
```

Example 2
```
Input: nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9
```

Example 3
```
Input: nums = [1, 0, 1, 2]
Output: 3
```

Constraints
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
""",
    "starter_code": {
        "python": """class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # Write your code here
        return 0
""",
        "javascript": """class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  longestConsecutive = function(nums) {
    // Write your code here
    return 0;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int longestConsecutive(int[] nums) {
        // Write your code here
        return 0;
    }
}
""",
        "cpp": """class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        // Write your code here
        return 0;
    }
};
""",
    },
    "reference_pseudocode": """Goal: find the length of the longest consecutive run in O(n).

1. If nums empty: return 0
2. Insert every value into a hash set seen
3. best = 0
4. For each num in seen:
       if num - 1 not in seen:  # num starts a sequence
           current = 1
           while num + current in seen:
               current += 1
           best = max(best, current)
5. Return best

Time Complexity: O(n) average (each element is part of at most one inner loop). Space Complexity: O(n) for the set.
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


def seed_longest_consecutive() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == LONGEST_CONSECUTIVE["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == LONGEST_CONSECUTIVE["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=LONGEST_CONSECUTIVE["slug"],
                title=LONGEST_CONSECUTIVE["title"],
                description=LONGEST_CONSECUTIVE["description"],
                difficulty=LONGEST_CONSECUTIVE["difficulty"],
                category=LONGEST_CONSECUTIVE["category"],
                starter_code=LONGEST_CONSECUTIVE["starter_code"],
                reference_pseudocode=LONGEST_CONSECUTIVE["reference_pseudocode"],
                reference_pseudocode_variants=LONGEST_CONSECUTIVE["reference_pseudocode_variants"],
                reference_talking_points=LONGEST_CONSECUTIVE["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Longest Consecutive Sequence")
        else:
            problem.description = LONGEST_CONSECUTIVE["description"]
            problem.difficulty = LONGEST_CONSECUTIVE["difficulty"]
            problem.category = LONGEST_CONSECUTIVE["category"]
            problem.starter_code = LONGEST_CONSECUTIVE["starter_code"]
            problem.reference_pseudocode = LONGEST_CONSECUTIVE["reference_pseudocode"]
            problem.reference_pseudocode_variants = LONGEST_CONSECUTIVE["reference_pseudocode_variants"]
            problem.reference_talking_points = LONGEST_CONSECUTIVE["reference_talking_points"]
            problem.slug = LONGEST_CONSECUTIVE["slug"]
            db.flush()
            print("Updated problem: Longest Consecutive Sequence")

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
    seed_longest_consecutive()
