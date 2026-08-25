import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase ,Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self.engine =  create_async_engine(DATABASE_URL ,echo = True)
        self.sessionLocal = async_sessionmaker(bind = self.engine , autoflush=False, autocommit = False)

    async def get_db(self):
        db = self.sessionLocal()

        try:
            yield db
        finally:
           await db.close()

    async def create(self , db: AsyncSession, model):
        db.add(model)
        await db.commit()
        await db.refresh(model)
        return model
    
    async def get_user_by_email(self,  db: Session,email: str, User):
        statement = select(User).where(User.email == email)
        return await db.execute(statement).scalar_one_or_none()  

    async def search_products(self,db: AsyncSession, model ,embeddings,request):
        query = select(model)
        if request.brand:
            query = query.where( model.brand.ilike(request.brand))
        if request.category:
            query = query.where(model.category.ilike(request.category))
        if request.max_price is not None:
            query = query.where( model.price <= request.max_price )

        result =  query.order_by(model.embedding.cosine_distance(embeddings)).limit(request.limit)
        result = await db.execute(query)
        products =  result.scalars().all()
       
        return products
        

class Base(DeclarativeBase):
    pass

database = Database()