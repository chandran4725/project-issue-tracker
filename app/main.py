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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods="[*]",
    allow_headers="[*]"
)

app.include_router(employee.router)
app.include_router(project.router)
app.include_router(role.router)
app.include_router(emp_pro_rel.router)
app.include_router(issue.router)