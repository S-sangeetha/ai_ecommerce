from src.graph.state import EcommerceState
from src.config.llm_config import llm_embedding
from src.schemas.chat import ProductQuery
from src.schemas.product import ProductSearchRequest
from src.graph.state import IntentQuery,AddToCartQuery,BuyProductQuery
from src.services.cart import cart_service
from src.services.product import product_service

structured_llm = llm_embedding.llm.with_structured_output(ProductQuery)
intent_llm = llm_embedding.llm.with_structured_output(IntentQuery)
add_to_cart_llm = llm_embedding.llm.with_structured_output(AddToCartQuery)
buy_product_llm = llm_embedding.llm.with_structured_output(BuyProductQuery)
class nodes:
    async def extract_buy_request(self, state: EcommerceState):

        result = await buy_product_llm.ainvoke(
            f"""
            Extract the product and quantity from this
            ecommerce purchase request.

            User request:
            {state["user_query"]}

            Return:
            - product_query
            - quantity
            """
        )

        return {
            "filters": {
                "query": result.product_query
            },
            "quantity": result.quantity
        }
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
        
        result  = await product_service.search_products(db = db , request= request)
        products = result["products"]
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

        result = await intent_llm.ainvoke(
            f"""
            Determine the intent of this ecommerce user query.

            Possible intents:

            - product_search:
             User wants to find, search, compare or see products.

             - add_to_cart:
            User wants to add a product to their shopping cart.

             - buy_product:
               User wants to purchase/order a product.
            - general:
              General conversation that is not a product search,
            cart action or purchase.
            User query:
            {user_query}

            Return only the appropriate intent.
            """
        )

        return {
            "intent": result.intent
        }
    
    async def extract_cart_request(self, state: EcommerceState):

        user_query = state["user_query"]

        result = await add_to_cart_llm.ainvoke(
            f"""
            Extract the product and quantity from this ecommerce request.

            User request:
            {user_query}

            Return:
            - product_query
            - quantity
            """
        )

        print("CART QUERY:", result.product_query)
        print("CART QUANTITY:", result.quantity)

        return {
            "filters": {
                "query": result.product_query
            },
            "quantity": result.quantity
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
    async def find_product(self, state: EcommerceState):

        db = state["db"]

        filters = state["filters"]

        request = ProductSearchRequest(
            query=filters["query"],
            limit=1
        )

        result  = await product_service.search_products(
            db=db,
            request=request
        )
        products = result["products"]
        print("PRODUCT LIST:", products)
       
        if not products:

            return {
                "products": [],
                "response": "Sorry, I couldn't find that product."
            }

        product = products[0]
        print("SELECTED PRODUCT:", product.id, product.name)
        return {
            "product_id": product.id,
            "products": [product]
        }
    async def add_product_to_cart(self, state: EcommerceState):

        print("PRODUCT ID:", state["product_id"])
        print("QUANTITY:", state["quantity"])
        print("USER ID:", state["user_id"])

        try:
            item = await cart_service.add_to_cart(
                db=state["db"],
                user_id=state["user_id"],
                product_id=state["product_id"],
                quantity=state["quantity"]
            )

            print("CART ITEM:", item)

            return {
                "response": (
                    f"Added {state['quantity']} item(s) "
                    f"to your cart successfully."
                )
            }

        except ValueError as e:
            return {
                "response": str(e)
            }
    async def create_order(self, state: EcommerceState):

        order = await cart_service.create_order(
            db=state["db"],
            user_id=state["user_id"],
            product_id=state["product_id"],
            quantity=state["quantity"]
        )

        return {
            "response": (
                f"Order placed successfully. "
                f"Order ID: {order.id}"
            )
        }
nodes_graph = nodes()