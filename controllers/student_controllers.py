from fastapi import HTTPException, Depends
from models.student_model import Student
from sqlalchemy.orm import Session
from models.db_model import Students as StudentDB
from database import get_db

class StudentController:
    @staticmethod
    def get_all(db: Session = Depends(get_db)) -> list[StudentDB]:
        return db.query(StudentDB).all()
    
    @staticmethod
    def get_by_id(db: Session = Depends(get_db), student_id: int = None) -> StudentDB:
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return student
        
    # nombre de la varible: tipo de variable
    @staticmethod
    def create(student: Student, db: Session = Depends(get_db)) -> StudentDB:
        new_student = StudentDB(**student.model_dump())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student