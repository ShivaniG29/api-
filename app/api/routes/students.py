from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import MessageResponse, StudentCreate, StudentRead
from app.services.student_service import (
    DuplicateStudentError,
    create_student,
    delete_student,
    get_student,
    list_students,
)

router = APIRouter(prefix="/api/v1/students", tags=["students"])


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a student",
)
def add_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
) -> StudentRead:
    """Create a student record."""
    try:
        return create_student(db, student_data)
    except DuplicateStudentError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[StudentRead],
    summary="View all students",
)
def read_students(db: Session = Depends(get_db)) -> list[StudentRead]:
    """Return all students in ID order."""
    return list_students(db)


@router.get(
    "/{student_id}",
    response_model=StudentRead,
    summary="View a student by ID",
)
def read_student(
    student_id: int = Path(gt=0),
    db: Session = Depends(get_db),
) -> StudentRead:
    """Return one student or a 404 response when the ID does not exist."""
    student = get_student(db, student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


@router.delete(
    "/{student_id}",
    response_model=MessageResponse,
    summary="Delete a student",
)
def remove_student(
    student_id: int = Path(gt=0),
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Delete one student or return 404 when the ID does not exist."""
    if not delete_student(db, student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return MessageResponse(message="Student deleted successfully")
