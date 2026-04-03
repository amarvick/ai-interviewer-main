"""
Seed script for test cases for the "Group Anagrams" problem.

Run from backend/:
    source venv/bin/activate
    python scripts/seed_test_cases_group_anagrams.py
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


TARGET_PROBLEM_SLUG = "group-anagrams"
TARGET_PROBLEM_TITLE = "Group Anagrams"

GROUP_ANAGRAMS_TEST_CASES = [
    {
        "params": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]},
        "expected_output": [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]],
        "is_hidden": False,
    },
    {
        "params": {"strs": [""]},
        "expected_output": [[""]],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["a"]},
        "expected_output": [["a"]],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["aa", "bb", "ab", "ba", "b"]},
        "expected_output": [["aa"], ["bb"], ["ab", "ba"], ["b"]],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["abc", "bca", "cab", "zzz", "zz", "z"]},
        "expected_output": [["abc", "bca", "cab"], ["zzz"], ["zz"], ["z"]],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["aaaaaaaaaa", "aaaaaaaaaa", "aaaaaaaaab"]},
        "expected_output": [["aaaaaaaaaa", "aaaaaaaaaa"], ["aaaaaaaaab"]],
        "is_hidden": True,
    },
    {
        "params": {"strs": ["listen", "silent", "enlist", "google", "glegoo"]},
        "expected_output": [["listen", "silent", "enlist"], ["google", "glegoo"]],
        "is_hidden": False,
    },
    {
        "params": {"strs": ["x"] * 50},
        "expected_output": [["x"] * 50],
        "is_hidden": True,
    },
    {
        "params": {"strs": ["abc", "acb", "bac", "bca", "cab", "cba", "def"]},
        "expected_output": [["abc", "acb", "bac", "bca", "cab", "cba"], ["def"]],
        "is_hidden": True,
    },
]


def _params_key(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def seed_group_anagrams_test_cases() -> None:
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
                "Group Anagrams problem not found. Seed the problem first via scripts/seed_problem_group_anagrams.py"
            )

        print(f"Seeding test cases for problem id={problem.id!r}, title={problem.title!r}")

        existing = db.query(TestCase).filter(TestCase.problem_id == problem.id).all()
        existing_by_params = {_params_key(tc.params): tc for tc in existing}
        seed_params_keys = {_params_key(tc["params"]) for tc in GROUP_ANAGRAMS_TEST_CASES}

        inserted = 0
        updated = 0
        skipped = 0
        deleted = 0

        for seed_case in GROUP_ANAGRAMS_TEST_CASES:
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
    seed_group_anagrams_test_cases()
