from pydantic import BaseModel, Field



# validaciones de los datos


# informacion de los estudiantes
# ... significa que es requerido
class Student (BaseModel):
    name: str = Field(...,min_length=2)
    age: int = Field (...,gt=0)
    grade: float = Field (..., ge=0,le=5)



# cuadno vas a responder(ya tiene id creado)
class StudentResponse(Student):
    id: int 

