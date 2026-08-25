from langgraph.graph import StateGraph, START, END

from src.graph.state import EcommerceState
from src.graph.nodes import  nodes_graph



def route_after_search(state: EcommerceState):

    products = state["products"]

    if len(products) == 0:
        return "fallback"

    if len(products) < 3:
        return "limited_results"


    return "generate_response"
def route_by_intent(state: EcommerceState):

    intent = state["intent"]

    if intent == "product_search":
        return "understand_query"

    return "general"

def create_graph():
    graph = StateGraph(EcommerceState)
    graph.add_node("understand_query",nodes_graph.understand_query)
    graph.add_node("search_products",nodes_graph.search_products)
    graph.add_node("generate_response",nodes_graph.generate_response)
    graph.add_node("fallback",nodes_graph.fallback)
    graph.add_node("limited_results",nodes_graph.limited_results)

    graph.add_edge(START ,"understand_query" )
    graph.add_edge("understand_query", "search_products")
    graph.add_conditional_edges( "search_products",  route_after_search,
    {
        "generate_response": "generate_response",
        "limited_results": "limited_results",
        "fallback": "fallback"
     }
    )
    graph.add_edge("fallback",END)
    graph.add_edge("limited_results", END)
    graph.add_edge("generate_response",END)

    return graph.compile()

ecommerce_graph = create_graph()