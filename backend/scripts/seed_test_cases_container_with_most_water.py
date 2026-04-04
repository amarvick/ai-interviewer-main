"""
Seed script for test cases for the "Container With Most Water" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_test_cases_container_with_most_water.py
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


TARGET_PROBLEM_SLUG = "container-with-most-water"
TARGET_PROBLEM_TITLE = "Container With Most Water"

CONTAINER_TEST_CASES = [
    {
        "params": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]},
        "expected_output": 49,
        "is_hidden": False,
    },
    {
        "params": {"height": [1, 1]},
        "expected_output": 1,
        "is_hidden": False,
    },
    {
        "params": {"height": [4, 3, 2, 1, 4]},
        "expected_output": 16,
        "is_hidden": False,
    },
    {
        "params": {"height": [1, 2, 1]},
        "expected_output": 2,
        "is_hidden": False,
    },
    {
        "params": {"height": [0, 0, 0, 0, 0]},
        "expected_output": 0,
        "is_hidden": False,
    },
    {
        "params": {"height": [2, 3, 4, 5, 18, 17, 6]},
        "expected_output": 17 * 2,
        "is_hidden": False,
    },
    {
        "params": {"height": [2, 3, 10, 5, 7, 8, 9]},
        "expected_output": 36,
        "is_hidden": False,
    },
    {
        "params": {"height": [1] * 200},
        "expected_output": 199,
        "is_hidden": True,
    },
    {
        "params": {"height": list(range(1000))},
        "expected_output": 998 * 499,
        "is_hidden": True,
    },
    {
        "params": {"height": [0, 10000, 0, 0, 10000]},
        "expected_output": 40000,
        "is_hidden": False,
    },
    {
        "params": {"height": [1, 3, 2, 5, 25, 24, 5]},
        "expected_output": 24 * 4,
        "is_hidden": False,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_container_test_cases() -> None:
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
                "Container With Most Water problem not found. Seed the problem first via scripts/seed_problem_container_with_most_water.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in CONTAINER_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in CONTAINER_TEST_CASES:
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
    seed_container_test_cases()
