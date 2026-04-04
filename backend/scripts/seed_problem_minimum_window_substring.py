"""
Seed script for the "Minimum Window Substring" problem.

Run (from repo root or backend/):
    python backend/scripts/seed_problem_minimum_window_substring.py
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
        "id": "sliding_window_need_counts",
        "title": "Sliding window with need counts (optimal)",
        "pseudocode": """1. need = Counter(t); missing = len(t)
2. left = start = end = 0
3. For right, char in enumerate(s, 1):  # use 1-based right for slicing
       if need[char] > 0:
           missing -= 1
       need[char] -= 1
       while missing == 0:
           if end == 0 or right - left < end - start:
               start, end = left, right
           need[s[left]] += 1
           if need[s[left]] > 0:
               missing += 1
           left += 1
4. Return s[start:end]
Time: O(m + n). Space: O(1) for alphabet (52 for letters).""",
        "complexity": "O(m + n) time, O(1) space",
        "is_optimal": True,
        "notes": "Classic sliding window pattern that expands until window is valid and then shrinks.",
        "match_signals": [
            "need",
            "missing",
            "while missing == 0",
        ],
        "strengths": [
            "Demonstrates O(m+n) approach requested in follow-up.",
            "Handles duplicates because counts can go negative when extra chars present.",
        ],
        "improvements": [
            "Mention using array of size 128/256 instead of Counter for speed.",
            "Explain why we only update best window when valid.",
        ],
    },
    {
        "id": "two_pointer_deque",
        "title": "Filtered window using deque of relevant indices",
        "pseudocode": """Filter s to indices that contain chars from t, then run window on this compact list.
Time: O(m + n).""",
        "complexity": "O(m + n) time, O(m) space",
        "is_optimal": False,
        "notes": "Same complexity but more complicated; useful to highlight alternative viewpoint.",
        "match_signals": [
            "filtered_s",
            "deque",
        ],
        "strengths": [
            "Can speed up when s is very long and t is small.",
        ],
        "improvements": [
            "Clarify need for storing original indices to return substring.",
        ],
    },
    {
        "id": "brute_force_substring",
        "title": "Brute-force check all substrings",
        "pseudocode": """Enumerate all substrings of s and check if it contains t.
Time: O(m^2 * alphabet).""",
        "complexity": "O(m^2) or worse",
        "is_optimal": False,
        "notes": "Discussed only to motivate why sliding window is necessary.",
        "match_signals": [
            "for i in range(m)",
            "for j in range(i, m)",
        ],
        "strengths": [
            "Simple reasoning baseline.",
        ],
        "improvements": [
            "Explain infeasibility for m up to 1e5.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "window_validity_condition",
        "title": "Tracking when window satisfies all requirements",
        "description": "Explain how `missing` (or matched count) lets us know when the window covers t entirely.",
        "bonus_mentions": [
            "missing == 0",
            "all chars covered",
        ],
    },
    {
        "id": "shrink_then_expand",
        "title": "Expand to meet condition, shrink to optimize",
        "description": "Emphasize the pattern of expanding right until valid, then shrinking left to find minimal window.",
        "bonus_mentions": [
            "two pointers",
            "while-loop to shrink",
            "minimal substring",
        ],
    },
    {
        "id": "time_complexity_proof",
        "title": "Why O(m + n)",
        "description": "Note each pointer moves at most m steps; dictionary updates are O(1).",
        "bonus_mentions": [
            "no pointer moves backwards",
            "Counter operations constant",
        ],
    },
]

MINIMUM_WINDOW = {
    "slug": "minimum-window-substring",
    "title": "Minimum Window Substring",
    "category": "Sliding Window",
    "difficulty": "Hard",
    "description": """Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return an empty string.

Example 1
```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

Example 2
```
Input: s = "a", t = "a"
Output: "a"
```

Example 3
```
Input: s = "a", t = "aa"
Output: ""
```

Constraints
- `1 <= s.length, t.length <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.

Follow-up: Find an algorithm that runs in O(m + n) time.
""",
    "starter_code": {
        "python": """class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # Write your code here
        return ""
""",
        "javascript": """class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {string}
   */
  minWindow = function(s, t) {
    // Write your code here
    return "";
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public String minWindow(String s, String t) {
        // Write your code here
        return "";
    }
}
""",
        "cpp": """class Solution {
public:
    string minWindow(string s, string t) {
        // Write your code here
        return "";
    }
};
""",
    },
    "reference_pseudocode": """1. need = Counter(t), missing = len(t)
2. left = start = end = 0
3. For right, ch in enumerate(s, 1):
       if need[ch] > 0:
           missing -= 1
       need[ch] -= 1
       if missing == 0:
           while True:
               left_char = s[left]
               need[left_char] += 1
               left += 1
               if need[left_char] > 0:
                   break
           if end == 0 or right - (left - 1) < end - start:
               start, end = left - 1, right
           missing += 1
4. Return s[start:end]
Time: O(m + n). Space: O(1) for alphabet (52).""",
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


def seed_minimum_window_substring() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == MINIMUM_WINDOW["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == MINIMUM_WINDOW["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=MINIMUM_WINDOW["slug"],
                title=MINIMUM_WINDOW["title"],
                description=MINIMUM_WINDOW["description"],
                difficulty=MINIMUM_WINDOW["difficulty"],
                category=MINIMUM_WINDOW["category"],
                starter_code=MINIMUM_WINDOW["starter_code"],
                reference_pseudocode=MINIMUM_WINDOW["reference_pseudocode"],
                reference_pseudocode_variants=MINIMUM_WINDOW["reference_pseudocode_variants"],
                reference_talking_points=MINIMUM_WINDOW["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Minimum Window Substring")
        else:
            problem.description = MINIMUM_WINDOW["description"]
            problem.difficulty = MINIMUM_WINDOW["difficulty"]
            problem.category = MINIMUM_WINDOW["category"]
            problem.starter_code = MINIMUM_WINDOW["starter_code"]
            problem.reference_pseudocode = MINIMUM_WINDOW["reference_pseudocode"]
            problem.reference_pseudocode_variants = MINIMUM_WINDOW["reference_pseudocode_variants"]
            problem.reference_talking_points = MINIMUM_WINDOW["reference_talking_points"]
            problem.slug = MINIMUM_WINDOW["slug"]
            db.flush()
            print("Updated problem: Minimum Window Substring")

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
    seed_minimum_window_substring()
