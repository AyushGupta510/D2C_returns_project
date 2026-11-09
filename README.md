# 📊 D2C Returns Intelligence Platform

**An AI-powered business intelligence and investigation platform for understanding e-commerce product returns using PostgreSQL analytics, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs).**

> Turning e-commerce return data and business documents into actionable, evidence-backed business insights.

---

## 🚀 Overview

Product returns are a major operational and financial challenge for Direct-to-Consumer (D2C) and e-commerce businesses.

High return rates can affect revenue, inventory management, logistics costs, customer experience, and overall business performance. However, businesses often have their order data, return policies, and operational documents scattered across different systems.

Understanding why returns are increasing requires more than simply looking at dashboards or asking questions to a generic chatbot.

**D2C Returns Intelligence** aims to address this problem by combining structured business analytics with document-based knowledge retrieval and Generative AI.

The platform allows users to ask business-related questions in natural language and receive investigation reports supported by actual database results and relevant policy evidence.

It is designed as a business investigation and decision-support system rather than a conventional chatbot.

## 🎯 Problem Statement

D2C and e-commerce businesses face several challenges when analyzing product returns:

- **Fragmented business information:** Order data, return policies, and operational documents are stored separately.
- **Limited analytical accessibility:** Business teams often need SQL knowledge or technical assistance to investigate return patterns.
- **Difficulty identifying patterns:** Understanding return rates across product categories, shipping methods, and other business dimensions can require multiple queries.
- **Disconnected information sources:** Traditional dashboards generally show numerical metrics but do not directly connect them with relevant policy documents.
- **Time-consuming investigations:** Analysts must manually retrieve data, examine documents, interpret findings, and prepare reports.

The platform aims to bring these investigation activities into one unified workflow.

## 💡 Proposed Solution

D2C Returns Intelligence combines three major capabilities:

### 1. Business Analytics

Uses PostgreSQL to retrieve and analyze structured order data.

Examples:
- Calculate overall return rates.
- Compare return rates across product categories.
- Analyze returns across shipping methods.
- Retrieve total orders and returned orders.
- Identify business segments that require further investigation.

### 2. Retrieval-Augmented Generation (RAG)

Uses a document retrieval pipeline to retrieve relevant information from business documents such as return policies and operational guidelines.

The current implementation includes:
- Document loading.
- Text splitting and chunking.
- Hugging Face embeddings.
- FAISS vector indexing.
- Similarity-based document retrieval.
- Evidence-grounded question answering.

### 3. GenAI-Powered Investigation

Uses a Large Language Model to combine analytical results and retrieved policy evidence.

The system aims to generate reports that distinguish:
- Measured business findings.
- Relevant policy information.
- What the available data establishes.
- Possible explanations that require further investigation.
- Recommended next investigative steps.

**Important:** Recommendations and possible explanations are not treated as proven causes unless supporting evidence establishes them.

---

## 🏗️ Current System Architecture

The current application follows this workflow:

```text
                 USER
                   |
                   v
          Streamlit Interface
                   |
                   v
       Business Investigation
                   |
          Natural Language
              Question
                   |
                   v
          Groq LLM (Router)
                   |
                   v
        Approved Query Selection
                   |
                   v
          Analytics Module
                   |
                   v
        Supabase PostgreSQL
                   |
                   v
         Business Analytics
                   |
                   |
                   v
          RAG Knowledge Base
                   |
             Policy Document
                   |
                   v
          Document Loading
                   |
                   v
            Text Chunking
                   |
                   v
          Hugging Face Embeddings
                   |
                   v
             FAISS Index
                   |
                   v
          Relevant Policy Evidence
                   |
                   v
          Groq LLM (Analysis)
                   |
                   v
        Investigation Report
                   |
                   v
          Streamlit Interface
```

### Investigation Workflow

1. A user enters a business question through the Streamlit interface.
2. The investigation module uses Groq to select an approved analytics query.
3. The analytics module executes the corresponding predefined SQL query against Supabase PostgreSQL.
4. The RAG module retrieves relevant passages from the return-policy document.
5. Groq combines the numerical analytics and retrieved evidence.
6. The system generates an investigation report.
7. Streamlit displays the report along with supporting analytics and policy evidence.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / UI | Streamlit |
| Database | PostgreSQL |
| Database Hosting | Supabase |
| Database Connectivity | SQLAlchemy, Psycopg |
| Data Processing | Pandas |
| LLM Provider | Groq |
| LLM Model | `openai/gpt-oss-120b` |
| LLM Framework | LangChain |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Embedding Integration | LangChain Hugging Face |
| Vector Database / Index | FAISS (CPU) |
| Document Processing | LangChain Community, TextLoader |
| Text Splitting | RecursiveCharacterTextSplitter |
| Environment Management | Python virtual environment, python-dotenv |
| Configuration | Environment variables (`.env`) |

### Technology Details

**Python:** Core programming language used to develop the application and implement business logic.

**Streamlit:** Provides the interactive web interface for entering business questions and viewing investigation reports.

**Supabase PostgreSQL:** Stores structured order information and serves as the source of business analytics.

**SQLAlchemy:** Provides database connectivity and execution of predefined SQL queries.

**Pandas:** Handles structured analytical results and data presentation.

**LangChain:** Integrates language models, document loaders, embeddings, text splitters, and vector retrieval.

**Groq:** Provides hosted LLM inference for query selection and investigation report generation.

**Hugging Face:** Provides the `all-MiniLM-L6-v2` embedding model for converting document chunks into vector representations.

**FAISS:** Creates and searches a local vector index to retrieve relevant policy passages.

---

## 📂 Project Structure

Current project organization:

```text
d2C_returns_project/
│
├── .env
├── .gitignore
│
├── phase_1/
│   │
│   ├── data set/
│   │   └── train.csv
│   │
│   ├── documents/
│   │   └── return_policy.txt
│   │
│   └── source/
│       ├── app.py
│       ├── analytics.py
│       ├── investigation.py
│       ├── rag.py
│       ├── database.py
│       ├── config.py
│       └── exploration.ipynb
│
└── README.md
```

*The README and project tree should be updated if the directory structure changes.*

### Module Responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Streamlit user interface |
| `analytics.py` | Predefined SQL analytics queries |
| `investigation.py` | Combines analytics, RAG, and LLM-generated reports |
| `rag.py` | Policy document loading, embeddings, FAISS retrieval, and question answering |
| `database.py` | Supabase PostgreSQL connection |
| `config.py` | Application configuration and API credentials |
| `exploration.ipynb` | Data exploration and initial workflow prototyping |
| `return_policy.txt` | Sample business return-policy knowledge source |

---

## 📊 Dataset

The initial development uses an e-commerce order dataset containing:

- **200,000 order records**
- **16 columns**

The dataset includes information such as:

- Order ID
- Customer age
- Product price
- Discount percentage
- Product rating
- Past purchase count
- Past return rate
- Delivery delay
- Session length
- Product views
- Device type
- Product category
- Shipping method
- Payment method
- Coupon usage
- Return status

The dataset is used to develop and test the business analytics functionality.

The order records have been migrated from local PostgreSQL to Supabase PostgreSQL.

The project also includes a sample return-policy document used for initial RAG development. It is a development knowledge source, not a verified policy for a real e-commerce company.

---

## ⚙️ Getting Started

### Prerequisites

Before running the application, install:

- Python 3.10 or newer (use a compatible version for the installed dependencies).
- Git
- VS Code or another Python IDE.
- A Supabase PostgreSQL project.
- A Groq API key.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

cd YOUR_REPOSITORY
```

Replace the repository URL with your actual GitHub repository.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the packages used by the current application:

```bash
pip install streamlit pandas sqlalchemy "psycopg[binary]" python-dotenv langchain langchain-groq langchain-community langchain-huggingface langchain-text-splitters sentence-transformers faiss-cpu
```

For reproducible installation, use a project-maintained `requirements.txt` when available.

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=your_supabase_postgresql_connection_url
GROQ_API_KEY=your_groq_api_key
```

Never commit `.env` or expose database credentials and API keys publicly.

The application uses the Supabase PostgreSQL connection through SQLAlchemy and Psycopg.

### 5. Run the Application

Navigate to the source directory:

```bash
cd phase_1/source
```

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Current Implemented Features

The current development version includes:

- [x] Initial dataset exploration.
- [x] PostgreSQL database setup.
- [x] Migration of order data to Supabase PostgreSQL.
- [x] Shared SQLAlchemy database connection.
- [x] Overall return analytics.
- [x] Product-category return analytics.
- [x] Shipping-method return analytics.
- [x] Predefined SQL query allowlist.
- [x] Groq LLM integration.
- [x] Return-policy document loading.
- [x] Text splitting and chunking.
- [x] Hugging Face embedding integration.
- [x] FAISS vector retrieval.
- [x] Policy question answering.
- [x] Combined analytics and RAG investigation workflow.
- [x] Streamlit application interface.
- [x] Display of investigation reports.
- [x] Expandable supporting analytics and policy evidence.

---

## 🔮 Future Development Roadmap

The project is being developed incrementally toward a more robust, enterprise-oriented architecture.

### Phase 2 — Data and Analytics Engineering
- Stronger data validation and quality checks.
- Reusable KPI calculation pipelines.
- More analytical dimensions and time-based comparisons.
- Query optimization and database indexing.
- Improved reporting and dashboard data preparation.

### Phase 3 — Advanced RAG Architecture
- PDF processing and document ingestion.
- Markdown conversion and document preprocessing.
- Metadata extraction.
- Improved semantic chunking strategies.
- Retrieval evaluation and hybrid search.
- Persistent vector indexing.
- Azure AI Search integration.

### Phase 4 — Advanced GenAI
- Structured information extraction.
- Pydantic-based response validation.
- More robust tool selection and orchestration.
- Improved evidence attribution and hallucination controls.
- Azure OpenAI integration.
- Investigation history and multi-step workflows.

### Phase 5 — Backend Development
- FastAPI backend.
- REST API design and integration.
- Request and response validation.
- Authentication and authorization.
- Structured logging and error handling.

### Phase 6 — Frontend Development
- React and TypeScript.
- Business intelligence dashboard.
- Interactive KPI visualization.
- Investigation history.
- Evidence and citation presentation.

### Phase 7 — Testing and Reliability
- Unit testing.
- Integration testing.
- End-to-end testing.
- RAG evaluation.
- Performance and latency testing.
- Security and access-control validation.

### Phase 8 — Deployment and Infrastructure
- Docker containerization.
- Azure Container Registry (ACR).
- Azure Kubernetes Service (AKS).
- Application deployment.
- CI/CD automation.
- Production monitoring and operational improvements.

*These are planned improvements, not currently implemented features.*

---

## 🔐 Security Considerations

The project uses environment variables for sensitive credentials.

Current and planned security improvements include:

- Excluding `.env` from Git.
- Never exposing API keys or database passwords in source code.
- Using restricted database permissions for application access.
- Validating user input and restricting database operations to approved queries.
- Applying authentication and authorization before multi-user deployment.
- Managing secrets securely during cloud deployment.
- Monitoring application errors and suspicious access.

---

## 🎯 Project Objective

The long-term objective is to develop a business intelligence and investigation platform that bridges the gap between structured business data and unstructured operational knowledge.

Rather than providing isolated SQL results or generic AI-generated answers, the system aims to deliver contextual business investigations supported by measurable data and relevant documents.

It is being developed with an emphasis on:

- GenAI application engineering.
- Retrieval-Augmented Generation.
- Database-driven business intelligence.
- LLM orchestration and structured outputs.
- Backend and frontend engineering.
- Cloud infrastructure and deployment.
- Software testing, security, and reliability.

---

## 📌 Development Status

**Current stage:** Initial working application and deployment preparation.

The current prototype successfully connects Supabase PostgreSQL, Groq, Hugging Face embeddings, FAISS, LangChain, and Streamlit.

The next milestone is to deploy the existing application and validate its behavior in a hosted environment.

Enterprise architecture improvements, advanced retrieval, testing, security hardening, and Azure deployment remain part of the future roadmap.

---

## 👨‍💻 Author

**Ayush Gupta**

B.Tech Computer Science and Engineering

Interested in Generative AI, RAG Systems, AI Application Engineering, and Agentic AI.

---

*Built incrementally to explore how Generative AI can transform business data and organizational knowledge into actionable intelligence.*
