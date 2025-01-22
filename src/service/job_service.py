import pandas as pd
from io import StringIO
from fastapi import HTTPException
from models.job_model import Job
from sqlalchemy.orm import Session
from repository.jobs_repository import FetchAll_job, FetchById_job, InsertJob_to_db

def insert_csv_to_db(csv_file, db: Session):
    try:
        csv_data = StringIO(csv_file)
        df = pd.read_csv(csv_data)
        row_count = len(df)
        if row_count < 1 or row_count > 1000:
            raise HTTPException(status_code=400, detail="CSV file must have between 1 and 1000 rows.")

        jobs_to_insert = []
        for _, row in df.iterrows():
            job = row['job']
            jobs_to_insert.append(Job(job=job))

        return InsertJob_to_db(jobs_to_insert, db)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")



def fetch_all_jobs(db: Session):
    try:
        return FetchAll_job(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all jobs: {str(e)}")

def fetch_job_by_id(job_id: str, db: Session):
    try:
        return FetchById_job(job_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching jobs by ID: {str(e)}")

