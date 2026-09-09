# 🛒 AI Ecommerce Assistant

An **AI-powered Ecommerce backend** built with **FastAPI, PostgreSQL, pgvector, SQLAlchemy, LangChain, LangGraph, MCP, and Google Gemini**.

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
* AI tool/action execution
* MCP-based tool integration

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

## 🔌 MCP Features

The application also integrates **MCP (Model Context Protocol)** to provide a standardized interface for exposing backend capabilities as AI-accessible tools.

MCP allows the AI layer to interact with application functionality through well-defined tools instead of directly manipulating the database or business logic.

Example MCP capabilities can include:

```text
search_products
get_product
add_to_cart
update_cart
remove_from_cart
get_cart
create_order
```

The MCP layer acts as a controlled bridge between the AI system and ecommerce services.

---

# 🧠 AI Architecture

The application follows an **LLM + LangGraph + MCP + deterministic business logic** architecture.

```text
                         User Query
                             │
                             ▼
                    ┌─────────────────┐
                    │  Google Gemini  │
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
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     Product Search      Cart Action       Order Action
          │                  │                  │
          ▼                  ▼                  ▼
     MCP Tool             MCP Tool           MCP Tool
          │                  │                  │
          ▼                  ▼                  ▼
   Product Service       Cart Service       Order Service
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                       PostgreSQL
                       + pgvector
```

The LLM is responsible for **understanding the user's language**, while LangGraph controls the workflow and MCP provides a standardized mechanism for executing application tools.

Deterministic backend services remain responsible for critical business operations such as:

* Stock validation
* Price calculation
* Cart updates
* Order creation
* Inventory reduction
* Database transactions

This prevents the LLM from directly controlling critical ecommerce logic.

---

# 🔌 Model Context Protocol (MCP)

## What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol for connecting AI applications with external tools, services, and data sources.

In this project, MCP provides a structured interface through which the AI workflow can access ecommerce functionality.

Instead of allowing the LLM to directly interact with the database, the AI can invoke controlled tools exposed through the MCP layer.

```text
                    AI Assistant
                         │
                         ▼
                    LangGraph
                         │
                         ▼
                    MCP Client
                         │
                         ▼
                  ┌─────────────┐
                  │ MCP Server  │
                  └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     Product Tools   Cart Tools     Order Tools
          │              │              │
          ▼              ▼              ▼
     Product Service  Cart Service  Order Service
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    PostgreSQL
                    + pgvector
```

## Why MCP?

MCP provides a clean separation between:

```text
AI Reasoning
     │
     ▼
Tool Selection
     │
     ▼
MCP Interface
     │
     ▼
Business Logic
     │
     ▼
Database
```

This architecture makes it easier to:

* Expose backend functionality to AI agents
* Standardize AI-to-tool communication
* Reuse tools across different AI workflows
* Keep business logic outside the LLM
* Add new AI tools without tightly coupling them to prompts
* Control which operations the AI is allowed to execute
* Build more maintainable agentic applications

---

# 🧰 MCP Tools

The ecommerce functionality can be exposed as MCP tools.

### Product Tools

```text
search_products
get_product
```

Example:

```text
User:
Show me Dell laptops under ₹50,000

        ↓

Gemini understands request

        ↓

LangGraph routes request

        ↓

MCP: search_products

        ↓

Product Service

        ↓

PostgreSQL + pgvector

        ↓

Product Results
```

### Cart Tools

```text
add_to_cart
update_cart
remove_from_cart
get_cart
```

Example:

```text
User:

Add 2 Apple iPhone 15 to cart

        ↓

Intent: add_to_cart

        ↓

LangGraph

        ↓

MCP: add_to_cart

        ↓

Cart Service

        ↓

Stock / product validation

        ↓

PostgreSQL

        ↓

Cart Updated
```

### Order Tools

```text
create_order
```

Example:

```text
User:

Buy Apple iPhone 15

        ↓

Intent: buy_product

        ↓

LangGraph

        ↓

MCP: create_order

        ↓

Order Service

        ↓

Stock Validation

        ↓

Create Order

        ↓

Reduce Stock
```

The MCP tools should remain thin interfaces. The actual business rules continue to live inside the backend services.

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

When MCP is used as the tool interface:

```text
LangGraph
    │
    ▼
Intent / State
    │
    ▼
Select Tool
    │
    ▼
MCP Tool
    │
    ▼
Backend Service
    │
    ▼
Database
```

This separates workflow orchestration from business operations.

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

This makes the LLM output predictable and easier for the backend and MCP tools to process.

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

product_id
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

These operations can be exposed through MCP tools while the actual cart business logic remains inside the cart service.

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

The LLM does not determine stock availability.

The database/business layer performs the validation.

Even when the request is triggered through an MCP tool:

```text
AI
 ↓
MCP create_order
 ↓
Order Service
 ↓
Stock Validation
 ↓
Database Transaction
```

The business layer remains the source of truth.

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

Authentication and authorization remain backend responsibilities.

MCP tools should execute operations within the authenticated user's context rather than allowing the LLM to determine user identity or permissions.

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
* Async SQLAlchemy
* Alembic

## AI / LLM

* Google Gemini
* LangChain
* LangGraph
* Google Generative AI Embeddings

## AI Tool Integration

* Model Context Protocol (MCP)
* MCP Client
* MCP Server
* AI Tool Calling

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
│   │   ├── cart.py
│   │   └── order.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   │
│   ├── mcp/
│   │   ├── server.py
│   │   ├── tools/
│   │   │   ├── product_tools.py
│   │   │   ├── cart_tools.py
│   │   │   └── order_tools.py
│   │   └── client.py
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

> The exact MCP directory structure can be adjusted depending on whether the MCP server is implemented inside the FastAPI application or as a separate service.

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
        Select Search Tool
                │
                ▼
          MCP Tool
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
        + pgvector
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

The workflow can then execute:

```text
Previous Context
      │
      ▼
LangGraph
      │
      ▼
Resolve "first one"
      │
      ▼
MCP add_to_cart
      │
      ▼
Cart Service
      │
      ▼
PostgreSQL
```

---

# 🛡️ AI + Business Logic Separation

One of the key architectural principles of this project is that **the LLM does not directly control critical business operations**.

```text
                 LLM
                  │
          Understand language
                  │
                  ▼
              LangGraph
                  │
          Decide workflow/tool
                  │
                  ▼
                MCP
                  │
          Controlled tool call
                  │
                  ▼
          Backend Service
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      Stock     Cart      Order
     Rules      Rules      Rules
        │         │         │
        └─────────┼─────────┘
                  ▼
              Database
```

For example, the LLM can understand:

```text
"Buy 5 iPhones"
```

But it should not decide:

```text
stock = 5
```

The backend determines the actual stock.

Similarly, the LLM can request:

```text
create_order
```

but the order service determines:

* Whether the product exists
* Whether the user is authorized
* Whether enough stock exists
* The actual product price
* The order total
* Inventory reduction
* Database transaction success

This provides a safer and more reliable architecture for AI-powered ecommerce applications.

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
* Tool calling
* Model Context Protocol (MCP)
* MCP servers
* MCP tools
* AI-to-backend tool integration
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
* More advanced MCP tool calling
* MCP resource integration
* MCP prompt templates
* Recommendation system
* Personalized product recommendations
* Production deployment
* Monitoring and logging
* Rate limiting
* Tool-level authorization
* MCP tool validation
* Distributed MCP server architecture

---

# 📌 Project Goal

The goal of this project is to understand how **Generative AI, Agentic AI, LangGraph, and MCP can be integrated with a traditional backend system**.

Rather than replacing traditional backend logic with an LLM, the project uses:

```text
LLM
 │
 ├── Understand user language
 ├── Extract information
 └── Determine required action
          │
          ▼
      LangGraph
          │
          ├── Workflow orchestration
          ├── Conditional routing
          └── State management
          │
          ▼
         MCP
          │
          ├── Standardized tool interface
          └── Controlled AI-to-system communication
          │
          ▼
    Backend Services
          │
          ├── Business rules
          ├── Validation
          ├── Transactions
          └── Authorization
          │
          ▼
      PostgreSQL
       + pgvector
```

The LLM handles **language understanding and decision routing**, LangGraph handles **agent workflow orchestration**, MCP provides a **standardized tool interface**, and the backend remains responsible for **data integrity, business rules, inventory, cart management, and orders**.

This creates a practical architecture for building **reliable, tool-enabled, agentic AI applications**.
