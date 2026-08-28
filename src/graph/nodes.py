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

              f"""Extract structured information from this ecommerce request.

                Intent MUST be exactly one of these values:
                - product_search
                - add_to_cart
                - buy_product
                - get_cart
                - general

                Intent definitions:

                product_search:
                User wants to search, find, compare, or browse products.

                add_to_cart:
                User wants to add a product to their cart.

                buy_product:
                User wants to directly purchase a product.

                get_cart:
                User wants to view their existing shopping cart.

                Examples of get_cart:
                - Show my cart
                - View my cart
                - What's in my cart?
                - What is in my cart?
                - Show cart
                - View cart
                - Cart

                general:
                Anything unrelated to product search or shopping actions.

                Extract:
                - intent
                - product_query
                - quantity
                - name
                - brand
                - category
                - min_price
                - max_price

                IMPORTANT:
                - For get_cart, product_query must be null.
                - For get_cart, name must be null.
                - For get_cart, brand must be null.
                - For get_cart, category must be null.
                - For get_cart, min_price must be null.
                - For get_cart, max_price must be null.
                - Do not invent values.

                IMPORTANT:
                - category must contain only the product type.
                - product_query must contain only the meaningful
                semantic requirement for product matching.
                - Do not repeat brand, category, or price inside product_query.
                - If there is no semantic requirement, set product_query to null.

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
            "name":result.name,
            "brand": result.brand,
            "category": result.category,
            "min_price": result.min_price,
            "max_price": result.max_price
        }
        }

    async def search_products(self ,state: EcommerceState,runtime):
        db = runtime.context["db"]
        filters = state["filters"]
        request = ProductSearchRequest(
        query=filters.get("query"),
        name = filters.get("name"),
        brand=filters.get("brand"),
        category=filters.get("category"),
        max_price=filters.get("max_price"),
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
                    "action": "product_search",
                    "count": 0,
                    "products": []
                }
            }

        product_list = "\n".join(
        f"{i + 1}. {product['name']} — "
        f"₹{product['price']:,.2f} "
        f"({product['brand']}) — "
        f"Stock: {product['stock']}"
        for i, product in enumerate(products)
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
            "response":  self.extract_text(response.content)
        }
    async def find_product(self, state: EcommerceState,runtime):

        db = runtime.context["db"]


        filters = state["filters"]
        print("FIND PRODUCT FILTERS:", filters)
        print("FIND PRODUCT QUERY:", filters.get("query"))
        product_name = filters.get("name") or filters.get("query")

        if not product_name:
            return {
                "products": [],
                "response": "Please include the product name when placing an order."
            }
        request = ProductSearchRequest(
            query=product_name,
            brand=filters.get("brand"),
            category=filters.get("category"),
            min_price=filters.get("min_price"),
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

    async def get_cart(self, state: EcommerceState,runtime):
        db = runtime.context["db"]
        items = await cart_service.get_cart(db=db,user_id=state["user_id"])
        if not items :
            return {
            "response": "Your cart is empty.",
            "data": {
                "action": "get_cart",
                "count": 0,
                "items": [],
                "total": 0
            }
        }
        cart_items = []
        total = 0
        for cart_item, product in items:
          item_total = float(product.price) * cart_item.quantity
          total += item_total
          cart_items.append({
            "cart_item_id": cart_item.id,
            "product_id": product.id,
            "product_name": product.name,
            "brand": product.brand,
            "quantity": cart_item.quantity,
            "price": float(product.price),
            "item_total": item_total
        })

        return {
            "response": (
                f"You have {len(cart_items)} item(s) in your cart. "
                f"Total: ₹{total:,.2f}"
            ),
            "data": {
                "action": "get_cart",
                "count": len(cart_items),
                "items": cart_items,
                "total": total
            }
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
    def extract_text(self,content):
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            )

        return str(content)
nodes_graph = nodes()