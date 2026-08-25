from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import database_service
from src.schemas.user import UserCreate
from src.services.user import user_service


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)


@router.post("/register")

def register(request: UserCreate ,  db: AsyncSession = Depends(database_service.get_db)):
    return user_service.create_user(db , request)