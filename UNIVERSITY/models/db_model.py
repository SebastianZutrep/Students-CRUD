from sqlalchemy import Column, Integer, String, Float
from database import Base

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(String, nullable=False)
    grade = Column(Float, nullable=False)