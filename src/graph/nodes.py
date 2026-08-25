from src.graph.state import EcommerceState
from src.config.llm_config import llm_embedding
from src.schemas.chat import ProductQuery
from src.schemas.product import ProductSearchRequest
from src.graph.state import IntentQuery

from src.services.product import product_service

structured_llm = llm_embedding.llm.with_structured_output(ProductQuery)
intent_llm = llm_embedding.llm.with_structured_output(IntentQuery)
class nodes:
    async def understand_query(self , state : EcommerceState):
        user_query  = state['user_query']
        result = await structured_llm.ainvoke(

            f"""
            Understand this ecommerce product search query.
            Extract:
            - brand
            - category
            - maximum price
            - semantic search query
            User query:
            {user_query}
            """
        )

        return {
            "filters": { "query": result.query,"brand": result.brand,"category": result.category, "max_price": result.max_price}
        }

    async def search_products(self ,state: EcommerceState):
        db = state["db"]
        filters = state["filters"]
        request = ProductSearchRequest(
        query=filters["query"],
        brand=filters["brand"],
        category=filters["category"],
        max_price=filters["max_price"],
        limit=5 )
        
        products = await product_service.search_products(db = db , request= request)
        
        return {"products": products}

    
    async def generate_response(self , state: EcommerceState):
        user_query = state["user_query"]
        products = state["products"]

        print("GENERATE PRODUCTS:", products)
        print("PRODUCT COUNT:", len(products))
        
        product_details  = "\n".join(
            [
                f"""
                 Product: {product.name}
                 Description: {product.description}
                 Brand: {product.brand}
                 Category: {product.category} 
                 Price: ₹{product.price}
                 Stock: {product.stock}
                """
                for product in products
            ]
        )
        prompt = f"""
        You are an AI ecommerce shopping assistant.
        User request:
        {user_query}
        Here are the product details found from the database:
        {product_details}
        Rules:
        - Use ONLY the information provided in the database results.
        - Never assume or invent stock availability.
        - If stock is 0, say the product is out of stock.
        - Do not invent specifications, features, discounts, or availability.
        - Mention the product name and price.
        """
        response = await llm_embedding.llm.ainvoke(prompt)
        print("LLM RESPONSE:", repr(response.content))
        return { "response": response.content}

    
    async def fallback(self, state: EcommerceState):

        return {
            "response": (
                "Sorry, I couldn't find any products "
                "matching your requirements."
            )
        }
    async def limited_results(self, state: EcommerceState):

        products = state["products"]

        return {
            "response": (
                f"I found only {len(products)} products "
                "matching your requirements."
            )
        }
    
    async def route_intent(self, state: EcommerceState):

        user_query = state["user_query"]

        result = await structured_llm.ainvoke(
            f"""
            Determine the intent of this ecommerce user query.

            Possible intents:

            1. product_search
            User wants to find, search, compare, or recommend products.

            2. general
            General conversation or questions that are not product searches.

            User query:
            {user_query}

            Return only the appropriate intent.
            """
        )

        return {
            "intent": result.intent
        }
    async def general(self, state: EcommerceState):

        user_query = state["user_query"]

        response = await llm_embedding.llm.ainvoke(
            f"""
            You are an AI ecommerce assistant.

            Answer the user's general question.

            User:
            {user_query}
            """
        )

        return {
            "response": response.content
        }
nodes_graph = nodes()