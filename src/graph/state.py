from typing import TypedDict, Any
from typing import Literal
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class EcommerceState(TypedDict):
    user_query: str
    user_id: int
    db: AsyncSession
    intent: str
    filters: dict[str, Any]
    products : list
    product_id: int
    quantity: int
    product_name: str
    total_price: float
    response : str
    

class IntentQuery(BaseModel):
    intent: Literal[
        "product_search",
        "add_to_cart",
        "buy_product",
        "general"
    ]
class AddToCartQuery(BaseModel):
    product_query: str
    quantity: int = 1

class BuyProductQuery(BaseModel):

    product_query: str

    quantity: int = 1