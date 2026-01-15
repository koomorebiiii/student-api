from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core import models
from app.schemas import student as schemas

class StudentService:
    @staticmethod
    async def get_student(db: AsyncSession, student_id: int):
        result = await db.execute(
            select(models.Student).where(models.Student.id == student_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(models.Student).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def create_student(db: AsyncSession, student: schemas.StudentCreate):
        db_student = models.Student(
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email
        )
        db.add(db_student)
        await db.commit()
        await db.refresh(db_student)
        return db_student
    
    @staticmethod
    async def update_student(db: AsyncSession, student_id: int, student_update: schemas.StudentUpdate):
        result = await db.execute(
            select(models.Student).where(models.Student.id == student_id)
        )
        db_student = result.scalar_one_or_none()
        
        if not db_student:
            return None
        
        update_data = student_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        await db.commit()
        await db.refresh(db_student)
        return db_student
    
    @staticmethod
    async def delete_student(db: AsyncSession, student_id: int):
        result = await db.execute(
            select(models.Student).where(models.Student.id == student_id)
        )
        db_student = result.scalar_one_or_none()
        
        if db_student:
            await db.delete(db_student)
            await db.commit()
            return True
        return False
    
    @staticmethod
    async def add_to_group(db: AsyncSession, student_id: int, group_id: int):
        result = await db.execute(
            select(models.Student).where(models.Student.id == student_id)
        )
        db_student = result.scalar_one_or_none()
        
        if not db_student:
            return None
        
        # Проверяем существует ли группа
        group_result = await db.execute(
            select(models.Group).where(models.Group.id == group_id)
        )
        group = group_result.scalar_one_or_none()
        
        if not group:
            return None
        
        db_student.group_id = group_id
        await db.commit()
        await db.refresh(db_student)
        return db_student
    
    @staticmethod
    async def remove_from_group(db: AsyncSession, student_id: int):
        result = await db.execute(
            select(models.Student).where(models.Student.id == student_id)
        )
        db_student = result.scalar_one_or_none()
        
        if not db_student:
            return None
        
        db_student.group_id = None
        await db.commit()
        await db.refresh(db_student)
        return db_student
    
    @staticmethod
    async def transfer_student(db: AsyncSession, student_id: int, new_group_id: int):
        return await StudentService.add_to_group(db, student_id, new_group_id)