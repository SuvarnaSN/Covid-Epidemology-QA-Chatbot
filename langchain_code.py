"""
langchain_code.py - Your exact working code from langchain.ipynb
NO CHANGES MADE - This is a direct copy
"""

import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from sentence_transformers import CrossEncoder
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# YOUR EXISTING CODE - PASTE HERE
# ============================================

# Load models (your existing code)
os.environ["GROQ_API_KEY"] = ""

vector_db_path = "D:\\AI Projects\\Chatbot-2\\vector_db"
collection_name = "document_collection"

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embedding,
    persist_directory=vector_db_path
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
)

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# ============================================
# YOUR get_answer FUNCTION (EXACT COPY)
# ============================================

def get_answer(query: str):
    """
    Your EXACT function from the notebook
    No changes made
    """
    
    k_retrieve = 50
    threshold = 0.15
    
    # Step 1: Retrieve chunks
    docs_with_scores = vector_store.similarity_search_with_relevance_scores(query, k=k_retrieve)
    
    # Step 2: Filter
    docs = [doc for doc, score in docs_with_scores if score > threshold]
    
    if not docs:
        return "⚠️ No relevant documents found. Please try rephrasing your question."
    
    # Step 3: Rerank
    pairs = [[query, d.page_content] for d in docs]
    rerank_scores = reranker.predict(pairs)
    
    # Step 4: Deduplicate and sort
    ranked_docs = sorted(zip(rerank_scores, docs), key=lambda x: x[0], reverse=True)
    
    seen_content = set()
    unique_docs = []
    for score, doc in ranked_docs:
        fingerprint = doc.page_content[:100]
        if fingerprint not in seen_content:
            seen_content.add(fingerprint)
            unique_docs.append((score, doc))
    
    top_docs = unique_docs[:5]
    
    # Step 5: Build context
    context_parts = []
    sources = []
    for i, (score, doc) in enumerate(top_docs, 1):
        source = doc.metadata.get('source', 'Unknown source')
        source_name = os.path.basename(source)
        if source_name not in sources:
            sources.append(source_name)
        
        chunk_text = f"[Chunk {i} - Source: {source_name}]\n{doc.page_content}"
        context_parts.append(chunk_text)
    
    context = "\n\n".join(context_parts)
    
    # Step 6: Prompt
    prompt = f"""
You are a precise data analyst answering questions using ONLY the context provided.

**RULES:**
1. **Answer using information explicitly stated in the context**
2. **If the exact answer is not in the context**, say:
   "⚠️ Information not explicitly stated in the provided context."
3. **Do NOT make assumptions or guesses**
4. **When you answer, mention which Chunk number(s) you used**

**Context:**
{context}

**Question:** {query}

**Answer (based ONLY on the context):**
"""
    
    # Step 7: Generate answer
    response = llm.invoke(prompt)
    
    # Step 8: Return answer with sources
    if sources:
        return f"{response.content}\n\n📄 **Sources:** {', '.join(sources)}"
    else:
        return response.content

# ============================================
# For testing (optional)
# ============================================
if __name__ == "__main__":
    test_query = "What was the global SARS-CoV-2 test positivity rate in week 1 of 2025?"
    print(f"Q: {test_query}")
    print(f"A: {get_answer(test_query)}")