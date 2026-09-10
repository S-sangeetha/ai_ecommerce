import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def search_products(
    query: str | None = None,
    name: str | None = None,
    brand: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    limit: int = 5
):
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp/server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "search_products",
                arguments={
                    "query": query,
                    "name": name,
                    "brand": brand,
                    "category": category,
                    "min_price": min_price,
                    "max_price": max_price,
                    "limit": limit
                }
            )

            # MCP returns the result as TextContent
            text = result.content[0].text

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "MCP_RESPONSE_NOT_JSON",
                    "raw_response": text
    }


    
async def add_to_cart(
    user_id: int,
    product_id: int,
    quantity: int = 1
):
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp/server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "add_to_cart",
                arguments={
                    "user_id": user_id,
                    "product_id": product_id,
                    "quantity": quantity
                }
            )

            text = result.content[0].text

            try:
                return json.loads(text)

            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "MCP_RESPONSE_NOT_JSON",
                    "raw_response": text
                }
async def main():

    result = await search_products(
        query="laptop"
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())