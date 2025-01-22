from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.department_model import Department
from sqlalchemy.orm import Session
from io import StringIO
import pandas as pd
from repository.department_repository import FetchAll_departments, FetchById_department, InsertDepartments_to_db


def insert_csv_to_db(csv_file, db: Session):
    try:
        csv_data = StringIO(csv_file)
        df = pd.read_csv(csv_data)
        row_count = len(df)
        if row_count < 1 or row_count > 1000:
            raise HTTPException(status_code=400, detail="CSV file must have between 1 and 1000 rows.")

        departments_to_insert = []
        for _, row in df.iterrows():
            department = row['department']
            departments_to_insert.append(Department(department=department))

        return InsertDepartments_to_db(departments_to_insert, db)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")




def fetch_all_departments(db: Session):
    try:
        return FetchAll_departments(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all departments: {str(e)}")

def fetch_by_id_department(department_id: str, db: Session):
    try:
        return FetchById_department(department_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching department by ID: {str(e)}")

