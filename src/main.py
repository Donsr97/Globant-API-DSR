import uvicorn
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine  
from models.job_model import Job  
from models.department_model import Department  


import pandas as pd
from io import StringIO
from fastapi.responses import JSONResponse
from router import hired_employee_router, job_router, department_router
app = FastAPI(
    title="Employee Management API",
    description="API to manage employees, jobs, and departments.",
    version="1.0",
    docs_url="/documentation"
)


app.include_router(router=hired_employee_router.router, tags=["Hired Employees"])
app.include_router(router=job_router.router, tags=["Jobs"])
app.include_router(router=department_router.router, tags=["Departments"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
