"""
Seed script for the "Encode and Decode Strings" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_problem_encode_decode_strings.py
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
        "id": "length_prefixed_utf8",
        "title": "Length-prefixed UTF-8 buffer",
        "pseudocode": """Encoding
1. Initialize builder = []
2. For each string s in strs:
       bytes_s = utf8_encode(s)
       builder.append(f"{len(bytes_s)}#")
       builder.append(bytes_s_decoded_as_text)
3. Return "".join(builder)

Decoding
1. Initialize result = [], i = 0
2. While i < len(encoded):
       j = i
       while encoded[j] != '#': j += 1
       length = int(encoded[i:j])
       j += 1
       result.append(encoded[j : j + length])
       i = j + length
3. Return result
Time: O(total_chars). Space: O(total_chars).""",
        "complexity": "O(total_chars) time, O(total_chars) space",
        "is_optimal": True,
        "notes": "Works for any UTF-8 payload because counts are based on byte length instead of relying on delimiters.",
        "match_signals": [
            "len(s)",
            "length + '#'",
            "while i < len",
            "parse length",
            "two-pointer decode",
        ],
        "strengths": [
            "Handles arbitrary characters (including '#', underscores, emojis) without escaping.",
            "Streaming friendly because each chunk carries its byte length up front.",
        ],
        "improvements": [
            "Call out why byte-length parsing must stop at '#', not any digit.",
            "Mention how to avoid quadratic string concatenation by using builders.",
        ],
    },
    {
        "id": "escaped_delimiter_join",
        "title": "Delimiter join with escaping",
        "pseudocode": """Encoding
1. Choose delimiter = '#', escape_char = '\\\\'
2. For each s in strs:
       escaped = s.replace('\\\\', '\\\\\\\\').replace('#', '\\\\#')
       builder.append(escaped)
3. Return "#".join(builder)

Decoding
1. Scan chars, when '#' appears check if it is escaped (preceded by odd number of '\\\\')
2. Split accordingly and unescape.
Time: O(total_chars). Space: O(total_chars).""",
        "complexity": "O(total_chars) time, O(total_chars) space",
        "is_optimal": False,
        "notes": "Easier to explain but error-prone; escaping bugs are common during interviews.",
        "match_signals": [
            "replace",
            "escape_char",
            "split",
            "delimiter",
        ],
        "strengths": [
            "Leverages familiar join/split operations.",
        ],
        "improvements": [
            "Explain how escaping logic must be symmetric to avoid corrupt data.",
            "Discuss how nested escaping becomes harder for arbitrary byte sequences.",
        ],
    },
    {
        "id": "external_serialization",
        "title": "External serialization (JSON/Base64)",
        "pseudocode": """1. Serialize strings as JSON or MessagePack -> bytes_payload
2. Optionally Base64 encode bytes_payload to keep printable characters
3. Decode by reversing the serialization
Time: O(total_chars). Space: O(total_chars).""",
        "complexity": "O(total_chars) time, O(total_chars) space",
        "is_optimal": False,
        "notes": "Valid but relies on libraries; interviewers expect you to rebuild the primitive manually.",
        "match_signals": [
            "json.dumps",
            "base64",
            "pickle",
        ],
        "strengths": [
            "Fast to implement with built-in serializers.",
        ],
        "improvements": [
            "Highlight portability and security concerns (e.g., `eval`, `pickle`).",
            "Clarify that this avoids practicing lower-level encoding, so it's less ideal for interviews.",
        ],
    },
]

REFERENCE_TALKING_POINTS = [
    {
        "id": "delimiter_failures",
        "title": "Why naive delimiter-based schemes break",
        "description": "Discuss examples where underscore or comma separators fail once payloads contain the same character, leading to ambiguous decoding.",
        "bonus_mentions": [
            "double underscores",
            "escaping strategy",
            "round-trip guarantee",
        ],
    },
    {
        "id": "byte_length_vs_char_length",
        "title": "Byte length parsing for UTF-8",
        "description": "Highlight that counting encoded bytes avoids issues with multi-byte characters and ensures the consumer reads exact slices.",
        "bonus_mentions": [
            "UTF-8 code units",
            "emoji",
            "multi-byte safety",
        ],
    },
    {
        "id": "generalized_streaming",
        "title": "Generalized algorithm for arbitrary alphabets",
        "description": "Explain how the length-prefixed protocol generalizes to any alphabet, streams, or binary blobs without needing escaping.",
        "bonus_mentions": [
            "protocol buffers",
            "framing",
            "stream processing",
        ],
    },
]

ENCODE_DECODE = {
    "slug": "encode-decode-strings",
    "title": "Encode and Decode Strings",
    "category": "Arrays, Strings and Hashing",
    "difficulty": "Medium",
    "description": """Design an algorithm to encode a list of strings into a single string. Later, decode that single string back into the original list.

Implement two methods:
- `encode(strs: List[str]) -> str`
- `decode(s: str) -> List[str]`

The encoded output should always decode back to the exact original list, even if strings contain spaces, punctuation, or arbitrary UTF-8 characters.

Example 1
```
Input: ["yeah", "science"]
Encoding (one example): "4#yeah7#science"
Output after decode: ["yeah", "science"]
```

Example 2
```
Input: ["Tread", "lightly", "!"]
Encoding: "5#Tread8#lightly1#!"
Output after decode: ["Tread", "lightly", "!"]
```

Constraints
- `0 <= strs.length < 100`
- `0 <= strs[i].length < 200`
- `strs[i]` may contain any UTF-8 characters

Follow-up
- How would you generalize your approach to handle any possible set of characters or binary data streams?
""",
    "starter_code": {
        "python": """class Codec:
    def encode(self, strs: List[str]) -> str:
        # Write your code here
        return ""

    def decode(self, s: str) -> List[str]:
        # Write your code here
        return []
""",
        "javascript": """class Codec {
  /**
   * @param {string[]} strs
   * @return {string}
   */
  encode(strs) {
    // Write your code here
    return "";
  }

  /**
   * @param {string} s
   * @return {string[]}
   */
  decode(s) {
    // Write your code here
    return [];
  }
}

module.exports = { Codec };
""",
        "java": """public class Codec {
    // Encodes a list of strings to a single string.
    public String encode(List<String> strs) {
        // Write your code here
        return "";
    }

    // Decodes a single string to a list of strings.
    public List<String> decode(String s) {
        // Write your code here
        return List.of();
    }
}
""",
        "cpp": """class Codec {
public:
    // Encodes a list of strings to a single string.
    string encode(vector<string>& strs) {
        // Write your code here
        return "";
    }

    // Decodes a single string to a list of strings.
    vector<string> decode(string s) {
        // Write your code here
        return {};
    }
};
""",
    },
    "reference_pseudocode": """Goal: Encode/decode without ambiguity using length-prefixed chunks.

Encoding
1. Initialize builder = []
2. For each string s in strs:
       data = s (treated as UTF-8)
       builder.append(str(len(data)))
       builder.append('#')
       builder.append(data)
3. Return "".join(builder)

Decoding
1. Initialize result = [], i = 0
2. While i < len(encoded):
       j = i
       while encoded[j] != '#': j += 1
       length = int(encoded[i:j])
       j += 1
       result.append(encoded[j:j+length])
       i = j + length
3. Return result

Time Complexity: O(total_chars). Space Complexity: O(total_chars).
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


def seed_encode_decode_strings() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(Problem.slug == ENCODE_DECODE["slug"])
            .first()
        )
        if problem is None:
            problem = (
                db.query(Problem)
                .filter(Problem.title == ENCODE_DECODE["title"])
                .first()
            )

        if problem is None:
            problem = Problem(
                slug=ENCODE_DECODE["slug"],
                title=ENCODE_DECODE["title"],
                description=ENCODE_DECODE["description"],
                difficulty=ENCODE_DECODE["difficulty"],
                category=ENCODE_DECODE["category"],
                starter_code=ENCODE_DECODE["starter_code"],
                reference_pseudocode=ENCODE_DECODE["reference_pseudocode"],
                reference_pseudocode_variants=ENCODE_DECODE["reference_pseudocode_variants"],
                reference_talking_points=ENCODE_DECODE["reference_talking_points"],
            )
            db.add(problem)
            db.flush()
            print("Inserted problem: Encode and Decode Strings")
        else:
            problem.description = ENCODE_DECODE["description"]
            problem.difficulty = ENCODE_DECODE["difficulty"]
            problem.category = ENCODE_DECODE["category"]
            problem.starter_code = ENCODE_DECODE["starter_code"]
            problem.reference_pseudocode = ENCODE_DECODE["reference_pseudocode"]
            problem.reference_pseudocode_variants = ENCODE_DECODE["reference_pseudocode_variants"]
            problem.reference_talking_points = ENCODE_DECODE["reference_talking_points"]
            problem.slug = ENCODE_DECODE["slug"]
            db.flush()
            print("Updated problem: Encode and Decode Strings")

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
    seed_encode_decode_strings()
