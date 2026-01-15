from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db  
from app.schemas import student as schemas
from app.services.student_service import StudentService  

router = APIRouter(prefix="/students", tags=["students"])  

@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: schemas.StudentCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.create_student(db, student)

@router.get("/", response_model=List[schemas.Student])
async def read_students(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await StudentService.get_students(db, skip, limit)

@router.get("/{student_id}", response_model=schemas.Student)
async def read_student(
    student_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_student = await StudentService.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int, 
    db: AsyncSession = Depends(get_db)
):
    if not await StudentService.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")

@router.post("/{student_id}/groups/{group_id}", response_model=schemas.Student)
async def add_student_to_group(
    student_id: int, 
    group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await StudentService.add_to_group(db, student_id, group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student or Group not found")
    return result

@router.delete("/{student_id}/groups", response_model=schemas.Student)
async def remove_student_from_group(
    student_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await StudentService.remove_from_group(db, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result

@router.put("/{student_id}/transfer/{new_group_id}", response_model=schemas.Student)
async def transfer_student(
    student_id: int, 
    new_group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await StudentService.transfer_student(db, student_id, new_group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student or Group not found")
    return result