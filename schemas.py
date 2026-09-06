import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# -------------------------------------------------------------------------------------------
class StudentResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime

    # Cho phép Pydantic đọc trực tiếp từ SQLAlchemy object (không chỉ dict)
    model_config = ConfigDict(from_attributes=True)

class StudentCreate(BaseModel):
    name: str

# -------------------------------------------------------------------------------------------
class TeacherResponse(BaseModel):
    id: uuid.UUID
    name: str
    create_at: datetime
    updated_at: datetime


class TeacherCreate(BaseModel):
    name: str

# -------------------------------------------------------------------------------------------
class ClassResponse(BaseModel):
    id : uuid.UUID
    name: str
    create_at : datetime
    update_at : datetime

class ClassCreate(BaseModel):
    name: str
# -------------------------------------------------------------------------------------------
class DivisionResponse(BaseModel):
    id : uuid.UUID
    name: str
    create_at : datetime
    update_at : datetime

class DivisionCreate(BaseModel):
    name: str

# -------------------------------------------------------------------------------------------
class EnrollmentCreate(BaseModel):
    student_id: uuid.UUID
    class_id: uuid.UUID

class EnrollmentResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    class_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
# -------------------------------------------------------------------------------------------
class TeachCreate(BaseModel):
    teacher_id: uuid.UUID
    class_id: uuid.UUID

class TeachResponse(BaseModel):
    id: uuid.UUID
    teacher_id: uuid.UUID
    class_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChangeTeacherRequest(BaseModel):
    teacher_id: uuid.UUID
    
# -------------------------------------------------------------------------------------------

