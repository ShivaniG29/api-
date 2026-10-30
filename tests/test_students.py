def valid_student(**overrides):
    student = {
        "name": "Avery Smith",
        "email": "avery@example.com",
        "age": 20,
        "course": "Computer Science",
    }
    student.update(overrides)
    return student


def test_add_student(client):
    response = client.post("/api/v1/students", json=valid_student())

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Avery Smith",
        "email": "avery@example.com",
        "age": 20,
        "course": "Computer Science",
    }


def test_add_student_rejects_invalid_input(client):
    invalid_student = valid_student(email="not-an-email", age=0)

    response = client.post("/api/v1/students", json=invalid_student)

    assert response.status_code == 422


def test_add_student_rejects_whitespace_name(client):
    response = client.post(
        "/api/v1/students",
        json=valid_student(name="   "),
    )

    assert response.status_code == 422


def test_add_student_rejects_duplicate_email_case_insensitively(client):
    client.post("/api/v1/students", json=valid_student())

    response = client.post(
        "/api/v1/students",
        json=valid_student(email="AVERY@example.com"),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A student with this email address already exists"
    )


def test_view_all_students(client):
    client.post("/api/v1/students", json=valid_student())
    client.post(
        "/api/v1/students",
        json=valid_student(name="Jordan Lee", email="jordan@example.com"),
    )

    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert [student["name"] for student in response.json()] == [
        "Avery Smith",
        "Jordan Lee",
    ]


def test_view_all_students_when_empty(client):
    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert response.json() == []


def test_view_student_by_id(client):
    created = client.post(
        "/api/v1/students",
        json=valid_student(),
    ).json()

    response = client.get(f"/api/v1/students/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_view_student_returns_not_found_for_unknown_id(client):
    response = client.get("/api/v1/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_view_student_rejects_non_positive_id(client):
    response = client.get("/api/v1/students/0")

    assert response.status_code == 422


def test_delete_student(client):
    created = client.post(
        "/api/v1/students",
        json=valid_student(),
    ).json()

    response = client.delete(f"/api/v1/students/{created['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted successfully"}
    assert client.get(f"/api/v1/students/{created['id']}").status_code == 404


def test_delete_student_returns_not_found_for_unknown_id(client):
    response = client.delete("/api/v1/students/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_delete_student_rejects_non_positive_id(client):
    response = client.delete("/api/v1/students/0")

    assert response.status_code == 422
