from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    group_id: Optional[int] = None

class Student(StudentBase):
    id: int
    group_id: Optional[int]
    
    model_config = ConfigDict(from_attributes=True)