from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class JobSchema(BaseModel):
    """Columns related to jobs table in database"""
    id: Optional[int] = None
    job: str
