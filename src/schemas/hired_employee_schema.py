from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class HiredEmployeeSchema(BaseModel):
    """Columns related to hired_employees table in database"""
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int
