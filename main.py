from fastapi import FastAPI, Depends ,status
from sqlalchemy.orm import Session ,joinedload
from database import get_db
from models import Student, Teacher, Class ,Enrollment ,Teach , Division
from constants import EnrollmentStatus ,TeachStatus
from schemas import ChangeTeacherRequest, StudentResponse,StudentCreate, TeacherCreate, TeacherResponse, ClassCreate, ClassResponse, EnrollmentResponse , EnrollmentCreate ,TeachCreate ,TeachResponse, DivisionCreate, DivisionResponse
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

@app.get('/divisions' , response_model = list[DivisionResponse])
def get_divisions(db: Session = Depends(get_db)):
    divisions = db.query(Division).all()
    return divisions
# POST ========================================================================================
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

@app.post('/divisions', response_model = DivisionResponse)
def create_division(division_data : DivisionCreate, db: Session = Depends(get_db)):
    new_division = Division(name = division_data.name)
    db.add(new_division)
    db.commit()
    db.refresh(new_division)
    return new_division
# GET id ========================================================================================
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: uuid.UUID, db: Session = Depends(get_db)):
    # dùng first ==> trả 1 object hoặc None nếu ko có
    # .all() sẽ trả về tất quả hoặc rỗng []
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return student

@app.get('/teachers/{teacher_id}', response_model = TeacherResponse)
def get_teacher(teacher_id: uuid.UUID, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'teacher not found')
    return teacher

@app.get('/classes/{class_id}', response_model = ClassResponse)
def get_class(class_id: uuid.UUID, db: Session = Depends(get_db)):
    current_class = db.query(Class).filter(Class.id == class_id).first()
    if current_class is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'class not found')
    return current_class

@app.get('/divisions/{division_id}', response_model = DivisionResponse)
def get_division(division_id: uuid.UUID, db: Session = Depends(get_db)):
    division = db.query(Division).filter(Division.id == division_id).first()
    if division is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'division not found')
    return division

# PUT = update ========================================================================================
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: uuid.UUID, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    student.name = student_data.name
    db.commit()
    db.refresh(student)
    return student

@app.put('/teachers/{teacher_id}' , response_model= TeacherResponse)
def update_teacher(teacher_id: uuid.UUID , teacher_data : TeacherCreate , db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'teacher not found')
    # update
    teacher.name = teacher_data.name
    db.commit()
    db.refresh(teacher)
    return teacher

@app.put('/classes/{class_id}' , response_model= ClassResponse)
def update_class(class_id: uuid.UUID , class_data : TeacherCreate , db: Session = Depends(get_db)):
    current_class = db.query(Class).filter(Class.id == class_id).first()
    if current_class is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'class not found')
    # update
    current_class.name = class_data.name
    db.commit()
    db.refresh(current_class)
    return current_class

@app.put('/divisions/{division_id}' , response_model= DivisionResponse)
def update_division(division_id: uuid.UUID , division_data : DivisionCreate , db: Session = Depends(get_db)):
    division = db.query(Division).filter(Division.id == division_id).first()
    if division is None: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'division not found')
    # update
    division.name = division_data.name
    db.commit()
    db.refresh(division)
    return division

# Delete ========================================================================================
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
    if teacher is None: raise HTTPException(status_code  = status.HTTP_404_NOT_FOUND, detail = 'teacher not found ')
    db.delete(teacher)
    db.commit()
    return {'message': 'teacher deleted successfully'}


@app.delete('/classes/{class_id}')
def delete_class(class_id : uuid.UUID , db: Session = Depends(get_db)):
    current_class = db.query(Class).filter(Class.id == class_id ).first()
    if current_class is None: raise HTTPException(status_code  = status.HTTP_404_NOT_FOUND, detail = 'class not found ')
    db.delete(current_class)
    db.commit()
    return {'message': 'class deleted successfully'}

@app.delete('/divisions/{division_id}')
def delete_division(division_id : uuid.UUID , db: Session = Depends(get_db)):
    division = db.query(Division).filter(Division.id == division_id ).first()
    if division is None: raise HTTPException(status_code  = status.HTTP_404_NOT_FOUND, detail = 'division not found ')
    db.delete(division)
    db.commit()
    return {'message': 'division deleted successfully'}

# business logic phức tạp hơn
# CREATE ENROLLMENT
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

# GET ENROLLMENT
# GET /students/{student_id}/classes
# Lấy tất cả lớp mà Học sinh X đã đăng ký
# hs X đăng ký những lớp nào ? (dựa vào hs X )
@app.get("/students/{student_id}/classes")
def get_classes_by_student(student_id: uuid.UUID, db: Session = Depends(get_db)):
    # 1. Kiểm tra học sinh có tồn tại không
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Query bảng Enrollments và eager load (joinedload) thông tin Class
    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.class_)) # class_ là tôi đặt tên , đại diện Lớp học  (phân biệt với class python nên mới có _ thôi)
        .filter(Enrollment.student_id == student_id ,
                Enrollment.status == EnrollmentStatus.ACTIVE)
        .all()
    )

    # 3. Trả về danh sách các Class
    return [e.class_ for e in enrollments]

# Lấy tất cả học sinh thuộc Lớp Y
# dựa theo lớp nào (là lớp Y)
# GET /classes/{class_id}/students
@app.get("/classes/{class_id}/students")
def get_students_by_class(class_id: uuid.UUID, db: Session = Depends(get_db)):
    # 1. Kiểm tra lớp học có tồn tại không
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")

    # 2. Query bảng Enrollments và eager load (joinedload) thông tin Student
    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.student))
        .filter(Enrollment.class_id == class_id ,
                Enrollment.status == EnrollmentStatus.ACTIVE)
        .all()
    )

    # 3. Trả về danh sách các Student
    return [e.student for e in enrollments]


# Update delete khi học sinh hủy đăng ký môn học
# PATCH /enrollments/cancel
# withdraw ===> là soft delete (thực tế ưu tiên hơn vì fallback được)
@app.patch("/enrollments/cancel", response_model=EnrollmentResponse)
def withdraw_enrollment( # withdraw = rút, rút khỏi, hủy ---> đăng ký môn học
    student_id: uuid.UUID,
    class_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    # 1. Tìm bản ghi đang hoạt động (ACTIVE)
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.class_id == class_id,
        Enrollment.status == EnrollmentStatus.ACTIVE
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active enrollment not found for this student and class"
        )

    # 2. Đổi trạng thái thành CANCELLED
    enrollment.status = EnrollmentStatus.CANCELLED

    db.commit()
    db.refresh(enrollment)
    return enrollment

# TEACH : phân công giảng dạy
@app.post("/teach", response_model=TeachResponse)
def assign_teacher(data: TeachCreate, db: Session = Depends(get_db)):
    # Check 1: teacher có tồn tại không
    teacher = db.query(Teacher).filter(Teacher.id == data.teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    # Check 2: class có tồn tại không
    class_obj = db.query(Class).filter(Class.id == data.class_id).first()
    if class_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    # Check 3: class này đã có teacher chưa (chỉ check class_id, KHÔNG check cặp)
    # KHÔNG check cặp => quy định mqh 1-1 : 1 lớp - 1 giáo viên
    # 1 lớp môn DSA chỉ cần 1 giáo viên phụ trách

    # lớp class_id = A đã có trong bảng Teach chưa ? ( có giáo viên phụ trách chưa ? )

    # ko check cả cặp (teacher id, class id) vì:
    # nếu lớp X có gv A dạy => (lớp X, gv A) tồn tại
    # nhưng lại cho lớp X có thêm gv B dạy => (lớp X , gv B) chưa tồn tại ==> thêm gv B dù đã có gv A rồi => sai
    # 1 lớp có nhiều giáo viên (là ko đúng) ==> quan hệ N-N

    # old
    # existing = db.query(Teach).filter(Teach.class_id == data.class_id).first()
    # if existing is not None:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This class already has a teacher")

    # new
    # Check 3: Lớp này đã có giáo viên ĐANG DẠY (ACTIVE) chưa?
    existing = db.query(Teach).filter(
        Teach.class_id == data.class_id,
        Teach.status == TeachStatus.ACTIVE
    ).first()

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This class already has an active teacher"
        )
    new_teach = Teach(teacher_id=data.teacher_id, class_id=data.class_id)
    db.add(new_teach)
    db.commit()
    db.refresh(new_teach)
    return new_teach

# get /teachers / teacher_id / classes
# 1 giáo viên dạy bao nhiêu lớp ? (quan hệ 1 - n)
@app.get("/teachers/{teacher_id}/classes")
def get_classes_by_teacher(teacher_id: uuid.UUID, db: Session = Depends(get_db)):
    # 1. Kiểm tra teacher có tồn tại không
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teacher not found")

    # 2. Query bảng Teacher và eager load (joinedload) thông tin Class
    all_teach = (
        db.query(Teach)
        .options(joinedload(Teach.class_)) # models Teach có class_ , class_ là tôi đặt tên , đại diện Lớp học  (phân biệt với class python nên mới có _ thôi)
        .filter(Teach.teacher_id == teacher_id ,
                Teach.status == TeachStatus.ACTIVE)
        .all()
    )

    # 3. Trả về danh sách các Class mà teacher id này phụ trách
    return [e.class_ for e in all_teach]

@app.patch("/teach/unassign", response_model=TeachResponse)
def unassign_teacher(class_id: uuid.UUID, db: Session = Depends(get_db)):
    # Tìm phân công đang ACTIVE của lớp này
    teach = db.query(Teach).filter(
        Teach.class_id == class_id,
        Teach.status == TeachStatus.ACTIVE
    ).first()

    if not teach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active teacher found for this class"
        )

    # Chuyển trạng thái sang CANCELLED
    teach.status = TeachStatus.CANCELLED
    db.commit()
    db.refresh(teach)
    return teach


@app.patch("/teach/{class_id}/teacher", response_model=TeachResponse)
def change_teacher(
    class_id: uuid.UUID,
    data: ChangeTeacherRequest,
    db: Session = Depends(get_db)
):
    # 1. Kiểm tra Lớp X có tồn tại không
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    # 2. Kiểm tra Giáo viên B có tồn tại không
    new_teacher = db.query(Teacher).filter(Teacher.id == data.teacher_id).first()
    if not new_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    # 3. Tìm phân công ĐANG ACTIVE của lớp X
    current_teach = db.query(Teach).filter(
        Teach.class_id == class_id,
        Teach.status == TeachStatus.ACTIVE
    ).first()

    if not current_teach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active teacher found for this class"
        )

    if current_teach.teacher_id == data.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This teacher is already assigned to this class"
        )

    # 4. Hủy phân công cũ & Tạo phân công mới trong 1 Transaction
    current_teach.status = TeachStatus.CANCELLED

    new_teach = Teach(
        teacher_id=data.teacher_id,
        class_id=class_id,
        status=TeachStatus.ACTIVE
    )
    db.add(new_teach)

    db.commit()
    db.refresh(new_teach)
    return new_teach


@app.get("/classes/{class_id}/teacher", response_model=TeacherResponse)
def get_teacher_by_class(class_id: uuid.UUID, db: Session = Depends(get_db)):
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    teach = db.query(Teach).options(joinedload(Teach.teacher)).filter(
        Teach.class_id == class_id,
        Teach.status == TeachStatus.ACTIVE
    ).first()

    if not teach:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active teacher assigned to this class")

    return teach.teacher

