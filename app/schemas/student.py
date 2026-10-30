from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentCreate(BaseModel):
    """Validated request body for creating a student."""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(gt=0, le=120)
    course: str = Field(min_length=1, max_length=100)

    @field_validator("name", "course")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        """Trim surrounding whitespace and reject empty text."""
        value = value.strip()
        if not value:
            raise ValueError("Field must not be empty or whitespace")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        """Store email addresses in a consistent case."""
        return str(value).lower()


class StudentRead(BaseModel):
    """Student representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    course: str


class MessageResponse(BaseModel):
    """Simple message response for successful delete operations."""

    message: str
