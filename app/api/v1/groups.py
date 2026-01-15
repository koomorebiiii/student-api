from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db 
from app.schemas import group as schemas
from app.schemas import student as student_schemas
from app.services.group_service import GroupService  
from app.services.student_service import StudentService

router = APIRouter(prefix="/groups", tags=["groups"])  

@router.post("/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
async def create_group(
    group: schemas.GroupCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await GroupService.create_group(db, group)

@router.get("/", response_model=List[schemas.Group])
async def read_groups(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await GroupService.get_groups(db, skip, limit)

@router.get("/{group_id}", response_model=schemas.Group)
async def read_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_group = await GroupService.get_group(db, group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    if not await GroupService.delete_group(db, group_id):
        raise HTTPException(status_code=404, detail="Group not found")

@router.get("/{group_id}/students", response_model=List[student_schemas.Student])
async def get_students_in_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    students = await GroupService.get_students_in_group(db, group_id)
    return students


@router.post("/add-student", response_model=student_schemas.Student)
async def api_add_student_to_group(
    student_id: int,
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Добавить студента в группу (ваш формат)"""
    result = await StudentService.add_to_group(db, student_id, group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student or Group not found")
    return result

@router.post("/transfer-student", response_model=student_schemas.Student)
async def api_transfer_student(
    student_id: int,
    from_group_id: int,
    to_group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Перевести студента из группы A в группу B (ваш формат)"""
    # Сначала проверяем, что студент в from_group_id
    student = await StudentService.get_student(db, student_id)
    if not student or student.group_id != from_group_id:
        raise HTTPException(status_code=404, detail="Student not found in source group")
    
    # Переводим
    result = await StudentService.add_to_group(db, student_id, to_group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Target group not found")
    return result