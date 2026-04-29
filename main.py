from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import students
from database import engine, Base
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de API
app.include_router(students.router)

# Servir archivos estáticos (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")