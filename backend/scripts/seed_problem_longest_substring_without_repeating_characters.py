"""
Seed script for the "Longest Substring Without Repeating Characters" problem.

Run from repo root:
    python backend/scripts/seed_problem_longest_substring_without_repeating_characters.py
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
        "id": "sliding_window_last_seen",
        "title": "Sliding window with last-seen indices",
        "pseudocode": """1. last_seen = {}  // char -> last index
2. left = 0, best = 0
3. For right, ch in enumerate(s):
       if ch in last_seen and last_seen[ch] >= left:
           left = last_seen[ch] + 1
       last_seen[ch] = right
       best = max(best, right - left + 1)
4. Return best
Time: O(n). Space: O(min(n, alphabet_size)).""",
        "complexity": "O(n) time, O(min(n, alphabet)) space",
        "is_optimal": True,
        "notes": "Standard approach using hash map to keep window unique.",
        "match_signals": [
            "left = max(left",
            "last_seen",
            "window",
        ],
        "strengths": [
            "Handles arbitrary ASCII because dictionary grows with unique chars only.",
        ],
        "improvements": [
            "Mention using array of size 128/256 when input limited to ASCII.",
        ],
    },
    {
        "id": "sliding_window_frequency",
        "title": "Sliding window with frequency set",
        "pseudocode": """1. seen = set(), left = 0, best = 0
2. For right in range(len(s)):
       while s[right] in seen:
           seen.remove(s[left]); left += 1
       seen.add(s[right])
       best = max(best, right - left + 1)
Time: O(n).""",
        "complexity": "O(n) time, O(min(n, alphabet)) space",
        "is_optimal": False,
        "notes": "Same complexity but uses set removal loop; good for explaining window invariants.",
        "match_signals": [
            "while s[right] in seen",
            "seen.add",
        ],
        "strengths": [
            "Demonstrates classic sliding window template.",
        ],
        "improvements": [
            "Explain why removing characters one by one keeps invariants.",
        ],
    },
    {
        "id": "brute_force_substring_check",
        "title": "Brute-force check all substrings",
        "pseudocode": """Enumerate all substrings and verify uniqueness with a set.
Time: O(n^3) worst case.""",
        "complexity": "O(n^3) time, O(n) space",
        "is_optimal": False,
        "notes": "Baseline reasoning; quickly dismissed for n up to 5e4.",
        "match_signals": [
            "for i in range(n)",
            "for j in range(i, n)",
        ],
        "strengths": [
            "Helps motivate sliding window optimization.",
        ],
        "improvements": [
            "Highlight why it times out for large strings.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "window_invariant",
        "title": "Sliding window invariant",
        "description": "Explain that the window defined by [left, right] always has unique characters, so its length is a candidate answer.",
        "bonus_mentions": [
            "shrink on duplicate",
            "monotonic left pointer",
        ],
    },
    {
        "id": "last_seen_vs_set",
        "title": "Why last-seen index is more efficient",
        "description": "Discuss how jumping `left` past duplicates avoids popping the set one-by-one, especially with repeated blocks.",
        "bonus_mentions": [
            "O(1) jump",
            "hash map of indices",
        ],
    },
    {
        "id": "alphabet_considerations",
        "title": "Handling arbitrary ASCII characters",
        "description": "Call out that because s may include digits/symbols/spaces, using a dictionary (or array of size 128/256) keeps memory bounded.",
        "bonus_mentions": [
            "ASCII table",
            "Space complexity",
        ],
    },
]

LONGEST_SUBSTRING = {
    "slug": "longest-substring-without-repeating-characters",
    "title": "Longest Substring Without Repeating Characters",
    "category": "Sliding Window",
    "difficulty": "Medium",
    "description": """Given a string `s`, return the length of the longest substring without repeating characters.

Example 1
```
Input: "abcabcbb"
Output: 3  // "abc"
```

Example 2
```
Input: "bbbbb"
Output: 1
```

Example 3
```
Input: "pwwkew"
Output: 3  // "wke"
```

Constraints
- `0 <= s.length <= 5 * 10^4`
- `s` may contain English letters, digits, symbols, and spaces.
""",
    "starter_code": {
        "python": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Write your code here
        return 0
""",
        "javascript": """class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  lengthOfLongestSubstring = function(s) {
    // Write your code here
    return 0;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        // Write your code here
        return 0;
    }
}
""",
        "cpp": """class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // Write your code here
        return 0;
    }
};
""",
    },
    "reference_pseudocode": """1. last_seen = {}
2. left = 0, best = 0
3. For right, ch in enumerate(s):
       if ch in last_seen and last_seen[ch] >= left:
           left = last_seen[ch] + 1
       last_seen[ch] = right
       best = max(best, right - left + 1)
4. Return best

Time: O(n). Space: O(min(n, alphabet_size)).
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


def seed_longest_substring() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == LONGEST_SUBSTRING["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == LONGEST_SUBSTRING["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=LONGEST_SUBSTRING["slug"],
                title=LONGEST_SUBSTRING["title"],
                description=LONGEST_SUBSTRING["description"],
                difficulty=LONGEST_SUBSTRING["difficulty"],
                category=LONGEST_SUBSTRING["category"],
                starter_code=LONGEST_SUBSTRING["starter_code"],
                reference_pseudocode=LONGEST_SUBSTRING["reference_pseudocode"],
                reference_pseudocode_variants=LONGEST_SUBSTRING["reference_pseudocode_variants"],
                reference_talking_points=LONGEST_SUBSTRING["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Longest Substring Without Repeating Characters")
        else:
            problem.description = LONGEST_SUBSTRING["description"]
            problem.difficulty = LONGEST_SUBSTRING["difficulty"]
            problem.category = LONGEST_SUBSTRING["category"]
            problem.starter_code = LONGEST_SUBSTRING["starter_code"]
            problem.reference_pseudocode = LONGEST_SUBSTRING["reference_pseudocode"]
            problem.reference_pseudocode_variants = LONGEST_SUBSTRING["reference_pseudocode_variants"]
            problem.reference_talking_points = LONGEST_SUBSTRING["reference_talking_points"]
            problem.slug = LONGEST_SUBSTRING["slug"]
            db.flush()
            print("Updated problem: Longest Substring Without Repeating Characters")

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
    seed_longest_substring()
