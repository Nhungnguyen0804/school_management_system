from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import StudentResponse
from schemas import StudentCreate
from fastapi import HTTPException
import uuid

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

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: uuid.UUID, db: Session = Depends(get_db)):
    # dùng first ==> trả 1 object hoặc None nếu ko có
    # .all() sẽ trả về tất quả hoặc rỗng []
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: uuid.UUID, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = student_data.name
    db.commit()
    db.refresh(student)
    return student