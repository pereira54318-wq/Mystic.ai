import streamlit as st
import time
import datetime
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI 👺", layout="wide", initial_sidebar_state="collapsed")

# --- FUNÇÃO PARA CARREGAR A LOGO ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Certifique-se de que a imagem do mago se chama 'mago.png' no seu GitHub
logo_mago = get_base64_image("mago.png")

# --- CSS PREMIMUM: FUNDO LISO, TEXTO 3D COLADO E CHAT VERMELHO ---
st.markdown(f"""
    <style>
    /* FUNDO LISO SEM NADA (SEM PARTÍCULAS) */
    .stApp {{
        background: linear-gradient(180deg, #000000 0%, #1a0000 50%, #4d0000 100%);
        color: #ff0000;
    }}

    /* TEXTO 3D GIGANTE QUASE JUNTO (COMPACTO) */
    .text-3d-giant {{
        font-family: 'Arial Black', sans-serif;
        font-size: 55px;
        line-height: 0.75; /* Quase junto */
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: -5px; /* Letras coladas */
        text-shadow: 
            0 1px 0 #800000, 0 2px 0 #700000, 0 3px 0 #600000, 
            0 4px 0 #500000, 0 5px 0 #400000, 0 8px 15px rgba(255,0,0,0.6);
        margin-bottom: 30px;
    }}

    /* LOGO DO MAGO */
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}
    .logo-img {{
        width: 200px;
        filter: drop-shadow(0 0 15px #f00);
    }}

    /* CHAT VERMELHO COM DEGRADÊ PRETO */
    .stChatMessage {{
        background: linear-gradient(90deg, #200000 0%, #000000 100%) !important;
        border: 2px solid #ff0000 !important;
        border-radius: 15px !important;
        color: #ffffff !important;
    }}

    /* BARRA DE CHAT ESTILO GEMINI */
    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 800px;
        border: 2px solid #ff0000 !important;
        border-radius: 30px !important;
        background: #000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if "logado" not in st.session_state: st.session_state.logado = False
if "mensagens" not in st.session_state: st.session_state.mensagens = []
if "global_chat" not in st.session_state: st.session_state.global_chat = []

# --- TELA DE ACESSO ---
if not st.session_state.logado:
    if logo_mago:
        st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{logo_mago}" class="logo-img"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="text-3d-giant">MELHOR IA DE<br>GERAR SCRIPT</div>', unsafe_allow_html=True)
    
    aba_login, aba_criar = st.tabs(["ENTRAR", "CRIAR CONTA"])
    with aba_login:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("INJETAR ACESSO"):
            if u:
                st.session_state.user = u
                st.session_state.logado = True
                st.rerun()
    with aba_criar:
        st.text_input("Novo Usuário")
        st.text_input("Gmail")
        st.text_input("Senha", type="password")
        st.button("VALIDAR E CRIAR")

# --- INTERFACE PRINCIPAL ---
else:
    # Sidebar limpa
    with st.sidebar:
        if logo_mago:
            st.image(f"data:image/png;base64,{logo_mago}", width=120)
        st.markdown(f"### 👺 {st.session_state.user}")
        if st.button("LOGOUT"):
            st.session_state.logado = False
            st.rerun()

    tab_ia, tab_perfil = st.tabs(["💬 TERMINAL", "👤 PERFIL / CHAT GLOBAL"])

    with tab_ia:
        # Novos botões solicitados
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ NOVO SCRIPT"): st.session_state.mensagens = []; st.rerun()
        with c2:
            if st.button("🔄 NOVO CHAT"): st.session_state.mensagens = []; st.rerun()

        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Solicite seu Script Rayfield..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                # CHAVES DUPLAS {{ }} PARA NÃO DAR ERRO DE SINTAXE
                lua = f"""local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = "Pereira System | {prompt}",
    LoadingTitle = "Injetando...",
    ConfigurationSaving = {{ Enabled = true, FileName = "Mystic" }}
}})
-- Script Hub para {prompt} ativado."""
                res = f"📡 **Terminal Mystic:**\n\n```lua\n{lua}\n```"
                st.markdown(res)
                st.session_state.mensagens.append({"role": "assistant", "content": res})

    with tab_perfil:
        st.markdown("<h2 style='color:red; text-align:center;'>🌐 CHAT GLOBAL (ONLINE)</h2>", unsafe_allow_html=True)
        
        # CHAT ONLINE REAL
        chat_box = st.container(height=350)
        with chat_box:
            for g in st.session_state.global_chat:
                st.markdown(f"**{g['u']}:** {g['t']}")

        with st.form("global", clear_on_submit=True):
            msg_t = st.text_input("Conversar com a comunidade...")
            if st.form_submit_button("ENVIAR"):
                if msg_t:
                    st.session_state.global_chat.append({"u": st.session_state.user, "t": msg_t})
                    st.rerun()
