from fastapi import FastAPI, Depends, HTTPException, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db  
from models.hired_employee_model import HiredEmployee  
from schemas.hired_employee_schema import HiredEmployeeSchema  
from service.hired_employee_service import insert_csv_to_db, fetch_all_hired_employees, fetch_by_id, get_hired_employees_by_quarter, get_departments_hiring_above_average
from database import SessionLocal, engine  
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/hired-employees")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/fetch-all", response_model=list[HiredEmployeeSchema])
def get_all_hired_employees(db: Session = Depends(get_db)):
    employees = fetch_all_hired_employees(db)
    return employees

@router.get("/fetch-by-id/{employee_id}", response_model=HiredEmployeeSchema)
def get_hired_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    employee = fetch_by_id(employee_id,db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee



@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        csv_file = await file.read()
        message = insert_csv_to_db(csv_file.decode('utf-8'), db)
        return JSONResponse(content={"message": message}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/hired-employees-by-quarter/{year}")
def fetch_hired_employees_by_quarter(year: int, db: Session = Depends(get_db)):
    data = get_hired_employees_by_quarter(year,db)
    return data

@router.get("/hired_employees_per_department/{year}")
def fetch_departments_hiring_above_average(year: int, db: Session = Depends(get_db)):
    data = get_departments_hiring_above_average(year,db)
    return data
