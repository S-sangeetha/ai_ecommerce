from fastapi import FastAPI
from src.api.user import router as user_router
from src.api.product import router as product_router
from src.api.chat import router as chat_router
from src.api.cart import router as cart_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is Running"}

app.include_router(user_router)
app.include_router(product_router)
app.include_router(chat_router)
app.include_router(cart_router)
