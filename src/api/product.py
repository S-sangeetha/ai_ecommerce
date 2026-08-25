from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import database_service
from src.schemas.product import ProductCreateRequest,ProductSearchRequest,ProductResponse
from src.services.product import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/")
async def create_product(
    request: ProductCreateRequest,
    db: AsyncSession = Depends(database_service.get_db)
):

    return await product_service.create_product(db, request)

@router.post("/search", response_model=list[ProductResponse])
async def search_products(request : ProductSearchRequest , db: AsyncSession = Depends(database_service.get_db)):
    return await product_service.search_products(db = db , request= request)
