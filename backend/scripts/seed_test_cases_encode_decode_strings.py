"""
Seed script for test cases for the "Encode and Decode Strings" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_test_cases_encode_decode_strings.py
"""

from pathlib import Path
import json
import sys

# Ensure "app" package is importable when running as a script path.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.database import Base, SessionLocal, engine
from app.db.models import Problem, TestCase
import app.db.models  # noqa: F401


TARGET_PROBLEM_SLUG = "encode-decode-strings"
TARGET_PROBLEM_TITLE = "Encode and Decode Strings"

ENCODE_DECODE_TEST_CASES = [
    {
        "params": {"strs": ["yeah", "science"]},
        "expected_output": ["yeah", "science"],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["Tread", "lightly", "!"]},
        "expected_output": ["Tread", "lightly", "!"],
        "is_hidden": False,
    },
    {
        "params": {"strs": []},
        "expected_output": [],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["", "", ""]},
        "expected_output": ["", "", ""],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["multi_line\nvalue", "tabs\tand spaces", "final"]},
        "expected_output": ["multi_line\nvalue", "tabs\tand spaces", "final"],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["anchors#hashes", "pipes|and#hashes", "##"]},
        "expected_output": ["anchors#hashes", "pipes|and#hashes", "##"],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["emoji 😀", "雪", "مرحبا", "data"]},
        "expected_output": ["emoji 😀", "雪", "مرحبا", "data"],
        "is_hidden": True,
    },
    {
        "params": {"strs": ["0", "1", "2", "3" * 50]},
        "expected_output": ["0", "1", "2", "3" * 50],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["under_score", "double__underscore", "_leading"]},
        "expected_output": ["under_score", "double__underscore", "_leading"],
        "is_hidden": False,
    },
    {
        "params": {
            "strs": [
                "a" * 180,
                "b" * 50 + "#marker",
                "line with spaces",
                "",
            ]
        },
        "expected_output": [
            "a" * 180,
            "b" * 50 + "#marker",
            "line with spaces",
            "",
        ],
        "is_hidden": True,
    },
    {
        "params": {"strs": ["escape\\characters", "#", "\\#\\#"]},
        "expected_output": ["escape\\characters", "#", "\\#\\#"],
        "is_hidden": False,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def seed_encode_decode_test_cases() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        problem = (
            db.query(Problem)
            .filter(
                (Problem.slug == TARGET_PROBLEM_SLUG)
                | (Problem.title == TARGET_PROBLEM_TITLE)
            )
            .first()
        )
        if problem is None:
            raise RuntimeError(
                "Encode and Decode Strings problem not found. Seed the problem first via scripts/seed_problem_encode_decode_strings.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in ENCODE_DECODE_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in ENCODE_DECODE_TEST_CASES:
            key = _params_key(seed_case["params"])
            current = existing_by_params.get(key)
            if current is None:
                db.add(
                    TestCase(
                        problem_id=problem.id,
                        params=seed_case["params"],
                        expected_output=seed_case["expected_output"],
                        is_hidden=seed_case["is_hidden"],
                    )
                )
                inserted += 1
                continue

            changed = False
            if current.expected_output != seed_case["expected_output"]:
                current.expected_output = seed_case["expected_output"]
                changed = True
            if bool(current.is_hidden) != bool(seed_case["is_hidden"]):
                current.is_hidden = seed_case["is_hidden"]
                changed = True

            if changed:
                updated += 1
            else:
                skipped += 1

        for current in existing:
            key = _params_key(current.params)
            if key not in seed_params_keys:
                db.delete(current)
                deleted += 1

        db.commit()
        print(
            f"Done. Inserted: {inserted}, Updated: {updated}, "
            f"Skipped: {skipped}, Deleted stale: {deleted}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed_encode_decode_test_cases()
