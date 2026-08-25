from typing import TypedDict, Any
from typing import Literal
from pydantic import BaseModel

class EcommerceState(TypedDict):
    user_query: str
    intent: str
    filters: dict[str, Any]
    products : list
    response : str
    db: Any

class IntentQuery(BaseModel):
    intent: Literal[
        "product_search",
        "add_to_cart",
        "buy_product",
        "general"
    ]