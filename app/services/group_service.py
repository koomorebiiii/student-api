from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core import models
from app.schemas import group as schemas

class GroupService:
    @staticmethod
    async def get_group(db: AsyncSession, group_id: int):
        result = await db.execute(
            select(models.Group)
            .options(selectinload(models.Group.students))
            .where(models.Group.id == group_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_groups(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(models.Group)
            .options(selectinload(models.Group.students))
            .offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def create_group(db: AsyncSession, group: schemas.GroupCreate):
        db_group = models.Group(name=group.name)
        db.add(db_group)
        await db.commit()
        await db.refresh(db_group)
        return db_group
    
    @staticmethod
    async def update_group(db: AsyncSession, group_id: int, group_update: schemas.GroupUpdate):
        result = await db.execute(
            select(models.Group).where(models.Group.id == group_id)
        )
        db_group = result.scalar_one_or_none()
        
        if not db_group:
            return None
        
        update_data = group_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_group, field, value)
        
        await db.commit()
        await db.refresh(db_group)
        return db_group
    
    @staticmethod
    async def delete_group(db: AsyncSession, group_id: int):
        result = await db.execute(
            select(models.Group).where(models.Group.id == group_id)
        )
        db_group = result.scalar_one_or_none()
        
        if db_group:
            await db.delete(db_group)
            await db.commit()
            return True
        return False
    
    @staticmethod
    async def get_students_in_group(db: AsyncSession, group_id: int):
        result = await db.execute(
            select(models.Group)
            .options(selectinload(models.Group.students))
            .where(models.Group.id == group_id)
        )
        group = result.scalar_one_or_none()
        
        return group.students if group else []