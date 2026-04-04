"""
Seed script for test cases for the "Longest Substring Without Repeating Characters" problem.

Run from repo root:
    python backend/scripts/seed_test_cases_longest_substring_without_repeating_characters.py
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


TARGET_PROBLEM_SLUG = "longest-substring-without-repeating-characters"
TARGET_PROBLEM_TITLE = "Longest Substring Without Repeating Characters"

LONGEST_SUBSTRING_TEST_CASES = [
    {
        "params": {"s": "abcabcbb"},
        "expected_output": 3,
        "is_hidden": False,
    },
    {
        "params": {"s": "bbbbb"},
        "expected_output": 1,
        "is_hidden": False,
    },
    {
        "params": {"s": "pwwkew"},
        "expected_output": 3,
        "is_hidden": False,
    },
    {
        "params": {"s": ""},
        "expected_output": 0,
        "is_hidden": False,
    },
    {
        "params": {"s": " "},
        "expected_output": 1,
        "is_hidden": False,
    },
    {
        "params": {"s": "dvdf"},
        "expected_output": 3,
        "is_hidden": False,
    },
    {
        "params": {"s": "anviaj"},
        "expected_output": 5,
        "is_hidden": False,
    },
    {
        "params": {"s": "abba"},
        "expected_output": 2,
        "is_hidden": False,
    },
    {
        "params": {"s": "tmmzuxt"},
        "expected_output": 5,
        "is_hidden": False,
    },
    {
        "params": {"s": "abcdefghijklmnopqrstuvwxyz"},
        "expected_output": 26,
        "is_hidden": False,
    },
    {
        "params": {"s": "a" * 50000},
        "expected_output": 1,
        "is_hidden": True,
    },
    {
        "params": {"s": ("abcde" * 10000) + "xyz"},
        "expected_output": 5,
        "is_hidden": True,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_longest_substring_test_cases() -> None:
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
                "Longest Substring Without Repeating Characters problem not found. Seed the problem first via scripts/seed_problem_longest_substring_without_repeating_characters.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in LONGEST_SUBSTRING_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in LONGEST_SUBSTRING_TEST_CASES:
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
    seed_longest_substring_test_cases()
