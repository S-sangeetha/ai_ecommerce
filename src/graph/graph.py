from langgraph.graph import StateGraph, START, END

from src.graph.state import EcommerceState , EcommerceContext
from src.graph.nodes import  nodes_graph
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

def route_by_intent(state: EcommerceState):

        intent = state["intent"]

        if intent == "product_search":
            return "product_search"

        if intent == "add_to_cart":
            return "add_to_cart"

        if intent == "buy_product":
            return "buy_product"
        
        if intent == "get_cart":
          return "get_cart"
        
        if intent == "remove_from_cart":
            return "remove_from_cart"

        if intent == "update_cart":
            return "update_cart"
        
        return "general"

def route_after_search(state: EcommerceState):

    products = state["products"]

    if not products:
        return "fallback"

    return "limited_results"

def route_after_product(state: EcommerceState):
    products = state.get("products", [])

    if not products:
        return "fallback"

    if state["intent"] == "add_to_cart":
        return "add_product_to_cart"
    if state["intent"] == "buy_product":
        return "create_order"
    if state["intent"] == "remove_from_cart":
        return "remove_from_cart"
    if state["intent"] == "update_cart":
       return "update_cart"
    return "fallback"

def create_graph(checkpointer):
    graph = StateGraph(EcommerceState,context_schema=EcommerceContext)
    graph.add_node(
        "understand_query",
        nodes_graph.understand_query
    )

    graph.add_node(
        "search_products",
        nodes_graph.search_products
    )

    graph.add_node(
        "find_product",
        nodes_graph.find_product
    )

    graph.add_node(
        "add_product_to_cart",
        nodes_graph.add_product_to_cart
    )
    graph.add_node(
        "get_cart",
        nodes_graph.get_cart
    )

    graph.add_node(
        "create_order",
        nodes_graph.create_order
    )

    graph.add_node(
        "generate_response",
        nodes_graph.generate_response
    )

    graph.add_node(
        "limited_results",
        nodes_graph.limited_results
    )
    graph.add_node(
        "remove_from_cart",
        nodes_graph.remove_from_cart
    )
    graph.add_node(
        "fallback",
        nodes_graph.fallback
    )

    graph.add_node(
        "general",
        nodes_graph.general
    )
    graph.add_node(
    "update_cart",
    nodes_graph.update_cart
)
    
    graph.add_edge(
        START,
        "understand_query"
    )


    graph.add_conditional_edges(
        "understand_query",
        route_by_intent,
        {
            "product_search": "search_products",
            "add_to_cart": "find_product",
            "buy_product": "find_product",
            "get_cart": "get_cart",
            "remove_from_cart": "find_product",
            "update_cart": "find_product",
            "general": "general"
        }
    )


    graph.add_conditional_edges(
        "search_products",
        route_after_search,
        {
            "limited_results": "limited_results",
            "fallback": "fallback"
        }
    )


    graph.add_conditional_edges(
        "find_product",
        route_after_product,
        {
            "add_product_to_cart": "add_product_to_cart",
            "create_order": "create_order",
            "remove_from_cart" :"remove_from_cart",
            "update_cart": "update_cart",
            "fallback": "fallback"
        }
    )


    # graph.add_edge("generate_response", END)
    graph.add_edge("limited_results", END)
    graph.add_edge("fallback", END)
    graph.add_edge("general", END)
    graph.add_edge("add_product_to_cart", END)
    graph.add_edge("create_order", END)
    graph.add_edge("remove_from_cart", END)
    graph.add_edge("get_cart", END)
    graph.add_edge("update_cart", END)


    return graph.compile( checkpointer=checkpointer)

