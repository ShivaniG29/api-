# Student Management System API

A beginner-friendly, backend-only student management system built with FastAPI.
It provides endpoints to create, list, retrieve, and delete student records.
Student data is stored in a local SQLite database.

## Technologies

- Python 3.10 or later
- FastAPI and Pydantic
- SQLAlchemy 2
- SQLite
- Pytest and FastAPI TestClient

## Project structure

```text
.
├── app/
│   ├── api/routes/       # HTTP endpoints and request handling
│   ├── db/               # SQLAlchemy base class and database session
│   ├── models/           # Database table definitions
│   ├── schemas/          # Pydantic request and response models
│   ├── services/         # Student data operations and business rules
│   └── main.py           # FastAPI application and startup lifecycle
├── tests/
│   ├── conftest.py       # Isolated test database and TestClient fixtures
│   └── test_students.py  # API success and validation/error tests
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

### Important files

- `app/main.py` creates the FastAPI application, initializes database tables at
  startup, and registers the student routes.
- `app/api/routes/students.py` defines the HTTP methods, paths, status codes,
  and error responses.
- `app/schemas/student.py` validates input and shapes API responses.
- `app/models/student.py` defines the SQLite `students` table.
- `app/services/student_service.py` contains the database operations and
  duplicate-email handling.
- `app/db/session.py` configures the database connection. By default, the
  SQLite file is `students.db` in the project directory.
- `tests/test_students.py` tests the API through FastAPI's `TestClient`.

## Prerequisites

Install Python 3.10 or later and ensure `python` and `pip` are available in
your terminal.

## Installation

From the project directory, create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, you can invoke the environment's Python
directly as `.\.venv\Scripts\python.exe`.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the application and test dependencies:

```text
python -m pip install -r requirements.txt
```

## Run the application

Start the development server from the project directory:

```text
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. The SQLite database and
`students` table are created automatically when the application starts.

To use a different SQLite file, set `DATABASE_URL` before starting the server.
For example, in PowerShell:

```powershell
$env:DATABASE_URL = "sqlite:///./my_students.db"
uvicorn app.main:app --reload
```

## API endpoints

All student endpoints use the `/api/v1/students` base path.

| Method | Path | Purpose | Success |
|---|---|---|---|
| `POST` | `/api/v1/students` | Add a student | `201 Created` |
| `GET` | `/api/v1/students` | View all students | `200 OK` |
| `GET` | `/api/v1/students/{student_id}` | View one student | `200 OK` |
| `DELETE` | `/api/v1/students/{student_id}` | Delete one student | `200 OK` |

Student fields:

| Field | Type | Rules |
|---|---|---|
| `name` | string | Required, 1–100 characters after trimming whitespace |
| `email` | string | Required, valid email address, unique (case-insensitive) |
| `age` | integer | Required, between 1 and 120 |
| `course` | string | Required, 1–100 characters after trimming whitespace |

### Add a student

`POST /api/v1/students`

Request:

```json
{
  "name": "Avery Smith",
  "email": "avery@example.com",
  "age": 20,
  "course": "Computer Science"
}
```

Response (`201 Created`):

```json
{
  "id": 1,
  "name": "Avery Smith",
  "email": "avery@example.com",
  "age": 20,
  "course": "Computer Science"
}
```

### View all students

`GET /api/v1/students`

Response (`200 OK`):

```json
[
  {
    "id": 1,
    "name": "Avery Smith",
    "email": "avery@example.com",
    "age": 20,
    "course": "Computer Science"
  }
]
```

An empty collection is returned as `[]`.

### View a student by ID

`GET /api/v1/students/1`

Response (`200 OK`):

```json
{
  "id": 1,
  "name": "Avery Smith",
  "email": "avery@example.com",
  "age": 20,
  "course": "Computer Science"
}
```

An unknown student ID returns `404 Not Found`. An ID that is not a positive
integer returns `422 Unprocessable Entity`.

### Delete a student

`DELETE /api/v1/students/1`

Response (`200 OK`):

```json
{
  "message": "Student deleted successfully"
}
```

An unknown student ID returns `404 Not Found`.

### Error responses

- Invalid or missing request fields and non-positive IDs return `422` with
  FastAPI's validation details.
- An email address that is already registered returns `409 Conflict`:

```json
{
  "detail": "A student with this email address already exists"
}
```

- A student ID that does not exist returns `404 Not Found`:

```json
{
  "detail": "Student not found"
}
```

## API documentation

FastAPI generates interactive documentation automatically while the server is
running:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Test with Postman

1. Start the server with `uvicorn app.main:app --reload`.
2. In Postman, use `http://127.0.0.1:8000/api/v1/students` as the base URL.
3. To add a student, choose `POST`, set **Body → raw → JSON**, enter the sample
   request above, and send it.
4. Choose `GET` and send the base URL to list students, or append a student ID
   (for example, `/1`) to retrieve one.
5. Choose `DELETE` and send the URL with a student ID to delete that record.
6. To check validation and duplicate handling, submit invalid data or repeat an
   email address and inspect the response status and JSON details.

## Test in a web browser

With the server running, open
<http://127.0.0.1:8000/api/v1/students> to list students or
<http://127.0.0.1:8000/api/v1/students/1> to retrieve student 1. Browsers can
make these GET requests directly. Use Swagger UI or Postman for POST and DELETE
requests.

## Run the tests

Activate the virtual environment, then run:

```text
python -m pytest
```

The tests use an in-memory SQLite database and cover creation, listing,
retrieval, deletion, invalid input and IDs, missing students, and duplicate
email addresses. They do not modify the application's `students.db` file.
