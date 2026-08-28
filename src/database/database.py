import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase ,Session
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, func
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
        if request.name:
            query = query.where( model.name.ilike(request.name.strip()))
        if request.brand:
            query = query.where( model.brand.ilike(request.brand.strip()))

        if request.category:
            query = query.where( model.category.ilike(request.category.strip()))

        if request.min_price is not None:
            query = query.where(model.price >= request.min_price)

        if request.max_price is not None:
            query = query.where(model.price <= request.max_price)

        if embeddings is not None:
            query = query.order_by(model.embedding.cosine_distance(embeddings) )

        query = query.limit(request.limit)

        result = await db.execute(query)

        products = result.scalars().all()

        if products:
            return products
        
        fuzzy_query = select(model)
        if request.name:
            name = request.name.strip()
            fuzzy_query = fuzzy_query.where(func.similarity(model.name, name) >= 0.3)
        if request.brand:
            brand = request.brand.strip()
            fuzzy_query = fuzzy_query.where(func.similarity(model.brand, brand) >= 0.3)
        if request.category:
            category = request.category.strip()
            fuzzy_query = fuzzy_query.where(func.similarity(model.category, category) >= 0.3)
        if request.min_price is not None:
             fuzzy_query = fuzzy_query.where( model.price >= request.min_price )
        if request.max_price is not None:
            fuzzy_query = fuzzy_query.where( model.price <= request.max_price )
        if embeddings is not None:
             fuzzy_query = fuzzy_query.order_by( model.embedding.cosine_distance(embeddings))
        fuzzy_query = fuzzy_query.limit(request.limit)
        result = await db.execute(fuzzy_query)
        return result.scalars().all()

    async def add_to_cart(self,db:AsyncSession,user_id: int ,product_id: int, quantity: int  , cart_model , cart_item_model, product_model):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        result = await db.execute(select(product_model).where(product_model.id == product_id) )
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")
        if product.stock < quantity:
            raise ValueError(f"Only {product.stock} units are available")
        result = await db.execute(select(cart_model).where(cart_model.user_id == user_id))
        cart = result.scalar_one_or_none()
        if not cart:
            cart = cart_model(user_id=user_id)

            db.add(cart)

            await db.flush()
        result = await db.execute(select(cart_item_model).where(cart_item_model.cart_id == cart.id,cart_item_model.product_id == product_id ) )
        cart_item = result.scalar_one_or_none()
        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                raise ValueError(
                        f"Only {product.stock} units are available"
                    )

            cart_item.quantity = new_quantity

        else:

            cart_item = cart_item_model(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )

        db.add(cart_item)

        await db.commit()

        await db.refresh(cart_item)

        return cart_item
    async def create_order(self,db: AsyncSession, user_id: int,product_id: int, quantity: int, product_model,order_model):
      try:
        result = await db.execute(
        select(product_model).where(
            product_model.id == product_id
        ).with_for_update()
        )

        product = result.scalar_one_or_none()

        if not product:
            raise ValueError("Product not found")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if product.stock < quantity:
            raise ValueError(
                f"Only {product.stock} item(s) are available"
            )

    
        total_price = product.price * quantity

        order = order_model(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status="confirmed"
        )

        
        product.stock -= quantity
        db.add(order)
        
        await db.commit()
        
        await db.refresh(order)
        return order
      except Exception: 
        await db.rollback()
        raise

      
    async def get_cart(self,db: AsyncSession,user_id: int,cart_model,cart_item_model ,product_model ):
        result = await db.execute(
            select(cart_item_model, product_model)
            .join(product_model, cart_item_model.product_id == product_model.id)
            .join(cart_model, cart_item_model.cart_id == cart_model.id)
            .where(cart_model.user_id == user_id)
        )

        return result.all()   
class Base(DeclarativeBase):
    pass

database_service = Database()