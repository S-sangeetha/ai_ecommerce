from sqlalchemy.orm import Session
from src.schemas.user import UserCreate
from src.models.user import User
from src.database.database import database_service
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    async def create_user(self,db: AsyncSession , request :UserCreate  ):
        existing_user = database_service.get_user_by_email(db,request.email,User)
        if existing_user:
            raise ValueError("Email already exists")

        user = User(
            name=request.name,
            email = request.email,
            password = request.password
        )
        return await database_service.create(db, user)

user_service = UserService()