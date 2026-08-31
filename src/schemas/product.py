from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime
from typing import Optional


class ProductCreateRequest(BaseModel):

    name: str = Field(..., min_length=1)
    description: str
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    brand: str
    category: str
    
class ProductSearchRequest(BaseModel):
    query: str | None = None
    name:str | None =None
    brand: str | None = None
    category: str | None = None
    
    min_price: float | None = Field(
        default=None,
        ge=0
    )

    max_price: float | None = Field(
        default=None,
        ge=0
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20
    )


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