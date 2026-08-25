from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import database
from src.schemas.chat import ChatRequest, ChatResponse
from src.graph.graph import ecommerce_graph

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(database.get_db)
):
        result = await ecommerce_graph.ainvoke({
        "user_query": request.message,
        "filters": {},
        "products": [],
        "response": "",
        "db": db
      })

        return {
        "response": result["response"]
         } 