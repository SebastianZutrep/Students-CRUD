from fastapi import HTTPException
from models.student_model import Student
from sqlalchemy.orm import Session
from models.db_model import Students as StudentDB
from typing import List

class StudentController:
    @staticmethod
    def get_all(db: Session) -> List[dict]:
        return db.query(StudentDB).all()

    @staticmethod
    def get_by_id(student_id: int, db: Session) -> dict:
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()

        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return student

    @staticmethod
    def create(student: Student, db: Session) -> dict:
        try:
            print(f"Datos recibidos: {student}")
            new_student = StudentDB(**student.model_dump())
            db.add(new_student)
            db.commit()
            db.refresh(new_student)
            print(f"Estudiante creado: {new_student}")
            return new_student
        except Exception as e:
            print(f"Error al crear estudiante: {e}")
            raise HTTPException(status_code=500, detail="Error al guardar el estudiante")

    @staticmethod
    def update(student_id: int, student: Student, db: Session) -> dict:
        try:
            db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
            if not db_student:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            for key, value in student.model_dump().items():
                setattr(db_student, key, value)
            db.commit()
            db.refresh(db_student)
            return db_student
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
            raise HTTPException(status_code=500, detail="Error al actualizar el estudiante")

    @staticmethod
    def delete(student_id: int, db: Session) -> dict:
        try:
            db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
            if not db_student:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            db.delete(db_student)
            db.commit()
            return {"message": "Estudiante eliminado correctamente"}
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            raise HTTPException(status_code=500, detail="Error al eliminar el estudiante")