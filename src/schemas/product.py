from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime


class ProductCreateRequest(BaseModel):

    name: str = Field(..., min_length=1)
    description: str
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    brand: str
    category: str
    
class ProductSearchRequest(BaseModel):
    query : str
    brand :str
    category :str
    max_price : float
    limit : int = 5


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    brand: str
    category: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)