"""
Seed script for test cases for the "3Sum" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_test_cases_three_sum.py
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


TARGET_PROBLEM_SLUG = "three-sum"
TARGET_PROBLEM_TITLE = "3Sum"

THREE_SUM_TEST_CASES = [
    {
        "params": {"nums": [-1, 0, 1, 2, -1, -4]},
        "expected_output": [[-1, -1, 2], [-1, 0, 1]],
        "is_hidden": False,
    },
    {
        "params": {"nums": [0, 1, 1]},
        "expected_output": [],
        "is_hidden": False,
    },
    {
        "params": {"nums": [0, 0, 0]},
        "expected_output": [[0, 0, 0]],
        "is_hidden": False,
    },
    {
        "params": {"nums": [3, 0, -2, -1, 1, 2]},
        "expected_output": [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]],
        "is_hidden": False,
    },
    {
        "params": {"nums": [-2, 0, 1, 1, 2]},
        "expected_output": [[-2, 0, 2], [-2, 1, 1]],
        "is_hidden": False,
    },
    {
        "params": {"nums": [-4, -2, -2, -2, 0, 1, 2, 2, 2, 4, 4, 6]},
        "expected_output": [
            [-4, -2, 6],
            [-4, 0, 4],
            [-4, 2, 2],
            [-2, -2, 4],
            [-2, 0, 2],
        ],
        "is_hidden": True,
    },
    {
        "params": {"nums": [1, 2, -2, -1]},
        "expected_output": [],
        "is_hidden": False,
    },
    {
        "params": {"nums": [0] * 50},
        "expected_output": [[0, 0, 0]],
        "is_hidden": True,
    },
    {
        "params": {"nums": list(range(5, 105, 5))},
        "expected_output": [],
        "is_hidden": True,
    },
    {
        "params": {"nums": [-100000, 50000, 50000, 0, 1, -1]},
        "expected_output": [[-100000, 50000, 50000], [-1, 0, 1]],
        "is_hidden": False,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_three_sum_test_cases() -> None:
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
                "3Sum problem not found. Seed the problem first via scripts/seed_problem_three_sum.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in THREE_SUM_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in THREE_SUM_TEST_CASES:
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
    seed_three_sum_test_cases()
