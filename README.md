# AI Ecommerce Assistant

An AI-powered ecommerce backend built with **FastAPI, PostgreSQL, pgvector, SQLAlchemy, LangGraph, and Google Gemini**.

The application allows users to search for products using natural language, add products to their cart, and place orders through an AI-powered conversational interface.

---

## 🚀 Features

- User registration and authentication
- Product management
- Product creation with AI-generated embeddings
- Semantic product search using pgvector
- Natural language product search
- Product filtering
- AI-powered intent detection
- LangGraph-based conversational workflow
- Add products to cart using natural language
- Purchase products using natural language
- Order creation
- Stock availability validation
- PostgreSQL database
- Async SQLAlchemy
- FastAPI REST APIs
- Google Gemini LLM
- Google Gemini embeddings

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Database
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic

### AI / LLM
- Google Gemini
- LangChain
- LangGraph
- Google Generative AI Embeddings

### Authentication
- JWT
- Password hashing

---

## 📁 Project Structure

```text
ai_ecommerce/
│
├── src/
│   │
│   ├── api/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── chat.py
│   │
│   ├── config/
│   │   └── llm_config.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── product.py
│   │   └── chat.py
│   │
│   ├── services/
│   │   ├── user.py
│   │   ├── product.py
│   │   └── cart.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   │
│   └── main.py
│
├── alembic/
│
├── .env
├── .gitignore
├── requirements.txt
├── alembic.ini
└── README.md

