from fastapi import FastAPI, Depends, HTTPException, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db  
from models.job_model import Job  
from schemas.job_schema import JobSchema  
from service.job_service import insert_csv_to_db, fetch_all_jobs, fetch_job_by_id
from fastapi.responses import JSONResponse
from database import SessionLocal

router = APIRouter(prefix="/job")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/fetch-all", response_model=list[JobSchema])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = fetch_all_jobs(db)
    return jobs

@router.get("/fetch-by-id/{job_id}", response_model=JobSchema)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = fetch_job_by_id(job_id, db)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        csv_file = await file.read()
        message = insert_csv_to_db(csv_file.decode('utf-8'), db)
        return JSONResponse(content={"message": message}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
