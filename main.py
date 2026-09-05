from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import StudentOut

app = FastAPI()


@app.get("/students", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students