import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Streamlit UI Setup
st.set_page_config(page_title="AI Web App", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(-10px);}
            to {opacity: 1; transform: translateY(0);}
        }
        .animated-text {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(45deg, #6a11cb, #2575fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 2s ease-in-out;
        }
        body { background-color: #121212; color: white; }
        .stTextArea textarea { font-size: 16px; background-color: #1e1e1e; color: white; }
        .stButton>button { background-color: #6a11cb; color: white; font-size: 18px; border-radius: 10px; }
        .stButton>button:hover { background-color: #2575fc; }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom Greeting
st.markdown('<h1 class="animated-text">Hello, Kushal! 👋</h1>', unsafe_allow_html=True)

# File Upload Feature
uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "pdf", "docx"])

# Chatbot Section
st.title("AI Assistant Chatbot")
st.write("Ask me anything and get AI-generated responses!")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role, content = msg["role"], msg["content"]
        if role == "user":
            st.markdown(f'<div style="text-align: right; color: #4a90e2;"><b>👤 You:</b> {content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: left; color: #6a11cb;"><b>🤖 AI:</b> {content}</div>', unsafe_allow_html=True)

# User Input
user_input = st.text_area("You:", "", key="user_input", height=100)
send_button = st.button("Send")

if send_button and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI Response
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(user_input)
    ai_response = response.text if hasattr(response, "text") else "Sorry, I couldn't process that."

    # Store AI Response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Refresh chat display
    st.rerun()
