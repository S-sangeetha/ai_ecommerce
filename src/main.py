from fastapi import FastAPI
from src.api.user import router as user_router
from src.api.product import router as product_router
from src.api.chat import router as chat_router
from src.api.cart import router as cart_router
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from contextlib import asynccontextmanager
from src.graph.graph import create_graph

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with AsyncSqliteSaver.from_conn_string(
        "ecommerce_memory.db"
    ) as checkpointer:

        app.state.ecommerce_graph = (
            create_graph(checkpointer)
        )

        yield
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "API is Running"}


app.include_router(user_router)
app.include_router(product_router)
app.include_router(chat_router)
app.include_router(cart_router)
