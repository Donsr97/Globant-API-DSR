from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DepartmentSchemas(BaseModel):
    """Columns related to departments table in database"""
    id: Optional[int] = None
    department: str