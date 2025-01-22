from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models.department_model import Department
from service.department_service import insert_csv_to_db, fetch_all_departments, fetch_by_id_department
from database import get_db
from schemas.department_schema import DepartmentSchemas

router = APIRouter(prefix="/department")

@router.get("/fetch-all", response_model=list[DepartmentSchemas])
def get_all_departments(db: Session = Depends(get_db)):
    departments = fetch_all_departments(db)
    return departments

@router.get("/fetch-by-id/{department_id}", response_model=DepartmentSchemas)
def get_department_by_id(department_id: int, db: Session = Depends(get_db)):
    department = fetch_by_id_department(department_id, db)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        csv_file = await file.read()
        message = insert_csv_to_db(csv_file.decode('utf-8'), db)
        return JSONResponse(content={"message": message}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
