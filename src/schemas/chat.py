from pydantic import BaseModel

class ProductQuery(BaseModel):
    query: str | None = None
    name :str | None = None
    brand: str | None = None
    category: str | None = None
    min_price: float | None = None
    max_price: float | None = None


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: str | None = None
    data: dict = {} 

