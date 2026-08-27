from src.graph.state import EcommerceState
from src.config.llm_config import llm_embedding
from src.schemas.chat import ProductQuery
from src.schemas.product import ProductSearchRequest
from src.graph.state import EcommerceRequest
from src.services.cart import cart_service
from src.services.product import product_service

# structured_llm = llm_embedding.llm.with_structured_output(ProductQuery)
# intent_llm = llm_embedding.llm.with_structured_output(IntentQuery)
# add_to_cart_llm = llm_embedding.llm.with_structured_output(AddToCartQuery)
# buy_product_llm = llm_embedding.llm.with_structured_output(BuyProductQuery)

request_llm = llm_embedding.llm.with_structured_output(
    EcommerceRequest
)
class nodes:
    async def extract_buy_request(self, state: EcommerceState):

        result = await request_llm.ainvoke(
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
        result = await request_llm.ainvoke(

              f"""
        You are an ecommerce request understanding system.

        Analyze the user's request and determine the intent.

        Possible intents:

        1. product_search
           User wants to find, search, compare or see products.

        2. add_to_cart
           User wants to add a product to their shopping cart.

        3. buy_product
           User wants to purchase or order a product.

        4. general
           General conversation that is not a product search,
           cart action or purchase.

        Extract the following when applicable:

        - product_query
        - quantity
        - brand
        - category
        - max_price

        For product_search:
        Extract brand, category, maximum price and the
        semantic product query.

        For add_to_cart:
        Extract the product name/query and quantity.

        For buy_product:
        Extract the product name/query and quantity.

        For general:
        product_query can be null.

        User request:
        {user_query}
        """
        )

        return {
        "intent": result.intent,
        "product_query": result.product_query,
        "quantity": result.quantity if result.quantity > 0 else 1,
        "filters": {
            "query": result.product_query,
            "brand": result.brand,
            "category": result.category,
            "max_price": result.max_price
        }
        }

    async def search_products(self ,state: EcommerceState,runtime):
        db = runtime.context["db"]
        filters = state["filters"]
        request = ProductSearchRequest(
        query=filters["query"],
        brand=filters["brand"],
        category=filters["category"],
        max_price=filters["max_price"],
        limit=5 )
        
        result  = await product_service.search_products(db = db , request= request)
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

        return {"products": product_data}

    
    async def generate_response(self , state: EcommerceState):
        user_query = state["user_query"]
        products = state["products"]

        print("GENERATE PRODUCTS:", products)
        print("PRODUCT COUNT:", len(products))
        
        product_details  = "\n".join(
            [
                f"""
                Product: {product["name"]}
                Brand: {product["brand"]}
                Category: {product["category"]}
                Price: ₹{product["price"]}
                Stock: {product["stock"]}                """
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
        if isinstance(response.content, list):
            response_text = "".join(
                block.get("text", "")
                for block in response.content
                if isinstance(block, dict)
        )
        else:
             response_text = str(response.content)
        print("LLM RESPONSE:", repr(response.content))
        return { "response":response_text ,
                "data": {
                    "action": "product_search",
            "count": len(products),
            "products": products
        }}

    
    async def fallback(self, state: EcommerceState):

        return {
            "response": (
                "Sorry, I couldn't find any products "
                "matching your requirements."
            )
        }
    async def limited_results(self, state: EcommerceState):

        products = state["products"]

        if not products:
            return {
                "response": "Sorry, I couldn't find any products matching your requirements.",
                "data": {
                    "count": 0,
                    "products": []
                }
            }

        product_list = "\n".join(
            f"- {product['name']} — {product['brand']}"
            for product in products
        )

        return {
            "response": (
                f"I found {len(products)} products:\n\n"
                f"{product_list}"
            ),
            "data": {
                "count": len(products),
                "products": products
            }
        }
    async def route_intent(self, state: EcommerceState):

        user_query = state["user_query"]

        result = await request_llm.ainvoke(
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

        result = await request_llm.ainvoke(
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
    async def find_product(self, state: EcommerceState,runtime):

        db = runtime.context["db"]


        filters = state["filters"]
        print("FIND PRODUCT FILTERS:", filters)
        print("FIND PRODUCT QUERY:", filters.get("query"))
        if not filters.get("query"):
            return {
                "products": [],
                "response": "Please include the product name when placing an order."
            }
        request = ProductSearchRequest(
            query=filters["query"],
            limit=1
        )
        request = ProductSearchRequest(
        query=filters.get("query"),
        brand=filters.get("brand"),
        category=filters.get("category"),
        max_price=filters.get("max_price"),
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
            "products": [ {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "brand": product.brand,
            "category": product.category,
            "price": float(product.price),
            "stock": product.stock
        }]
        }
    async def add_product_to_cart(self, state: EcommerceState,runtime):

        try:
            item = await cart_service.add_to_cart(
                db = runtime.context["db"],
                user_id=state["user_id"],
                product_id=state["product_id"],
                quantity=state["quantity"]
            )
            product = state["products"][0]
            total =  product["price"] * state["quantity"]

            print("CART ITEM:", product)

            return {
                "response": (
                       f"Added {state['quantity']} "
                      f"{product['name']} to your cart successfully."
                      
                      f"for ₹{total:,.2f}."
                ),
                "data": {
               "action": "add_to_cart",
                "cart_item_id": item.id,
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": state["quantity"],
                "price": product["price"],
                "total": total
        }
            }

        except ValueError as e:
            return {
                "response": str(e)
            }
    async def create_order(self, state: EcommerceState,runtime):
        try:
            order = await cart_service.create_order(
                db=runtime.context["db"],
                user_id=state["user_id"],
                product_id=state["product_id"],
                quantity=state["quantity"]
            )
        except ValueError as error:
            return {"response": str(error)}

        product = state["products"][0]

        total = product["price"] * state["quantity"]
        return {
            "response": (
                f"Order placed successfully! "
            f"Order ID: {order.id}. "
            f"{product['name']} × {state['quantity']} "
            f"for ₹{total:,.2f}."
            ),
             "data": {
            "action": "create_order",
            "order_id": order.id,
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": state["quantity"],
            "price": product["price"],
            "total": total
        }
        }
nodes_graph = nodes()