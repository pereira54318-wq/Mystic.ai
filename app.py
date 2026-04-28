import streamlit as st
import os
import time
import io
import chromadb
from dotenv import load_dotenv
from PIL import Image
from xai_sdk import Client
from xai_sdk.chat import user, system, image as xai_image
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from faster_whisper import WhisperModel
from melo.api import TTS

# Configuração da página (deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="MYSTIC AI 2026", page_icon="🧙🏻‍♂️", layout="wide")

load_dotenv()

# ===================== CSS AVANÇADO - ULTRA CINZA & GLASSMORPISM =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');

    .stApp {
        background: radial-gradient(circle at top, #252525, #0f0f0f);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Título 3D com Animação Glow */
    .mystic-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2rem, 8vw, 5rem);
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to bottom, #ffffff, #666666);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.2));
        margin-bottom: 0;
        letter-spacing: -2px;
    }

    .mystic-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 0.9rem;
        color: #888;
        letter-spacing: 5px;
        margin-bottom: 40px;
    }

    /* Balões de Chat Customizados */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }

    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilização da Barra de Chat */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===================== TÍTULO =====================
st.markdown('<h1 class="mystic-title">MYSTIC AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="mystic-subtitle">PREMIUM GREY EDITION • 2026</p>', unsafe_allow_html=True)

# ===================== CACHE DE MODELOS =====================
@st.cache_resource
def init_models():
    whisper = WhisperModel("small", device="cpu", compute_type="int8")
    tts = TTS(language="PT", device="auto")
    embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    db_client = chromadb.PersistentClient(path="./mystic_memory")
    collection = db_client.get_or_create_collection(name="mystic_rag", embedding_function=embedding_function)
    return whisper, tts, collection

whisper_model, tts_model, rag_collection = init_models()

# Cliente X.AI com verificação de erro
api_key = os.getenv("XAI_API_KEY")
if not api_key:
    st.error("⚠️ API Key não encontrada. Configure o segredo 'XAI_API_KEY'.")
    st.stop()
client = Client(api_key=api_key)

# ===================== ESTADO DA SESSÃO =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===================== LOGICA RAG =====================
def add_to_rag(text: str, role: str):
    doc_id = f"{role.lower()}_{int(time.time() * 1000)}"
    rag_collection.add(documents=[f"{role}: {text}"], ids=[doc_id])

def get_context(query: str):
    results = rag_collection.query(query_texts=[query], n_results=3)
    return "\n".join(results.get('documents', [[]])[0])

# ===================== SIDEBAR MELHORADA =====================
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/wizard.png", width=80)
    st.title("Painel de Controle")
    st.divider()
    selected_lang = st.selectbox("Idioma Global", ["PT", "EN", "ES", "JP"], index=0)
    voice_on = st.toggle("Ativar Resposta por Voz", value=True)
    
    if st.button("Limpar Memória Local"):
        st.session_state.messages = []
        st.rerun()

# ===================== ÁREA DE CHAT =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "images" in msg:
            for img in msg["images"]:
                st.image(img, width=300)

# ===================== INPUTS =====================
# Container para uploads e áudio antes do chat input
with st.container():
    c1, c2 = st.columns([1, 1])
    with c1:
        uploaded_files = st.file_uploader("🖼️ Enviar Imagens", type=["png","jpg"], accept_multiple_files=True)
    with c2:
        audio_input = st.audio_input("🎤 Comando de Voz")

prompt = st.chat_input("O que você deseja manifestar?")

# Processamento de Áudio
if audio_input and not prompt:
    with st.status("🔮 Decifrando sua voz..."):
        with open("temp.wav", "wb") as f: f.write(audio_input.getvalue())
        segments, _ = whisper_model.transcribe("temp.wav")
        prompt = " ".join(s.text for s in segments)

# ===================== GERAÇÃO DE RESPOSTA =====================
if prompt:
    # Preparar imagens
    imgs_pil = [Image.open(f) for f in uploaded_files] if uploaded_files else []
    
    # Exibir prompt do usuário
    st.session_state.messages.append({"role": "user", "content": prompt, "images": imgs_pil})
    with st.chat_message("user"):
        st.markdown(prompt)
        for im in imgs_pil: st.image(im, width=300)

    # Resposta da IA
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            chat = client.chat.create(model="grok-4.20-reasoning")
            context = get_context(prompt)
            
            # Construção do prompt com contexto
            system_instruction = f"Você é a MYSTIC AI. Idioma: {selected_lang}. Contexto: {context}"
            chat.append(system(system_instruction))
            
            content_payload = [prompt]
            for img in imgs_pil:
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                content_payload.append(xai_image(buf.getvalue()))
            
            chat.append(user(*content_payload) if len(content_payload) > 1 else user(prompt))

            for chunk in chat.stream():
                if hasattr(chunk, 'content') and chunk.content:
                    full_response += chunk.content
                    response_placeholder.markdown(full_response + " ▌")
            
            response_placeholder.markdown(full_response)
            
            # Voz
            if voice_on:
                wav_path = "mystic_voice.wav"
                tts_model.tts_to_file(full_response[:500], speaker_id=0, speed=1.0, filename=wav_path)
                st.audio(wav_path, autoplay=True)

            # Salvar no RAG
            add_to_rag(prompt, "User")
            add_to_rag(full_response, "Mystic")
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Erro na conexão mística: {e}")
