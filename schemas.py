import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StudentResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime

    # Cho phép Pydantic đọc trực tiếp từ SQLAlchemy object (không chỉ dict)
    model_config = ConfigDict(from_attributes=True)

class StudentCreate(BaseModel):
    name: str

