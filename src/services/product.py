from sqlalchemy.ext.asyncio import AsyncSession
from src.config.llm_config import llm_embedding
from src.schemas.product import ProductCreateRequest,ProductSearchRequest
from src.models.product import Product
from src.database.database import database_service

class ProductService:
    def __init__(self):
        self.llm_config = llm_embedding

    async def create_product(self, db: AsyncSession, request : ProductCreateRequest):
        product_text = f"""
        Product Name: {request.name}
        Description: {request.description}
        Brand: {request.brand}
        Category: {request.category}
        """

        embedding = await self.llm_config.create_embeddings(product_text)
        product = Product(
            name=request.name,
            description=request.description,
            brand=request.brand,
            category=request.category,
            price=request.price,
            stock=request.stock,
            embedding=embedding
        )
        return await database_service.create(db, product)
    
    async def search_products(self,db:AsyncSession , request : ProductSearchRequest):
        search_embedding = None
        if request.query:
            search_embedding = await self.llm_config.create_embeddings(request.query)

        products = await database_service.search_products(db,Product,search_embedding,request)

        print("SEARCH RESULTS:", products)
        print("RESULT COUNT:", len(products))

        return {
        "products": products
    }

    
product_service = ProductService()

