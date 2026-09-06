from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Teacher, Class ,Enrollment
from schemas import StudentResponse,StudentCreate, TeacherCreate, TeacherResponse, ClassCreate, ClassResponse, EnrollmentResponse , EnrollmentCreate
from fastapi import HTTPException
import uuid

app = FastAPI()
# route

@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get('/teachers', response_model= list[TeacherResponse]) # list vì get ra danh sách teacher
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all() # lấy danh sách hoặc rỗng []
    return teachers

@app.get('/classes' , response_model = list[ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    return classes

# POST ======================================================================
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

@app.post('/classes', response_model = ClassResponse)
def create_class(class_data : ClassCreate, db: Session = Depends(get_db)):
    new_class = Class(name = class_data.name)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


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

@app.get('/classes/{class_id}', response_model = ClassResponse)
def get_class(class_id: uuid.UUID, db: Session = Depends(get_db)):
    current_class = db.query(Class).filter(Class.id == class_id).first()
    if current_class is None: raise HTTPException(status_code = 404, detail = 'class not found')
    return current_class

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

@app.put('/classes/{class_id}' , response_model= ClassResponse)
def update_class(class_id: uuid.UUID , class_data : TeacherCreate , db: Session = Depends(get_db)):
    current_class = db.query(Class).filter(Class.id == class_id).first()
    if current_class is None: raise HTTPException(status_code = 404, detail = 'class not found')
    # update
    current_class.name = class_data.name
    db.commit()
    db.refresh(current_class)
    return current_class

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


@app.delete('/classes/{class_id}')
def delete_class(class_id : uuid.UUID , db: Session = Depends(get_db)):
    current_class = db.query(Class).filter(Class.id == class_id ).first()
    if current_class is None: raise HTTPException(status_code  = 404, detail = 'class not found ')
    db.delete(current_class)
    db.commit()
    return {'message': 'class deleted successfully'}


@app.post("/enrollments", response_model= EnrollmentResponse)
def create_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db)):
    # Check 1: student có tồn tại không
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check 2: class có tồn tại không
    class_obj = db.query(Class).filter(Class.id == data.class_id).first()
    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")

    # Check 3: đã đăng ký chưa
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.class_id == data.class_id
    ).first()
    if existing is not None: # student này đã đăng ký rồi
        raise HTTPException(status_code=409, detail="Student already enrolled in this class")

    # Qua hết 3 check mới thực sự tạo
    # tham gia (đăng ký học) <--- student nào + lớp nào
    new_enrollment = Enrollment(student_id=data.student_id, class_id=data.class_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment