from src.models.cart import Cart, CartItem
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import database_service
from src.models.cart import Cart, CartItem
from src.models.product import Product
from src.models.order import Order

class CartService:
    async def add_to_cart(self,db: AsyncSession, user_id: int,  product_id: int,quantity: int = 1 ):
         cart_item =await database_service.add_to_cart( db=db, user_id=user_id,  product_id=product_id, quantity=quantity ,cart_model = Cart , cart_item_model =CartItem , product_model=Product)
         return cart_item
    async def grt_cart(self,db: AsyncSession, user_id: int):
        cart_products = await database_service.get_cart(db= db , user_id= user_id,cart_model = Cart, cart_item_model =CartItem , product_model=Product )
        return cart_products


    async def create_order(self, db: AsyncSession,user_id: int,product_id: int,quantity: int):
        order = await database_service.create_order(
            db=db,
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            product_model=Product,
            order_model=Order)
        return order

cart_service = CartService()