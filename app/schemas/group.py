from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.student import Student

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None

class Group(GroupBase):
    id: int
    students: List[Student] = []
    
    model_config = ConfigDict(from_attributes=True)