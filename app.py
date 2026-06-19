"""
streamlit_app.py - UI Only
This file only contains UI code and calls your existing notebook logic
"""

import streamlit as st
import os
import sys
from datetime import datetime

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="COVID-19 QA Chatbot",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit defaults
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppHeader {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 12px 16px;
        border-radius: 15px 15px 0 15px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .assistant-message {
        background-color: #e9ecef;
        color: #212529;
        padding: 12px 16px;
        border-radius: 15px 15px 15px 0;
        max-width: 80%;
        margin-right: auto;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ============================================
# Initialize Session State
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome! I'm a COVID-19 QA assistant. Ask me anything about the WHO epidemiological updates or the ASU student survey on COVID-19 impacts."
        }
    ]

# ============================================
# Import your QA Logic from langchain.py
# ============================================

try:
    from langchain_code import get_answer
    LOGIC_LOADED = True
    print("✅ Successfully imported get_answer from langchain.py")  # DEBUG
except ImportError as e:
    LOGIC_LOADED = False
    st.error(f"""
    ⚠️ Could not import langchain.py. 
    
    Error: {e}
    
    Please make sure:
    1. langchain.py is in the same folder as this file
    2. langchain.py has a function called get_answer
    """)
    print(f"❌ Import error: {e}")  # DEBUG

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.title("🦠 COVID-19 Chatbot")
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Knowledge Base
    - WHO Epidemiological Update (2025)
    - ASU Student Survey (2020)
    - 2 Research Papers
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Tips
    - Ask specific questions
    - Use natural language
    - The bot only answers from the papers
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Chat cleared! Ask me anything about COVID-19."
            }
        ]
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📝 Example Questions")
    example_questions = [
        "What was the global SARS-CoV-2 test positivity rate in week 1 of 2025?",
        "How many new COVID-19 cases were reported globally?",
        "What percentage of students delayed graduation due to COVID-19?",
        "How many students completed the ASU survey?",
        "What is the current most prevalent SARS-CoV-2 variant?",
        "What percentage of students lost their job due to COVID-19?"
    ]
    
    for q in example_questions:
        if st.button(f"• {q[:40]}...", use_container_width=True, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# ============================================
# MAIN CHAT INTERFACE
# ============================================
st.title("🦠 COVID-19 Epidemiology QA Chatbot")
st.caption("Ask questions about COVID-19 epidemiology and student impacts from research papers")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end;">
                <div class="user-message">
                    {message["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start;">
                <div class="assistant-message">
                    {message["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# INPUT AREA
# ============================================
st.markdown("---")

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Type your question:",
        placeholder="e.g., What was the global SARS-CoV-2 test positivity rate?",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("Send", type="primary", use_container_width=True)

# ============================================
# PROCESS QUERY
# ============================================
if submit_button and user_input and LOGIC_LOADED:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🧠 Searching papers and generating answer..."):
        try:
            print(f"📝 Processing question: {user_input}")  # DEBUG
            result = get_answer(user_input)
            print(f"✅ Got result: {result[:100]}...")  # DEBUG
        except Exception as e:
            result = f"❌ Error: {str(e)}"
            print(f"❌ Error: {e}")  # DEBUG
            import traceback
            traceback.print_exc()  # DEBUG - prints full error
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": result})
    
    st.rerun()

# ============================================
# FOOTER
# ============================================
st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.8em; margin-top: 30px; padding: 20px 0;">
        🔬 Powered by LangChain, ChromaDB, and Groq Llama 3.1
    </div>
    """, unsafe_allow_html=True)