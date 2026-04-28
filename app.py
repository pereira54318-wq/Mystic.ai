import streamlit as st
import os
import time
import io
from dotenv import load_dotenv
from PIL import Image

from xai_sdk import Client
from xai_sdk.chat import user, system, image as xai_image

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from faster_whisper import WhisperModel
from melo.api import TTS

load_dotenv()

# ===================== CSS - TEMA CINZA + TÍTULO 3D =====================
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
        box-shadow: 
            0 0 40px rgba(119, 119, 119, 0.7),
            inset 0 0 30px rgba(200, 200, 200, 0.15);
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

    .chat-message-user {
        background: #2a2a2a;
        border-radius: 15px;
        padding: 14px;
        border: 2px solid #666666;
        margin: 10px 0;
    }
    .chat-message-assistant {
        background: #1f1f1f;
        border-left: 6px solid #888888;
        padding: 14px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===================== TÍTULO 3D =====================
st.markdown('<h1 class="mystic-title">MYSTIC AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="mystic-subtitle">2026 • GROK POWERED • CINZA EDITION</p>', unsafe_allow_html=True)

st.caption("🌌 Entidade Mística com Visão • Voz • Memória Semântica")

# ===================== INICIALIZAÇÃO =====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_collection" not in st.session_state:
    embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    db_client = chromadb.PersistentClient(path="./mystic_memory")
    st.session_state.rag_collection = db_client.get_or_create_collection(
        name="mystic_rag", embedding_function=embedding_function
    )

@st.cache_resource
def load_whisper():
    return WhisperModel("small", device="cpu", compute_type="int8")

@st.cache_resource
def load_tts():
    return TTS(language="PT", device="auto")

whisper_model = load_whisper()
tts_model = load_tts()
client = Client(api_key=os.getenv("XAI_API_KEY"))

# ===================== FUNÇÕES =====================
def add_to_rag(text: str, role: str):
    doc_id = f"msg_{int(time.time() * 1000)}"
    st.session_state.rag_collection.add(documents=[f"{role}: {text}"], ids=[doc_id])

def retrieve_relevant_context(query: str, top_k=5):
    results = st.session_state.rag_collection.query(query_texts=[query], n_results=top_k)
    return "\n".join(results.get('documents', [[]])[0]) if results.get('documents') else ""

def mystic_response(prompt: str, images: list = None):
    chat = client.chat.create(model="grok-4.20-reasoning")
    context = retrieve_relevant_context(prompt)
    if context:
        chat.append(system(f"Contexto relevante anterior:\n{context}"))

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

def speak_with_melotts(text: str, language: str = "PT", reference_file=None):
    try:
        tts = TTS(language=language.upper()[:2], device="auto")
        speaker_id = 0
        if reference_file:
            st.info("🗣️ Usando referência de voz para cloning aproximado...")

        wav_path = "temp_mystic_voice.wav"
        tts.tts_to_file(text[:650], speaker_id=speaker_id, speed=1.0, filename=wav_path)
        
        with open(wav_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/wav", autoplay=True)
        return audio_bytes
    except Exception as e:
        st.error(f"Erro no TTS: {e}")
        return None

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("⚙️ Configurações MYSTIC 2026")
    selected_lang = st.selectbox("Idioma", ["PT", "EN", "ES", "FR", "ZH"], index=0)
    voice_enabled = st.toggle("🔊 Ativar Voz (MeloTTS)", value=True)
    cloning_enabled = st.toggle("🗣️ Voice Cloning (referência)", value=False)
    
    reference_file = None
    if cloning_enabled:
        reference_file = st.file_uploader("Upload referência de voz (10-30s)", type=["wav", "mp3"])

# ===================== HISTÓRICO =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        for img in msg.get("images", []):
            st.image(img, width=450)

# ===================== INPUTS =====================
prompt = st.chat_input("Escreva ou fale com MYSTIC AI...")

col1, col2, col3 = st.columns([4, 1.2, 1])
with col2:
    uploaded_files = st.file_uploader("📸 Imagens (múltiplas)", type=["png","jpg","jpeg"], accept_multiple_files=True, label_visibility="collapsed")
with col3:
    audio_input = st.audio_input("🎤 Falar agora")

images = [Image.open(f) for f in uploaded_files] if uploaded_files else []

# Processa áudio (STT)
if audio_input:
    with st.spinner("🎤 Transcrevendo..."):
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_input.getvalue())
        segments, _ = whisper_model.transcribe("temp_audio.wav", beam_size=5, language=None)
        transcribed = " ".join(seg.text for seg in segments)
        prompt = (prompt or "") + " " + transcribed
        st.success(f"Transcrito: {transcribed[:100]}...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        for img in images:
            st.image(img, width=400)

    with st.chat_message("assistant"):
        with st.spinner("🌌 MYSTIC AI consulta os cosmos..."):
            response = mystic_response(prompt, images)

        if voice_enabled:
            with st.spinner("🔊 Gerando voz..."):
                speak_with_melotts(response, language=selected_lang, reference_file=reference_file)

    add_to_rag(prompt, "Usuário")
    add_to_rag(response, "MYSTIC AI")

    st.session_state.messages.append({"role": "user", "content": prompt, "images": images})
    st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("MYSTIC AI 2026 • Tema Cinza Total • Grok 4.20 + RAG + MeloTTS")
