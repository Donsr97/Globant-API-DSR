from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.job_model import Job

def InsertJob_to_db(job, db: Session):
    db.add_all(job)
    db.commit()
    return "Data inserted successfully"

def FetchAll_job(db: Session):
    return db.query(Job).all()

def FetchById_job(job_id: str, db: Session):
    return db.query(Job).filter(Job.id == job_id).first()
