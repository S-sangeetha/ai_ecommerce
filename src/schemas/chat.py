from pydantic import BaseModel

class ProductQuery(BaseModel):
    query: str
    brand: str | None = None
    category: str | None = None
    max_price: float | None = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str

