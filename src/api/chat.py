from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import database_service
from src.schemas.chat import ChatRequest, ChatResponse
from fastapi import APIRouter, Depends, Request

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
@router.post("/", response_model=ChatResponse)
async def chat( request: Request, chat_request: ChatRequest, db: AsyncSession = Depends(database_service.get_db)):      
        graph = request.app.state.ecommerce_graph

        result = await graph.ainvoke(
    {
        "user_query": chat_request.message,
        "user_id": 1,
        "intent": "",
        "product_query": None,
        "quantity": 1,
        "filters": {},
        "products": [],
        "product_id": None,
        "response": "",
        "data": {}
    }, 
    config={
            "configurable": {
                "thread_id": "user-1"
            }
        },
    context={"db": db}
)

        return {
        "response": result["response"],
        "intent": result.get("intent"),
         "data": result.get("data", {})
         } 