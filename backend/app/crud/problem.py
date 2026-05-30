from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.db.models.problem import Problem
from app.db.models.problem_list import ProblemList
from app.db.models.problem_list_problem import ProblemListProblem
from app.db.models.user_problem import UserProblem

# For problem page
def get_problem_by_id(db, problem_id: str):
    return (
        db.query(Problem)
        .filter(or_(Problem.id == problem_id, Problem.slug == problem_id))
        .first()
    )

# For home page
def get_problem_lists(db: Session):
    return db.query(ProblemList).all()

# For problem list page
def get_problem_list_name_by_id(db: Session, problem_list_id: str):
    problem_list = db.query(ProblemList).filter(ProblemList.id == problem_list_id).first()
    return problem_list.name if problem_list else None

def get_problems_from_problem_list(db: Session, problem_list_id: str):
    return (
        db.query(Problem)
        .join(ProblemListProblem, ProblemListProblem.problem_id == Problem.id)
        .filter(ProblemListProblem.problem_list_id == problem_list_id)
        .all()
    )


def search_problems_from_problem_list(
    db: Session,
    problem_list_id: str,
    *,
    search: str = "",
    page: int = 1,
    page_size: int = 10,
):
    query = (
        db.query(Problem)
        .join(ProblemListProblem, ProblemListProblem.problem_id == Problem.id)
        .filter(ProblemListProblem.problem_list_id == problem_list_id)
    )

    normalized_search = search.strip()
    if normalized_search:
        pattern = f"%{normalized_search}%"
        query = query.filter(
            or_(
                Problem.title.ilike(pattern),
                Problem.category.ilike(pattern),
                Problem.difficulty.ilike(pattern)
            )
        )
    
    total = query.count()
    offset = (page - 1) * page_size

    problems = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )
    return problems, total

def get_passed_problem_ids_for_user(
    db: Session,
    user_id: str,
    problem_ids: list[str],
) -> set[str]:
    if not problem_ids:
        return set()
    rows = (
        db.query(UserProblem.problem_id)
        .filter(
            UserProblem.user_id == user_id,
            UserProblem.problem_id.in_(problem_ids),
            UserProblem.is_passed.is_(True),
        )
        .all()
    )
    return {row[0] for row in rows}
