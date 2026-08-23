import uuid
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Teacher(Base):
    __tablename__ = "teachers" # tên table thật sự trong Postgres

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) #Python tự sinh UUID khi tạo object, trước khi insert.
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) #Postgres tự set giá trị
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now()) # on update: mỗi lần row được UPDATE, Postgres tự cập nhật lại updated_at

class Students(Base):
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())