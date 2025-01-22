import pandas as pd
from io import StringIO
from fastapi import HTTPException
from models.hired_employee_model import HiredEmployee
from models.department_model import Department
from models.job_model import Job
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from repository.hired_employee_repository import FetchAll_employees, FetchById_employee, InsertEmployee_to_db, FetchHired_employees_per_department, FetchHired_employee_counts

def insert_csv_to_db(csv_file, db: Session):
    try:
        csv_data = StringIO(csv_file)
        df = pd.read_csv(csv_data)
        row_count = len(df)
        if row_count < 1 or row_count > 1000:
            raise HTTPException(status_code=400, detail="CSV file must have between 1 and 1000 rows.")

        hired_employees_to_insert = []
        for _, row in df.iterrows():
            new_employee = HiredEmployee(
                name=row['name'],
                datetime=row['datetime'],
                department_id=row['department_id'],
                job_id=row['job_id']
            )
            hired_employees_to_insert.append(new_employee)

        return InsertEmployee_to_db(hired_employees_to_insert, db)

    except Exception as e:
        error_message = f"Error during the process: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)


def fetch_all_hired_employees(db: Session):
    try:
        return FetchAll_employees(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all emplyees: {str(e)}")

def fetch_by_id(employee_id: str, db: Session):
    try:
        return FetchById_employee(employee_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employees by ID: {str(e)}")



#######################################################################################
###### 
###### Ex1. Number of employees hired for each job and department in 2021 divided by quarter. 
######      The table must be ordered alphabetically by department and job.




def initialize_hired_counts() -> dict:
    return {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}

def update_hired_counts(result, department, job) -> dict:
    hired_counts = initialize_hired_counts()
    for row in result:
        if row.department == department and row.job == job:
            hired_counts[f"Q{int(row.quarter)}"] = row.hired
    return hired_counts

def format_hired_employee_data(result) -> list:
    final_data = []
    for department, job in set((row.department, row.job) for row in result):
        hired_counts = update_hired_counts(result, department, job)
        final_data.append({
            "department": department,
            "job": job,
            **hired_counts
        })
    return final_data

def get_hired_employees_by_quarter(year: int, db: Session):
    result = FetchHired_employee_counts(year, db)
    final_data = format_hired_employee_data(result)
    return final_data

#######################################################################################
###### 
###### Ex2. List of ids, name and number of employees hired of each department that hired more
######      employees than the mean of employees hired in 2021 for all the departments, ordered
######      by the number of employees hired (descending).




def calculate_mean_hired_employees(hired_employees_data: list) -> float:
    if not hired_employees_data:
        return 0
    total_hired = sum(item.hired for item in hired_employees_data)
    return total_hired / len(hired_employees_data)

def get_departments_hiring_above_average(year: int, db: Session):
    hired_employees_data = FetchHired_employees_per_department(year, db)

    if not hired_employees_data:
        return []

    mean_hired = calculate_mean_hired_employees(hired_employees_data)

    departments_above_average = [
        {
            "id": item.department_id,
            "department": item.department,
            "hired": item.hired
        }
        for item in hired_employees_data
        if item.hired > mean_hired
    ]

    departments_above_average.sort(key=lambda x: x["hired"], reverse=True)

    return departments_above_average
