from typing import Annotated
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

student_data = [
    {
        "id": 1,
        "name": "Alice",
        "age": 20,
        "courses": [
            {"id": 101, "name": "Math", "credits": 3},
            {"id": 102, "name": "Physics", "credits": 4},
        ],
    },
    {
        "id": 2,
        "name": "Bob",
        "age": 22,
        "courses": [{"id": 103, "name": "Chemistry", "credits": 3}],
    },
]


class Course(BaseModel):
    id: Annotated[
        int,
        Field(
            ..., description="Course ID to be entered (3 digits)", examples=[123, 104]
        ),
    ]
    name: Annotated[
        str, Field(..., description="Course name", examples=["Math", "Chemistry"])
    ]
    credits: Annotated[
        int,
        Field(
            ...,
            description="Credits the course has to offer (usually single digit)",
            examples=[3, 5],
        ),
    ]


class CourseUpdate(BaseModel):
    id: Annotated[
        int | None,
        Field(description="Course ID to be entered (3 digits)", examples=[123, 104]),
    ] = None
    name: Annotated[
        str | None, Field(description="Course name", examples=["Math", "Chemistry"])
    ] = None
    credits: Annotated[
        int | None,
        Field(
            description="Credits the course has to offer (usually single digit)",
            examples=[3, 5],
        ),
    ] = None


class Student(BaseModel):
    id: Annotated[
        int,
        Field(
            ..., description="Id of student - 2 digits max", lt=100, examples=[1, 20]
        ),
    ]
    name: Annotated[
        str,
        Field(
            ...,
            max_length=40,
            title="Student Name",
            description="Students full name to be stored in db",
            examples=["John Smith", "Joseph Killings"],
        ),
    ]
    age: Annotated[int, Field(..., gt=18)]
    courses: list[Course]

    @computed_field
    @property
    def total_credits(self) -> int:
        return sum(course.credits for course in self.courses)


class StudentUpdate(BaseModel):
    id: Annotated[
        int | None,
        Field(description="Id of student - 2 digits max", lt=100, examples=[1, 23]),
    ] = None
    name: Annotated[
        str | None,
        Field(
            max_length=40,
            title="Student Name",
            description="Students full name to be stored in db",
            examples=["John Smith", "Joseph Killings"],
        ),
    ] = None
    age: Annotated[int | None, Field(gt=18)] = None
    courses: list[Course] | None = None


app = FastAPI(title="Student Courses API")


@app.get("/")
def rootDir():
    return JSONResponse(
        status_code=200, content={"success": "server is working and is loaded"}
    )


@app.get("/students")
def list_students():
    return student_data


@app.get("/students/{student_id}")
def get_student(
    student_id: int = Path(
        ...,
        description="The id of the student you want to retieve",
        ge=1,
        example=21,
    ),
):
    for student in student_data:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
