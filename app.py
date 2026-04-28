import streamlit as st
import os
import time
import io
from dotenv import load_dotenv
from PIL import Image

from xai_sdk import Client
from xai_sdk.chat import user, system, image as xai_image

load_dotenv()

# ===================== CSS - TÍTULO 3D CINZA =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');

    .stApp {
        background: linear-gradient(135deg, #1a1a1a, #0f0f0f, #1f1f1f);
        color: #cccccc;
    }

    .mystic-title {
        font-family: 'Orbitron', 'Impact', sans-serif;
        font-size: 5.2rem;
        font-weight: 900;
        text-align: center;
        margin: 10px 0 5px 0;
        padding: 20px 0;
        color: #e0e0e0;
        text-shadow:
            -6px -6px 0 #555555,
            6px -6px 0 #555555,
            -6px 6px 0 #555555,
            6px 6px 0 #555555,
            0 0 30px #888888,
            0 0 50px #555555;
        letter-spacing: -3px;
        line-height: 1.0;
        border: 8px solid #777777;
        border-radius: 15px;
        background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
        box-shadow: 0 0 40px rgba(119, 119, 119, 0.7);
    }

    .mystic-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 1.4rem;
        color: #999999;
        margin-bottom: 25px;
        letter-spacing: 6px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Título 3D
st.markdown('<h1 class="mystic-title">MYSTIC AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="mystic-subtitle">2026 • GROK POWERED • CINZA EDITION</p>', unsafe_allow_html=True)

st.caption("🌌 Versão Leve para Streamlit Cloud")

# ===================== CONFIGURAÇÃO =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

client = Client(api_key=os.getenv("XAI_API_KEY"))

def mystic_response(prompt: str, images: list = None):
    chat = client.chat.create(model="grok-4.20-reasoning")
    
    content = [prompt]
    for img in images or []:
        byte_arr = io.BytesIO()
        img.save(byte_arr, format=img.format or "PNG")
        content.append(xai_image(byte_arr.getvalue()))

    chat.append(user(*content) if len(content) > 1 else user(content[0]))

    full_response = ""
    placeholder = st.empty()
    for chunk in chat.stream():
        if hasattr(chunk, 'content') and chunk.content:
            full_response += chunk.content
            placeholder.markdown(full_response + " ▌")
    placeholder.markdown(full_response)
    return full_response

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("⚙️ MYSTIC AI 2026")
    st.info("Modelo: Grok 4.20 (xAI)\nTema: Cinza Total")

# ===================== HISTÓRICO =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        for img in msg.get("images", []):
            st.image(img, width=450)

# ===================== INPUT =====================
prompt = st.chat_input("Fale com MYSTIC AI...")

col1, col2 = st.columns([5, 1])
with col2:
    uploaded_files = st.file_uploader("📸 Imagens", type=["png","jpg","jpeg"], accept_multiple_files=True, label_visibility="collapsed")

images = [Image.open(f) for f in uploaded_files] if uploaded_files else []

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        for img in images:
            st.image(img, width=400)

    with st.chat_message("assistant"):
        with st.spinner("🌌 MYSTIC AI está pensando..."):
            response = mystic_response(prompt, images)

    st.session_state.messages.append({"role": "user", "content": prompt, "images": images})
    st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("MYSTIC AI 2026 • Tema Cinza • Grok 4.20")
