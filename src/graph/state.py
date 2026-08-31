from typing import TypedDict, Any
from typing import Literal
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class EcommerceState(TypedDict):
    user_query: str
    user_id: int
    
    intent: str

    product_query: str | None
    quantity: int

    filters: dict[str, Any]
    products: list

    product_id: int | None

    response: str
    data: dict
class EcommerceContext(TypedDict):
    db: AsyncSession

class EcommerceRequest(BaseModel):
    intent: Literal[
        "product_search",
        "add_to_cart",
        "buy_product",
        "get_cart",
        "remove_from_cart",
        "update_cart",
        "general"
    ]

    product_query: str | None = None
    quantity: int = 1
    name :str |None = None
    brand: str | None = None
    category: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    

# class IntentQuery(BaseModel):
#     intent: Literal[
#         "product_search",
#         "add_to_cart",
#         "buy_product",
#         "general"
#     ]
# class AddToCartQuery(BaseModel):
#     product_query: str
#     quantity: int = 1

# class BuyProductQuery(BaseModel):

#     product_query: str

#     quantity: int = 1