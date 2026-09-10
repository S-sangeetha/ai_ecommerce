import asyncio
import selectors
import sys
from pathlib import Path
from src.models.cart import Cart,CartItem
from src.models.product import Product

asyncio.set_event_loop_policy(
    asyncio.WindowsSelectorEventLoopPolicy()
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from mcp.server import MCPServer
from sqlalchemy import text
from src.schemas.product import ProductSearchRequest
from src.services.product import product_service
from src.database.database import database_service


mcp = MCPServer("AI Ecommerce")

@mcp.tool()
async def search_products(
        query: str | None = None,
        name: str | None = None,
        brand: str | None = None,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        limit: int = 5
    ) -> dict:

        try:
            request = ProductSearchRequest(
                query=query,
                name=name,
                brand=brand,
                category=category,
                min_price=min_price,
                max_price=max_price,
                limit=limit
            )

            async with database_service.sessionLocal() as db:

                result = await product_service.search_products(
                    db=db,
                    request=request
                )

            products = result["products"]

            product_data = [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "brand": product.brand,
                    "category": product.category,
                    "price": float(product.price),
                    "stock": product.stock
                }
                for product in products
            ]

            return {
                "success": True,
                "query": query,
                "products": product_data
            }

        except Exception as e:
            return {
                "success": False,
                "error_type": type(e).__name__,
                "error": str(e)
            }

@mcp.tool()
async def add_to_cart(
        user_id: int,
        product_id: int,
        quantity: int = 1,
    ) -> dict:

        try:
            async with database_service.sessionLocal() as db:

                cart_item = await database_service.add_to_cart(
                    db=db,
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity,
                    cart_model=Cart,
                    cart_item_model=CartItem,
                    product_model=Product
                )

            return {
                "success": True,
                "cart_item_id": cart_item.id,
                "product_id": cart_item.product_id,
                "quantity": cart_item.quantity
            }

        except Exception as e:
            return {
                "success": False,
                "error_type": type(e).__name__,
                "error": str(e)
            }

if __name__ == "__main__":
    mcp.run()