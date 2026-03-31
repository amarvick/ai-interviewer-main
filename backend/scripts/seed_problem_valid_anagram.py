"""
Seed script for the "Valid Anagram" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_valid_anagram.py
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
        "id": "frequency_counter_hash_map",
        "title": "Single-pass frequency counter",
        "pseudocode": """1. If len(s) != len(t): return False
2. Initialize counts = {}  // char -> difference
3. For each index i:
       counts[s[i]] = counts.get(s[i], 0) + 1
       counts[t[i]] = counts.get(t[i], 0) - 1
4. Return True if all counts.values() == 0
Time: O(n). Space: O(k) distinct characters.""",
        "complexity": "O(n) time, O(k) space (O(1) for lowercase a-z)",
        "is_optimal": True,
        "notes": "Works for unicode and streams because it processes both strings in lockstep.",
        "match_signals": [
            "Counter(",
            "collections.Counter",
            "dict(",
            "HashMap",
            "defaultdict",
        ],
        "strengths": [
            "Matches character frequencies in a single pass, so it scales linearly.",
            "Handles arbitrary character sets (including Unicode) without extra branching.",
        ],
        "improvements": [
            "Call out why decrementing for `t` in the same loop keeps memory bounded.",
            "Mention that early exits can happen if a count becomes negative mid-scan.",
        ],
    },
    {
        "id": "sorted_comparison",
        "title": "Sort and compare",
        "pseudocode": """1. If len(s) != len(t): return False
2. Return sorted(s) == sorted(t)
Time: O(n log n). Space: O(n) for the sorted copies.""",
        "complexity": "O(n log n) time, O(n) space",
        "is_optimal": False,
        "notes": "Simple to reason about but slower than frequency counting.",
        "match_signals": [
            "sorted(",
            "sort(",
            "Arrays.sort",
            "std::sort",
        ],
        "strengths": [
            "Easy to implement and reason about for quick correctness.",
        ],
        "improvements": [
            "Discuss why sorting loses the O(n) runtime and how that impacts large inputs.",
            "Note that sorting destroys original order, which matters if indices are needed.",
        ],
    },
    {
        "id": "fixed_array_frequency",
        "title": "Fixed-size frequency array",
        "pseudocode": """1. If len(s) != len(t): return False
2. counts = [0] * 26
3. For each char in s: counts[ord(char) - ord('a')] += 1
4. For each char in t: counts[ord(char) - ord('a')] -= 1
5. Return all(count == 0 for count in counts)
Time: O(n). Space: O(1) for lowercase English letters.""",
        "complexity": "O(n) time, O(1) space (lowercase assumption)",
        "is_optimal": True,
        "notes": "Fastest constant factors when constraints guarantee lowercase a-z.",
        "match_signals": [
            "[0] * 26",
            "vector<int>(26",
            "new int[26]",
        ],
        "strengths": [
            "Leverages the limited alphabet to keep memory constant.",
            "Demonstrates attention to constraint-driven optimizations.",
        ],
        "improvements": [
            "Mention how this needs to change for full Unicode support.",
            "Call out why using indices instead of hash maps reduces overhead.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "frequency_balance",
        "title": "Frequency balance argument",
        "description": "Explain why matching counts per character is both necessary and sufficient for anagrams.",
        "bonus_mentions": [
            "injective mapping",
            "canceling counts",
            "stream processing",
        ],
    },
    {
        "id": "sorting_tradeoffs",
        "title": "Sorting versus hashing",
        "description": "Compare O(n log n) sorting with O(n) counting, including memory and stability implications.",
        "bonus_mentions": [
            "time/space trade-off",
            "n log n",
            "lexicographic order",
        ],
    },
    {
        "id": "unicode_extension",
        "title": "Unicode and arbitrary alphabets",
        "description": "Discuss how to adapt the solution when inputs include Unicode—e.g., using map-based counts or normalization.",
        "bonus_mentions": [
            "code points",
            "normalization",
            "defaultdict",
        ],
    },
]

VALID_ANAGRAM = {
    "slug": "valid-anagram",
    "title": "Valid Anagram",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Easy",
    "description": """Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.

Two strings are anagrams if they use the same characters with the same multiplicities (order does not matter).

Example 1
```
Input: s = "anagram", t = "nagaram"
Output: true
```

Example 2
```
Input: s = "rat", t = "car"
Output: false
```

Constraints
- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

Follow-up
- How would you handle Unicode characters where the alphabet is much larger?
""",
    "starter_code": {
        "python": """class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Write your code here
        return False
""",
        "javascript": """class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {boolean}
   */
  isAnagram = function(s, t) {
    // Write your code here
    return false;
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public boolean isAnagram(String s, String t) {
        // Write your code here
        return false;
    }
}
""",
        "cpp": """class Solution {
public:
    bool isAnagram(const string& s, const string& t) {
        // Write your code here
        return false;
    }
};
""",
    },
    "reference_pseudocode": """Goal: confirm two strings are anagrams by comparing character counts.

1. If lengths differ, return False immediately.
2. Initialize a frequency counter (hash map or fixed array).
3. Increment counts for characters in s while decrementing for characters in t.
4. Return False if any count deviates from zero; otherwise return True.
Time: O(n), Space: O(k) for alphabet size (O(1) for lowercase English letters).
Follow-up: switch the counter to a defaultdict or Counter to handle arbitrary Unicode code points.
""",
    "reference_pseudocode_variants": REFERENCE_VARIANTS,
    "reference_talking_points": REFERENCE_TALKING_POINTS,
}

TARGET_LIST_IDS = ("blind_75", "taro_75", "neetcode_150", "grind_169", "google_50")


def seed_valid_anagram() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == VALID_ANAGRAM["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem).filter(Problem.title == VALID_ANAGRAM["title"]).first()
            )

        if problem is None:
            problem = Problem(
                slug=VALID_ANAGRAM["slug"],
                title=VALID_ANAGRAM["title"],
                description=VALID_ANAGRAM["description"],
                difficulty=VALID_ANAGRAM["difficulty"],
                category=VALID_ANAGRAM["category"],
                starter_code=VALID_ANAGRAM["starter_code"],
                reference_pseudocode=VALID_ANAGRAM["reference_pseudocode"],
                reference_pseudocode_variants=VALID_ANAGRAM["reference_pseudocode_variants"],
                reference_talking_points=VALID_ANAGRAM["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Valid Anagram")
        else:
            problem.description = VALID_ANAGRAM["description"]
            problem.difficulty = VALID_ANAGRAM["difficulty"]
            problem.category = VALID_ANAGRAM["category"]
            problem.starter_code = VALID_ANAGRAM["starter_code"]
            problem.reference_pseudocode = VALID_ANAGRAM["reference_pseudocode"]
            problem.reference_pseudocode_variants = VALID_ANAGRAM["reference_pseudocode_variants"]
            problem.reference_talking_points = VALID_ANAGRAM["reference_talking_points"]
            problem.slug = VALID_ANAGRAM["slug"]
            db.flush()
            print("Updated problem: Valid Anagram")

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
    seed_valid_anagram()
