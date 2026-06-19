# 🦠 COVID-19 Epidemiology QA Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that answers questions about COVID-19 using research papers and WHO epidemiological reports. The application uses semantic search with ChromaDB, reranking with CrossEncoder, and Groq's Llama 3.1 model to generate precise answers based only on the retrieved context.

---

## 🚀 Features

- Semantic document retrieval using **ChromaDB**
- Embeddings generated with **all-mpnet-base-v2**
- Context reranking using **CrossEncoder**
- LLM-powered answer generation using **Groq Llama 3.1**
- Streamlit chat interface
- Source citation for responses
- Duplicate chunk removal
- Relevance score filtering
- Answer generation restricted to retrieved context

---

## 🏗 Architecture

```
User Query
     ↓
ChromaDB Vector Store
     ↓
Top 50 Similar Chunks
     ↓
Relevance Threshold Filtering
     ↓
CrossEncoder Reranking
     ↓
Top 5 Chunks
     ↓
Groq Llama 3.1
     ↓
Final Answer + Sources
```

---

## 📚 Knowledge Base

The chatbot can answer questions from:

- WHO Epidemiological Update (2025)
- ASU Student Survey on COVID-19 impacts (2020)
- COVID-19 research papers

Examples:

- What was the global SARS-CoV-2 test positivity rate in week 1 of 2025?
- How many students completed the ASU survey?
- What percentage of students delayed graduation due to COVID-19?
- Which SARS-CoV-2 variant was most prevalent?

---

## 🛠 Tech Stack

### Backend

- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers
- CrossEncoder
- Groq API

### Frontend

- Streamlit

### Models

#### Embedding Model

```
sentence-transformers/all-mpnet-base-v2
```

#### Reranker

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

#### LLM

```
llama-3.1-8b-instant
```

---

## 📂 Project Structure

```bash
.
├── app.py                  # Streamlit UI
├── langchain_code.py       # RAG pipeline and answer generation
├── vector_db/              # ChromaDB vector database
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/covid19-rag-chatbot.git

cd covid19-rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Groq API Key

In `langchain_code.py`:

```python
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"
```

Or use environment variables:

```bash
export GROQ_API_KEY=YOUR_API_KEY
```

Windows:

```bash
set GROQ_API_KEY=YOUR_API_KEY
```

---

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🔍 Retrieval Pipeline

### Step 1: Semantic Search

Retrieve top 50 chunks from ChromaDB:

```python
vector_store.similarity_search_with_relevance_scores(query, k=50)
```

### Step 2: Threshold Filtering

Keep only chunks with relevance score > 0.15.

### Step 3: Reranking

Rank documents using:

```python
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### Step 4: Deduplication

Remove repeated chunks.

### Step 5: Context Construction

Select top 5 chunks.

### Step 6: Answer Generation

Generate responses with:

```
llama-3.1-8b-instant
```

while ensuring answers are based only on retrieved context.

---

## 💡 Example Questions

- What was the global SARS-CoV-2 test positivity rate in week 1 of 2025?
- How many new COVID-19 cases were reported globally?
- What percentage of students lost their jobs due to COVID-19?
- How many students completed the ASU survey?
- Which variant was most prevalent?

---

## 📸 User Interface

The Streamlit interface includes:

- Interactive chat window
- Sidebar with example questions
- Clear chat functionality
- Source attribution
- Loading indicators

---

## 🔒 Hallucination Prevention

The chatbot follows strict rules:

- Answers only from retrieved context.
- No assumptions or guessing.
- Returns:

```
⚠️ Information not explicitly stated in the provided context.
```

if information is unavailable.

---

## Future Improvements

- PDF upload support
- Conversation memory
- Hybrid search (BM25 + Vector Search)
- Metadata filtering
- Citation highlighting
- Multi-document support
- Docker deployment

---

## Dependencies

```txt
langchain
langchain-chroma
langchain-huggingface
langchain-groq
sentence-transformers
chromadb
streamlit
torch
transformers
```
