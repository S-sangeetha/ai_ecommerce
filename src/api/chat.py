from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import database_service
from src.schemas.chat import ChatRequest, ChatResponse
from src.graph.graph import ecommerce_graph

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(database_service.get_db)
):
        result = await ecommerce_graph.ainvoke(
    {
        "user_query": request.message,
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
    context={"db": db}
)

        return {
        "response": result["response"],
        "intent": result.get("intent"),
         "data": result.get("data", {})
         } 