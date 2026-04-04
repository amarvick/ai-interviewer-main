"""
Seed script for test cases for the "Valid Parentheses" problem.

Run:
    python backend/scripts/seed_test_cases_valid_parentheses.py
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


TARGET_PROBLEM_SLUG = "valid-parentheses"
TARGET_PROBLEM_TITLE = "Valid Parentheses"

VALID_PARENTHESES_TEST_CASES = [
    {"params": {"s": "()"}, "expected_output": True, "is_hidden": False},
    {"params": {"s": "()[]{}"}, "expected_output": True, "is_hidden": False},
    {"params": {"s": "(]"}, "expected_output": False, "is_hidden": False},
    {"params": {"s": "([])"}, "expected_output": True, "is_hidden": False},
    {"params": {"s": "([)]"}, "expected_output": False, "is_hidden": False},
    {"params": {"s": "{" * 5000 + "}" * 5000}, "expected_output": True, "is_hidden": True},
    {"params": {"s": "(" * 5000 + ")" * 4999}, "expected_output": False, "is_hidden": True},
    {"params": {"s": ""}, "expected_output": True, "is_hidden": False},
    {"params": {"s": "]"}, "expected_output": False, "is_hidden": False},
    {"params": {"s": "((({{{[[[]]]}}})))"}, "expected_output": True, "is_hidden": False},
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_valid_parentheses_test_cases() -> None:
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
                "Valid Parentheses problem not found. Seed the problem first via scripts/seed_problem_valid_parentheses.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in VALID_PARENTHESES_TEST_CASES}

        inserted = updated = skipped = deleted = 0

        for seed_case in VALID_PARENTHESES_TEST_CASES:
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
    seed_valid_parentheses_test_cases()
