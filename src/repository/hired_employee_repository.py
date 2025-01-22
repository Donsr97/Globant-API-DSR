from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.hired_employee_model import HiredEmployee
from models.department_model import Department
from models.job_model import Job
from sqlalchemy import func, extract

def InsertEmployee_to_db(hired_employee, db: Session):
    db.add_all(hired_employee)
    db.commit()
    return "Data inserted successfully"

def FetchAll_employees(db: Session):
    return db.query(HiredEmployee).all()

def FetchById_employee(employee_id: str, db: Session):
    return db.query(HiredEmployee).filter(HiredEmployee.id == employee_id).first()


def FetchHired_employees_per_department(year: int, db: Session):
    return (
        db.query(
            Department.id.label("department_id"),
            Department.department.label("department"),
            func.count(HiredEmployee.id).label("hired")
        )
        .join(Department, Department.id == HiredEmployee.department_id)
        .filter(func.extract("year", HiredEmployee.datetime) == year)
        .group_by(Department.id, Department.department)
        .all()
    )

def FetchHired_employee_counts(year: int, db: Session):
    return (
        db.query(
            Department.department.label("department"),
            Job.job.label("job"),
            func.extract("quarter", HiredEmployee.datetime).label("quarter"),
            func.count(HiredEmployee.id).label("hired"),
        )
        .join(Department, Department.id == HiredEmployee.department_id)
        .join(Job, Job.id == HiredEmployee.job_id)
        .filter(func.extract("year", HiredEmployee.datetime) == year)
        .group_by(Department.department, Job.job, func.extract("quarter", HiredEmployee.datetime))
        .order_by(Department.department, Job.job)
        .all()
    )
