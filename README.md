# 🛒 AI Ecommerce Assistant

An **AI-powered Ecommerce backend** built with **FastAPI, PostgreSQL, pgvector, SQLAlchemy, LangChain, LangGraph, and Google Gemini**.

The application combines traditional ecommerce functionality with **AI-powered conversational shopping**.

Instead of interacting with multiple APIs manually, users can communicate with the ecommerce system using natural language.

### Examples

```text
Show me laptops under ₹50,000

Add Apple iPhone 15 to my cart

Add 2 Apple iPhone 15 to cart

Buy Apple iPhone 15

Show me my cart

Update Apple iPhone 15 quantity to 3

Remove Apple iPhone 15 from my cart

Show me Dell laptops for programming
```

The AI understands the user's request, identifies the intent, extracts relevant information, searches the product database, and executes the appropriate ecommerce action.

---

# 🚀 Features

## 🤖 AI Features

* Natural language understanding
* LLM-based intent classification
* Structured LLM output using Pydantic
* Product information extraction
* Query understanding
* Google Gemini LLM integration
* Google Gemini embeddings
* Semantic product search
* Vector similarity search using pgvector
* Hybrid search using structured filters + vector similarity
* AI-powered grounded responses
* Conversation memory
* Context-aware requests
* Reference resolution such as:

  * "Add the first one to cart"
  * "What about Lenovo?"
* LangGraph-based AI workflow
* Conditional routing
* Stateful AI workflow

## 🛍️ Ecommerce Features

* User registration
* User authentication
* JWT authentication
* Password hashing
* Product creation
* Product management
* Product embeddings
* Product search
* Brand filtering
* Category filtering
* Minimum price filtering
* Maximum price filtering
* Add product to cart
* Update cart quantity
* Remove product from cart
* Get cart
* Stock validation
* Order creation
* Order quantity validation
* Automatic stock reduction after purchase

---

# 🧠 AI Architecture

The application follows an **LLM + deterministic business logic** architecture.

```text
                         User Query
                             │
                             ▼
                    ┌─────────────────┐
                    │   Google Gemini │
                    │  Query Analysis │
                    └────────┬────────┘
                             │
                             ▼
                    Structured Output
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
        Intent Detection              Information
                                      Extraction
              │                             │
              └──────────────┬──────────────┘
                             ▼
                        LangGraph
                             │
                    Conditional Routing
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 Product Search          Cart Action         Order Action
        │                    │                    │
        ▼                    ▼                    ▼
 Hybrid Search          Cart Service        Order Service
        │                    │                    │
        ▼                    ▼                    ▼
 PostgreSQL +          PostgreSQL +        PostgreSQL +
 pgvector              Business Logic      Business Logic
```

The LLM is responsible for **understanding the user's language**, while deterministic backend services handle important business operations such as:

* Stock validation
* Price calculation
* Cart updates
* Order creation
* Inventory reduction

This prevents the LLM from directly controlling critical ecommerce logic.

---

# 🔎 Hybrid Product Search

The project uses a combination of **structured filtering and semantic vector search**.

### Structured filtering

The system can filter products using:

```text
Brand
Category
Minimum Price
Maximum Price
```

For example:

```text
Show me Dell laptops under ₹50,000
```

The query can be converted into:

```text
brand = Dell
category = Laptop
max_price = 50000
```

### Semantic search

The user's product query is converted into an embedding.

```text
"I need a laptop suitable for programming"
                │
                ▼
         Embedding Model
                │
                ▼
          Vector Embedding
                │
                ▼
          pgvector Search
```

Products are ranked using **cosine similarity/distance**.

This allows the application to understand queries based on meaning rather than only exact keyword matches.

---

# 🧠 LangGraph Workflow

The conversational system is implemented using **LangGraph**.

```text
START
  │
  ▼
understand_query
  │
  ▼
route_by_intent
  │
  ├── product_search
  │       │
  │       ▼
  │   search_products
  │       │
  │       ├── products found
  │       │       │
  │       │       ▼
  │       │   limited_results
  │       │
  │       └── no products
  │               │
  │               ▼
  │            fallback
  │
  ├── add_to_cart
  │       │
  │       ▼
  │   find_product
  │       │
  │       ▼
  │   add_product_to_cart
  │
  ├── buy_product
  │       │
  │       ▼
  │   find_product
  │       │
  │       ▼
  │   create_order
  │
  ├── get_cart
  │
  ├── update_cart
  │
  ├── remove_from_cart
  │
  └── general
```

---

# 🔀 Intent Detection

The AI identifies different ecommerce intents.

```text
product_search
add_to_cart
buy_product
get_cart
update_cart
remove_from_cart
general
```

Example:

```text
"Show me laptops"
        ↓
product_search
```

```text
"Add iPhone 15 to cart"
        ↓
add_to_cart
```

```text
"Buy 2 iPhone 15"
        ↓
buy_product
```

```text
"Show my cart"
        ↓
get_cart
```

---

# 📦 Structured LLM Output

The LLM output is converted into a structured Pydantic model.

```python
class EcommerceRequest(BaseModel):

    intent: Literal[
        "product_search",
        "add_to_cart",
        "buy_product",
        "general"
    ]

    product_query: str | None = None
    quantity: int = 1

    brand: str | None = None
    category: str | None = None
    max_price: float | None = None
```

For example:

```text
"Add 2 Apple iPhone 15 to my cart"
```

can be interpreted as:

```json
{
    "intent": "add_to_cart",
    "product_query": "Apple iPhone 15",
    "quantity": 2,
    "brand": "Apple"
}
```

This makes the LLM output predictable and easier for the backend to process.

---

# 💬 Conversation Memory

The application supports conversation-based interactions using LangGraph persistence/checkpointing.

For example:

### First request

```text
Show me laptops under ₹50,000
```

The system returns:

```text
1. Lenovo IdeaPad Slim 3
2. Dell Inspiron 15
```

### Follow-up request

```text
Add the first one to cart
```

The system can resolve:

```text
"the first one"
        ↓
previous search results
        ↓
Lenovo IdeaPad Slim 3
        ↓
product_id = 38
```

This allows the user to interact with the application conversationally instead of repeating the complete product name.

---

# 🛒 Cart Operations

The AI assistant supports:

### Add to cart

```text
Add Apple iPhone 15 to cart
```

### Add quantity

```text
Add 2 Apple iPhone 15 to cart
```

### Update quantity

```text
Update Apple iPhone 15 quantity to 3
```

### Remove product

```text
Remove Apple iPhone 15 from my cart
```

### View cart

```text
Show me my cart
```

---

# 📦 Order Processing

The application validates stock before creating an order.

```text
User requests:
Buy 5 Apple iPhone 15
        │
        ▼
Check product
        │
        ▼
Check stock
        │
        ├── Enough stock
        │       ↓
        │   Create order
        │       ↓
        │   Reduce stock
        │
        └── Insufficient stock
                ↓
          Return error
```

Example:

```text
Only 4 item(s) are available
```

The LLM does not determine stock availability. The database/business layer performs the validation.

---

# 🗄️ Database

The application uses:

* PostgreSQL
* pgvector
* SQLAlchemy
* Async SQLAlchemy
* Alembic

Product embeddings are stored in PostgreSQL using the `pgvector` extension.

Conceptually:

```text
products
   │
   ├── id
   ├── name
   ├── description
   ├── brand
   ├── category
   ├── price
   ├── stock
   └── embedding
```

---

# 🔐 Authentication

The application supports:

* User registration
* Login
* JWT authentication
* Password hashing
* User-specific cart data
* User-specific orders

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn

## Database

* PostgreSQL
* pgvector
* SQLAlchemy
* Alembic

## AI / LLM

* Google Gemini
* LangChain
* LangGraph
* Google Generative AI Embeddings

## Authentication

* JWT
* Password Hashing

## Development

* Git
* Postman
* Docker

---

# 📁 Project Structure

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
```

---

# 🔄 Example End-to-End Flow

```text
User:
"Show me Dell laptops under ₹50,000"
                │
                ▼
        Google Gemini
                │
                ▼
        Structured Request
                │
                ▼
        Intent: product_search
                │
                ▼
           LangGraph
                │
                ▼
       Product Search Service
                │
        ┌───────┴────────┐
        ▼                ▼
   SQL Filters      Vector Search
        │                │
        └───────┬────────┘
                ▼
          PostgreSQL
                │
                ▼
          Product Results
                │
                ▼
          AI Response
```

Then the user can continue:

```text
"Add the first one to cart"
```

The conversation state is used to identify the previously selected product.

---

# 🎯 Key AI Concepts Demonstrated

This project demonstrates practical experience with:

* Large Language Models (LLMs)
* Prompt engineering
* Structured LLM output
* Intent classification
* Information extraction
* Embeddings
* Vector databases
* Semantic search
* Cosine similarity
* Hybrid search
* Retrieval-augmented / grounded generation concepts
* LangChain
* LangGraph
* Conditional routing
* Stateful workflows
* Conversation memory
* Contextual reference resolution
* AI agent orchestration
* Tool/action execution
* AI guardrails
* LLM + deterministic business logic
* AI application error handling
* LLM cost and latency considerations

---

# 🚀 Future Improvements

Possible future improvements include:

* LangSmith tracing and observability
* LLM evaluation
* Search result reranking
* Improved spelling-error handling
* Query rewriting
* Search result caching
* Streaming AI responses
* Human-in-the-loop workflows
* More advanced tool calling
* Recommendation system
* Personalized product recommendations
* Production deployment
* Monitoring and logging

---

# 📌 Project Goal

The goal of this project is to understand how **Generative AI and Agentic AI can be integrated with a traditional backend system**.

Rather than replacing traditional backend logic with an LLM, the project uses the LLM for **language understanding and decision routing**, while the backend remains responsible for **data integrity, business rules, inventory, cart management, and orders**.

This creates a practical architecture for building reliable AI-powered applications.
