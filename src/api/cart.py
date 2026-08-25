from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import database_service
from src.services.cart import cart_service
router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)
@router.post("/add")
async def add_to_cart(
    product_id: int,
    quantity: int,
    current_user :int  = 1,
    db: AsyncSession = Depends(database_service.get_db)
):
    item = await cart_service.add_to_cart(
        db=db,
        user_id=current_user,
        product_id=product_id,
        quantity=quantity
    )

    return {
        "message": "Product added to cart",
        "cart_item_id": item.id,
        "quantity": item.quantity
    }