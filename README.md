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

# 🛒 AI Ecommerce — Intelligent Shopping Assistant

An **AI-powered Ecommerce backend** built with **FastAPI, PostgreSQL, pgvector, Google Gemini, LangChain, and LangGraph**.

This project combines traditional ecommerce functionality with **AI-powered product search and conversational shopping**.

Instead of forcing users to interact with multiple APIs manually, users can simply type requests such as:

> "Show me a Dell laptop under ₹50,000"

> "Add 2 Dell Inspiron 15 to my cart"

> "Buy 1 HP laptop"

The AI understands the user's intent, finds the relevant product, adds it to the cart, or places the order through a **LangGraph-based workflow**.

---

## 🚀 What Makes This Project Different?

This is not just a traditional ecommerce API.

The application uses an **AI Agent workflow** to understand what the user wants and decide what action should happen next.

### Example

User:

```text
Add 2 Dell Inspiron 15 to my cart