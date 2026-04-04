"""
Seed script for test cases for the "Find Minimum in Rotated Sorted Array" problem.

Run:
    python scripts/seed_test_cases_find_min_rotated_sorted_array.py
"""

from pathlib import Path
import json
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.database import Base, SessionLocal, engine
from app.db.models import Problem, TestCase
import app.db.models  # noqa: F401


TARGET_PROBLEM_SLUG = "find-minimum-in-rotated-sorted-array"
TARGET_PROBLEM_TITLE = "Find Minimum in Rotated Sorted Array"

FIND_MIN_TEST_CASES = [
    {"params": {"nums": [3, 4, 5, 1, 2]}, "expected_output": 1, "is_hidden": False},
    {"params": {"nums": [4, 5, 6, 7, 0, 1, 2]}, "expected_output": 0, "is_hidden": False},
    {"params": {"nums": [11, 13, 15, 17]}, "expected_output": 11, "is_hidden": False},
    {"params": {"nums": [1]}, "expected_output": 1, "is_hidden": False},
    {"params": {"nums": [2, 1]}, "expected_output": 1, "is_hidden": False},
    {"params": {"nums": [5, 6, 7, 1, 2, 3, 4]}, "expected_output": 1, "is_hidden": False},
    {"params": {"nums": [6, 7, 8, 9, 1, 2, 3, 4, 5]}, "expected_output": 1, "is_hidden": False},
    {"params": {"nums": [30, 40, 50, 10, 20]}, "expected_output": 10, "is_hidden": False},
    {"params": {"nums": [2, 3, 4, 5, 6, 7, 8, 9, 1]}, "expected_output": 1, "is_hidden": False},
    {"params": {"nums": list(range(1000))}, "expected_output": 0, "is_hidden": True},
    {"params": {"nums": list(range(500, 1000)) + list(range(500))}, "expected_output": 0, "is_hidden": True},
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_find_min_test_cases() -> None:
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
                "Find Minimum in Rotated Sorted Array problem not found. Seed the problem first."
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_keys = {_params_key(case["params"]) for case in FIND_MIN_TEST_CASES}

        inserted = updated = skipped = deleted = 0

        for case in FIND_MIN_TEST_CASES:
            key = _params_key(case["params"])
            current = existing_by_params.get(key)
            if current is None:
                db.add(
                    TestCase(
                        problem_id=problem.id,
                        params=case["params"],
                        expected_output=case["expected_output"],
                        is_hidden=case["is_hidden"],
                    )
                )
                inserted += 1
                continue

            changed = False
            if current.expected_output != case["expected_output"]:
                current.expected_output = case["expected_output"]
                changed = True
            if bool(current.is_hidden) != bool(case["is_hidden"]):
                current.is_hidden = case["is_hidden"]
                changed = True

            if changed:
                updated += 1
            else:
                skipped += 1

        for current in existing:
            key = _params_key(current.params)
            if key not in seed_keys:
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
    seed_find_min_test_cases()
