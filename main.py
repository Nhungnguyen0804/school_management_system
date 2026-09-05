from ctypes.wintypes import HPALETTE

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Teacher
from schemas import StudentResponse,StudentCreate, TeacherCreate, TeacherResponse
from fastapi import HTTPException
import uuid

app = FastAPI()


@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get('/teachers', response_model= list[TeacherResponse]) # list vì get ra danh sách teacher
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all() # lấy danh sách hoặc rỗng []
    return teachers


@app.post("/students", response_model=StudentResponse)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(name=student_data.name)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post('/teachers', response_model = TeacherResponse)
def create_teacher(teacher_data : TeacherCreate, db: Session = Depends(get_db)):
    new_teacher = Teacher(name = teacher_data.name)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: uuid.UUID, db: Session = Depends(get_db)):
    # dùng first ==> trả 1 object hoặc None nếu ko có
    # .all() sẽ trả về tất quả hoặc rỗng []
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@app.get('/teachers/{teacher_id}', response_model = TeacherResponse)
def get_teacher(teacher_id: uuid.UUID, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None: raise HTTPException(status_code = 404, detail = 'teacher not found')
    return teacher

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: uuid.UUID, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = student_data.name
    db.commit()
    db.refresh(student)
    return student

@app.put('/teachers/{teacher_id}' , response_model= TeacherResponse)
def update_teacher(teacher_id: uuid.UUID , teacher_data : TeacherCreate , db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None: raise HTTPException(status_code = 404, detail = 'teacher not found')
    # update
    teacher.name = teacher_data.name
    db.commit()
    db.refresh(teacher)
    return teacher

@app.delete("/students/{student_id}")
def delete_student(student_id: uuid.UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@app.delete('/teachers/{teacher_id}')
def delete_teacher(teacher_id : uuid.UUID , db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id ).first()
    if teacher is None: raise HTTPException(status_code  = 404, detail = 'teacher not found ')
    db.delete(teacher)
    db.commit()
    return {'message': 'teacher deleted successfully'}