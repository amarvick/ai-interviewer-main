"""
Seed script for the "Group Anagrams" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_group_anagrams.py
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
        "id": "sorted_key_map",
        "title": "Sort each word and bucket by signature",
        "pseudocode": """1. Initialize dict groups = {}  // key -> list of strings
2. For each word in strs:
       key = "".join(sorted(word))
       groups.setdefault(key, []).append(word)
3. Return list(groups.values())
Time: O(n * k log k) where k is average word length.""",
        "complexity": "O(n * k log k) time, O(nk) space",
        "is_optimal": False,
        "notes": "Common baseline. Sorting each word dominates cost.",
        "match_signals": [
            "sorted(",
            "Arrays.sort",
            "\"\".join",
        ],
        "strengths": [
            "Straightforward reasoning and easy to implement.",
        ],
        "improvements": [
            "Discuss scaling issues when strings are long (sorting cost).",
            "Mention why stable ordering of groups is unspecified.",
        ],
    },
    {
        "id": "frequency_signature",
        "title": "Character frequency signature (optimal)",
        "pseudocode": """1. Initialize dict groups = {}
2. For each word:
       counts = [0] * 26
       for char in word:
           counts[ord(char) - ord('a')] += 1
       key = tuple(counts)
       groups.setdefault(key, []).append(word)
3. Return list(groups.values())
Time: O(n * k). Space: O(nk).""",
        "complexity": "O(n * k) time, O(nk) space",
        "is_optimal": True,
        "notes": "Avoids per-word sorting; handles length 0 words gracefully.",
        "match_signals": [
            "[0] * 26",
            "tuple(counts)",
            "freq[ord",
        ],
        "strengths": [
            "Linear in the total characters, which beats sorting on longer strings.",
            "Stable canonical key ensures identical words map together.",
        ],
        "improvements": [
            "Explain memory considerations when storing many tuples.",
            "Call out how to adapt for Unicode by using maps instead of fixed arrays.",
        ],
    },
    {
        "id": "prime_hash_signature",
        "title": "Prime multiplication hash",
        "pseudocode": """1. Assign each letter a unique prime number
2. For each word, compute product of primes for its letters
3. Use the product as key in groups dict
Time: O(n * k) but be careful about overflow.""",
        "complexity": "O(n * k) time, O(n) space",
        "is_optimal": False,
        "notes": "Interesting interview discussion but risk of overflow / collisions.",
        "match_signals": [
            "primes",
            "product",
            "unique factors",
        ],
        "strengths": [
            "Demonstrates creativity using number theory for hashing.",
        ],
        "improvements": [
            "Address overflow and floating point issues explicitly.",
            "Clarify why a more deterministic signature (sorted or counts) is safer.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "key_design",
        "title": "Designing a canonical key",
        "description": "Explain why anagrams share the same signature (sorted string, frequency tuple) and how collisions are avoided.",
        "bonus_mentions": [
            "canonical representation",
            "hashable tuple",
            "avoid collisions",
        ],
    },
    {
        "id": "time_complexity_tradeoffs",
        "title": "Sorting vs counting complexity",
        "description": "Compare the O(k log k) sort per word with the O(k) frequency count and when each is preferable.",
        "bonus_mentions": [
            "long words vs short words",
            "alphabet size",
            "space-speed balance",
        ],
    },
    {
        "id": "handling_edge_cases",
        "title": "Edge cases: empty strings, single letters, large groups",
        "description": "Call out how empty strings still form a valid group and why dictionary iteration order doesn’t matter for output.",
        "bonus_mentions": [
            "empty string bucket",
            "output ordering",
            "large groups memory",
        ],
    },
]

GROUP_ANAGRAMS = {
    "slug": "group-anagrams",
    "title": "Group Anagrams",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Medium",
    "description": """Given an array of strings `strs`, group the anagrams together. You can return the groups in any order.

Example 1
```
Input: ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

Example 2
```
Input: [""]
Output: [[""]]
```

Example 3
```
Input: ["a"]
Output: [["a"]]
```

Constraints
- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.
""",
    "starter_code": {
        "python": """class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Write your code here
        return []
""",
        "javascript": """class Solution {
  /**
   * @param {string[]} strs
   * @return {string[][]}
   */
  groupAnagrams = function(strs) {
    // Write your code here
    return [];
  };
}

module.exports = { Solution };
""",
        "java": """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        // Write your code here
        return List.of();
    }
}
""",
        "cpp": """class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        // Write your code here
        return {};
    }
};
""",
    },
    "reference_pseudocode": """Goal: group anagrams by a shared signature.

1. Initialize dictionary groups = {}
2. For each word in strs:
       counts = [0] * 26
       for char in word:
           counts[ord(char) - ord('a')] += 1
       key = tuple(counts)
       groups.setdefault(key, []).append(word)
3. Return list(groups.values())

Time Complexity: O(n * k) where k is average length. Space Complexity: O(nk).
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


def seed_group_anagrams() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == GROUP_ANAGRAMS["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == GROUP_ANAGRAMS["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=GROUP_ANAGRAMS["slug"],
                title=GROUP_ANAGRAMS["title"],
                description=GROUP_ANAGRAMS["description"],
                difficulty=GROUP_ANAGRAMS["difficulty"],
                category=GROUP_ANAGRAMS["category"],
                starter_code=GROUP_ANAGRAMS["starter_code"],
                reference_pseudocode=GROUP_ANAGRAMS["reference_pseudocode"],
                reference_pseudocode_variants=GROUP_ANAGRAMS["reference_pseudocode_variants"],
                reference_talking_points=GROUP_ANAGRAMS["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Group Anagrams")
        else:
            problem.description = GROUP_ANAGRAMS["description"]
            problem.difficulty = GROUP_ANAGRAMS["difficulty"]
            problem.category = GROUP_ANAGRAMS["category"]
            problem.starter_code = GROUP_ANAGRAMS["starter_code"]
            problem.reference_pseudocode = GROUP_ANAGRAMS["reference_pseudocode"]
            problem.reference_pseudocode_variants = GROUP_ANAGRAMS["reference_pseudocode_variants"]
            problem.reference_talking_points = GROUP_ANAGRAMS["reference_talking_points"]
            problem.slug = GROUP_ANAGRAMS["slug"]
            db.flush()
            print("Updated problem: Group Anagrams")

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
    seed_group_anagrams()
