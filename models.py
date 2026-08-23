import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Teacher(Base):
    __tablename__ = "teachers" # tên table thật sự trong Postgres

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) #Python tự sinh UUID khi tạo object, trước khi insert.
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) #Postgres tự set giá trị
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now()) # on update: mỗi lần row được UPDATE, Postgres tự cập nhật lại updated_at

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")

class Student(Base): #đại diện cho MỘT student
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    teach: Mapped["Teach"] = relationship(back_populates="teacher")
    
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

    # relationship() cho phép: enrollment.student -> object Student thật
    student: Mapped["Student"] = relationship(back_populates="enrollments")
    class_: Mapped["Class"] = relationship(back_populates="enrollments")


class Teach(Base):
    __tablename__ = "teach"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    teacher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    # unique=True vì rule: 1 class chỉ có 1 teacher -> mỗi class_id chỉ xuất hiện 1 lần trong bảng này
    class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classes.id"), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    teacher: Mapped["Teacher"] = relationship(back_populates="teach")
    class_: Mapped["Class"] = relationship(back_populates="teach")
