import uuid
from datetime import datetime
from sqlalchemy import Index, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import Enum as SQLEnum
from constants import EnrollmentStatus ,TeachStatus
class Teacher(Base):
    __tablename__ = "teachers" # tên table thật sự trong Postgres , dùng để back_populates

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) #Python tự sinh UUID khi tạo object, trước khi insert.
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) #Postgres tự set giá trị
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now()) # on update: mỗi lần row được UPDATE, Postgres tự cập nhật lại updated_at


    # foreign key trỏ đến bảng division. cột id
    division_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("divisions.id"), nullable=True)

    #teacher --> division / khoa
    division: Mapped["Division"] = relationship(back_populates="division") # mqh 2 chieu

class Student(Base): #đại diện cho MỘT student
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # student --> teach
    teacher: Mapped["Teach"] = relationship(back_populates="teacher")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")

class Class(Base):
    __tablename__ = "classes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # relationship() KHÔNG tạo cột nào trong DB.
    # Nó chỉ giúp Python: class_obj.enrollments -> trả về list các Enrollment liên quan
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="class_")
    teach: Mapped["Teach"] = relationship(back_populates="class_")




class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Đây mới là Foreign Key THẬT - cột này lưu UUID của 1 row bên table students
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("students.id"), nullable=False)
    # Foreign Key trỏ sang table classes
    class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classes.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # Thêm cột trạng thái (mặc định là ACTIVE khi mới đăng ký)
    status: Mapped[EnrollmentStatus] = mapped_column(
        SQLEnum(EnrollmentStatus ,native_enum=False), # native_enum=False: Lưu dạng VARCHAR thay vì Postgres ENUM type ( vì Postgres ENUM type muốn update thì làm phức tạp hơn, Alembic thường gặp lỗi hoặc nhận diện sai sự thay đổi của Postgres ENUM , khó tương thích nếu muốn chuyển db)
        default=EnrollmentStatus.ACTIVE,
        nullable=False
    )
    # relationship() cho phép: enrollment.student -> object Student thật
    # Enrollment --> Student
    student: Mapped["Student"] = relationship(back_populates="enrollments")
    class_: Mapped["Class"] = relationship(back_populates="enrollments")


class Teach(Base):
    __tablename__ = "teach"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    teacher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    # unique=True vì rule: 1 class chỉ có 1 teacher -> mỗi class_id chỉ xuất hiện 1 lần trong bảng này
    # 1. BỎ unique=True Ở ĐÂY
    class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classes.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    status: Mapped[TeachStatus] = mapped_column(
            SQLEnum(TeachStatus ,native_enum=False),
            default=TeachStatus.ACTIVE,
            nullable=False
        )
    teacher: Mapped["Teacher"] = relationship(back_populates="teach")
    class_: Mapped["Class"] = relationship(back_populates="teach")

    # 2. THÊM RULE NÀY: Chỉ cấm trùng class_id đối với những dòng có status == ACTIVE
    __table_args__ = (
        Index(
            "uq_teach_active_class",
            "class_id",
            unique=True,
            postgresql_where=(status == TeachStatus.ACTIVE)
        ),
    )

class Division(Base):
    __tablename__ = "divisions" # khoa/ bộ môn

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # thuoc tính này chứa teacher, ko phải division chính nó
    # 1 division - n teacher ==> list[teacher] , ko phải 1 obj đơn
    teacher: Mapped[list["Teacher"]] = relationship(back_populates="teachers")





'''
Mỗi cặp relationship() phải khớp như "2 đầu dây":
A.field_x  = relationship(back_populates="field_y")
B.field_y  = relationship(back_populates="field_x")

'''