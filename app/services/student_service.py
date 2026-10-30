from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


class DuplicateStudentError(Exception):
    """Raised when a student email address is already registered."""


def create_student(db: Session, student_data: StudentCreate) -> Student:
    """Persist a student, rejecting duplicate email addresses."""
    student = Student(**student_data.model_dump())
    db.add(student)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateStudentError(
            "A student with this email address already exists"
        ) from exc
    db.refresh(student)
    return student


def list_students(db: Session) -> list[Student]:
    """Return every student ordered by ID."""
    return list(db.query(Student).order_by(Student.id).all())


def get_student(db: Session, student_id: int) -> Student | None:
    """Return a student by ID, or None if it does not exist."""
    return db.get(Student, student_id)


def delete_student(db: Session, student_id: int) -> bool:
    """Delete a student by ID and report whether a record was removed."""
    student = db.get(Student, student_id)
    if student is None:
        return False
    db.delete(student)
    db.commit()
    return True
