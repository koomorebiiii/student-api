from fastapi import FastAPI
from app.api.v1 import students, groups  
from app.core.database import engine, Base
from app.config import settings

app = FastAPI(title="Students API")

@app.on_event("startup")
async def startup():
    print("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(students.router, prefix="/api/v1")
app.include_router(groups.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Students API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}