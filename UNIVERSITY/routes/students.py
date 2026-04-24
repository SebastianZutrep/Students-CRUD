from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.student_model import Student, StudentResponse
from controllers.student_controllers import StudentController

router = APIRouter(prefix="/students")

# se esta creando un endpoint

# traer todos los estudantes registrados
@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return StudentController.get_all(db)

# recibe una variable y ese valor entra a la funcion y luego procesar lo que s ehara
@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.get_by_id(db, student_id)

@router.post("/")
def create_students(student: Student, db: Session = Depends(get_db)):
    return StudentController.create(student, db)

@router.put("/{student_id}")
def update_student(student_id: int, update_data: Student, db: Session = Depends(get_db)):
    return StudentController.update(db, student_id, update_data)

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return StudentController.delete(db, student_id)



