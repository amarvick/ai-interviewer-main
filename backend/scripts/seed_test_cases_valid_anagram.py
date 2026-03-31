"""
Seed script for test cases for the "Valid Anagram" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_test_cases_valid_anagram.py
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


TARGET_PROBLEM_SLUG = "valid-anagram"
TARGET_PROBLEM_TITLE = "Valid Anagram"

VALID_ANAGRAM_TEST_CASES = [
    {
        "params": {"s": "anagram", "t": "nagaram"},
        "expected_output": True,
        "is_hidden": False,
    },
    {
        "params": {"s": "rat", "t": "car"},
        "expected_output": False,
        "is_hidden": False,
    },
    {
        "params": {"s": "a", "t": "a"},
        "expected_output": True,
        "is_hidden": False,
    },
    {
        "params": {"s": "aa", "t": "a"},
        "expected_output": False,
        "is_hidden": False,
    },
    {
        "params": {"s": "aaaabbbbcccc", "t": "bcabcabcabca"},
        "expected_output": True,
        "is_hidden": True,
    },
    {
        "params": {"s": "你好世界", "t": "界世好你"},
        "expected_output": True,
        "is_hidden": True,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def seed_valid_anagram_test_cases() -> None:
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
                "Valid Anagram problem not found. Seed the problem first via scripts/seed_problem_valid_anagram.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in VALID_ANAGRAM_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in VALID_ANAGRAM_TEST_CASES:
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
    seed_valid_anagram_test_cases()
