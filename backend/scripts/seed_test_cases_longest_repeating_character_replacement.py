"""
Seed script for test cases for the "Longest Repeating Character Replacement" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_test_cases_longest_repeating_character_replacement.py
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


TARGET_PROBLEM_SLUG = "longest-repeating-character-replacement"
TARGET_PROBLEM_TITLE = "Longest Repeating Character Replacement"

LONGEST_REPEATING_TEST_CASES = [
    {
        "params": {"s": "ABAB", "k": 2},
        "expected_output": 4,
        "is_hidden": False,
    },
    {
        "params": {"s": "AABABBA", "k": 1},
        "expected_output": 4,
        "is_hidden": False,
    },
    {
        "params": {"s": "AAAA", "k": 0},
        "expected_output": 4,
        "is_hidden": False,
    },
    {
        "params": {"s": "ABCDE", "k": 1},
        "expected_output": 2,
        "is_hidden": False,
    },
    {
        "params": {"s": "ABCDE", "k": 4},
        "expected_output": 5,
        "is_hidden": False,
    },
    {
        "params": {"s": "BAAAB", "k": 2},
        "expected_output": 5,
        "is_hidden": False,
    },
    {
        "params": {"s": "ABBB", "k": 2},
        "expected_output": 4,
        "is_hidden": False,
    },
    {
        "params": {"s": "ABCABCABC", "k": 3},
        "expected_output": 6,
        "is_hidden": False,
    },
    {
        "params": {"s": "Z", "k": 0},
        "expected_output": 1,
        "is_hidden": False,
    },
    {
        "params": {"s": "ABAA", "k": 0},
        "expected_output": 2,
        "is_hidden": False,
    },
    {
        "params": {"s": "ABCD" * 25000, "k": 2},
        "expected_output": 3,
        "is_hidden": True,
    },
    {
        "params": {"s": "A" * 50000 + "B" * 50000, "k": 50000},
        "expected_output": 100000,
        "is_hidden": True,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_longest_repeating_test_cases() -> None:
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
                "Longest Repeating Character Replacement problem not found. Seed it first via scripts/seed_problem_longest_repeating_character_replacement.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in LONGEST_REPEATING_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in LONGEST_REPEATING_TEST_CASES:
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
    seed_longest_repeating_test_cases()
