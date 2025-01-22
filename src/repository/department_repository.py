from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.department_model import Department

def InsertDepartments_to_db(departments, db: Session):
    db.add_all(departments)
    db.commit()
    return "Data inserted successfully"

def FetchAll_departments(db: Session):
    return db.query(Department).all()

def FetchById_department(department_id: str, db: Session):
    return db.query(Department).filter(Department.id == department_id).first()
