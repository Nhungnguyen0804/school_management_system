from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import StudentResponse
from schemas import StudentCreate

app = FastAPI()


@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.post("/students", response_model=StudentResponse)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(name=student_data.name)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student