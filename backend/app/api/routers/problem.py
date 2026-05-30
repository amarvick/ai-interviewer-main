import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.problem import (
    ProblemListProblemsResponse,
    ProblemListResponse,
    ProblemResponse,
    ProblemSearchPageResponse,
)
from app.crud.problem import (
    get_problem_lists as get_problem_list_records,
    get_problems_from_problem_list as get_problems_from_problem_list_record,
    get_passed_problem_ids_for_user,
    get_problem_list_name_by_id,
    get_problem_by_id as get_problem_by_id_record,
    search_problems_from_problem_list,
)
from app.crud.testcase import get_public_testcases_by_problem_id
from app.core.auth import get_current_user_optional
from app.db.models.user import User

router = APIRouter()

@router.get("/problem-lists", response_model=list[ProblemListResponse])
def get_problem_lists(db: Session = Depends(get_db)):
    return get_problem_list_records(db)

@router.get("/problems/{problem_list_id}", response_model=ProblemListProblemsResponse)
def get_problems_from_problem_list(
    problem_list_id: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    list_name = get_problem_list_name_by_id(db, problem_list_id)
    if list_name is None:
        raise HTTPException(status_code=404, detail="Problem list not found")

    problems = get_problems_from_problem_list_record(db, problem_list_id)
    passed_problem_ids: set[str] = set()
    if current_user is not None:
        passed_problem_ids = get_passed_problem_ids_for_user(
            db=db,
            user_id=current_user.id,
            problem_ids=[problem.id for problem in problems],
        )
    for problem in problems:
        problem.is_passed = problem.id in passed_problem_ids
    return {"name": list_name, "problems": problems}

@router.get(
    "/problems/{problem_list_id}/search",
    response_model=ProblemSearchPageResponse,
)
def search_problem_list_page(
    problem_list_id: str,
    search: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    """Template endpoint for backend-refreshed search results.

    Fill in the CRUD function first, then this endpoint will be ready for the
    frontend query hook. This endpoint intentionally lives next to the existing
    list endpoint so you can compare the old full-list flow to the paged flow.
    """
    list_name = get_problem_list_name_by_id(db, problem_list_id)
    if list_name is None:
        raise HTTPException(status_code=404, detail="Problem list not found")

    try:
        problems, total = search_problems_from_problem_list(
            db,
            problem_list_id,
            search=search,
            page=page,
            page_size=page_size,
        )
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

    passed_problem_ids: set[str] = set()
    if current_user is not None:
        passed_problem_ids = get_passed_problem_ids_for_user(
            db=db,
            user_id=current_user.id,
            problem_ids=[problem.id for problem in problems],
        )
    for problem in problems:
        problem.is_passed = problem.id in passed_problem_ids

    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return {
        "name": list_name,
        "problems": problems,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next_page": page < total_pages,
        "has_previous_page": page > 1,
    }

@router.get("/problem/{problem_identifier}", response_model=ProblemResponse)
def get_problem_by_id(problem_identifier: str, db: Session = Depends(get_db)):
    problem = get_problem_by_id_record(db, problem_identifier)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    test_cases = get_public_testcases_by_problem_id(db, problem.id)
    problem.test_cases = test_cases
    return problem
