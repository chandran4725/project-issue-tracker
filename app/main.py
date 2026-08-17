from fastapi import FastAPI

from app.util.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.util.config import settings

from app.routes import (
    employee,
    project,
    role,
    emp_pro_rel,
    issue
)


Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(employee.router)
app.include_router(project.router)
app.include_router(role.router)
app.include_router(emp_pro_rel.router)
app.include_router(issue.router)