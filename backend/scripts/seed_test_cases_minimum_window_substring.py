"""
Seed script for test cases for the "Minimum Window Substring" problem.

Run (from repo root or backend/):
    python backend/scripts/seed_test_cases_minimum_window_substring.py
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


TARGET_PROBLEM_SLUG = "minimum-window-substring"
TARGET_PROBLEM_TITLE = "Minimum Window Substring"

MINIMUM_WINDOW_TEST_CASES = [
    {
        "params": {"s": "ADOBECODEBANC", "t": "ABC"},
        "expected_output": "BANC",
        "is_hidden": False,
    },
    {
        "params": {"s": "a", "t": "a"},
        "expected_output": "a",
        "is_hidden": False,
    },
    {
        "params": {"s": "a", "t": "aa"},
        "expected_output": "",
        "is_hidden": False,
    },
    {
        "params": {"s": "ab", "t": "b"},
        "expected_output": "b",
        "is_hidden": False,
    },
    {
        "params": {"s": "ab", "t": "a"},
        "expected_output": "a",
        "is_hidden": False,
    },
    {
        "params": {"s": "aa", "t": "aa"},
        "expected_output": "aa",
        "is_hidden": False,
    },
    {
        "params": {"s": "bba", "t": "ab"},
        "expected_output": "ba",
        "is_hidden": False,
    },
    {
        "params": {"s": "bdab", "t": "ab"},
        "expected_output": "ab",
        "is_hidden": False,
    },
    {
        "params": {"s": "xyyzyzyx", "t": "xyz"},
        "expected_output": "zyx",
        "is_hidden": False,
    },
    {
        "params": {"s": "aaaaaaaaaaaabbbbbcdd", "t": "abcdd"},
        "expected_output": "abbbbbcdd",
        "is_hidden": True,
    },
    {
        "params": {"s": "ABCDEF", "t": "FED"},
        "expected_output": "DEF",
        "is_hidden": False,
    },
    {
        "params": {"s": "ABBCZBAC", "t": "ABC"},
        "expected_output": "BAC",
        "is_hidden": False,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_minimum_window_test_cases() -> None:
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
                "Minimum Window Substring problem not found. Seed the problem first via scripts/seed_problem_minimum_window_substring.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in MINIMUM_WINDOW_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in MINIMUM_WINDOW_TEST_CASES:
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
    seed_minimum_window_test_cases()
