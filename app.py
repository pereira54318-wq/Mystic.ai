import streamlit as st
import time
import datetime
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC MAGO AI 🧙🏻‍♂️", layout="wide", initial_sidebar_state="collapsed")

# --- FUNÇÃO PARA CARREGAR A LOGO DO MAGO ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Certifique-se de que a imagem do mago se chama 'mago.png' no seu repositório
logo_mago = get_base64_image("mago.png")

# --- CSS PREMIMUM: VISUAL MAGO HACKER LISO ---
st.markdown(f"""
    <style>
    /* FUNDO LISO TOTAL RED & BLACK */
    .stApp {{
        background: linear-gradient(180deg, #000000 0%, #1a0000 50%, #4d0000 100%);
        color: #ff0000;
    }}

    /* TEXTO 3D GIGANTE COLADO */
    .text-3d-giant {{
        font-family: 'Arial Black', sans-serif;
        font-size: 55px;
        line-height: 0.75;
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: -5px;
        text-shadow: 0 4px 15px rgba(255,0,0,0.6);
        margin-bottom: 30px;
    }}

    /* ABA VERMELHA (TABS CUSTOM) */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #300000;
        border-radius: 10px;
        padding: 5px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ff0000 !important;
        font-weight: bold;
    }}

    /* BARRA DE CHAT MAIOR COM CONTORNO VERMELHO (ESTILO GEMINI) */
    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 95% !important;
        max-width: 900px;
        border: 3px solid #ff0000 !important; /* Contorno maior */
        border-radius: 35px !important;
        background: #000 !important;
        padding: 10px !important;
    }}

    /* CHAT VERMELHO COM DEGRADÊ */
    .stChatMessage {{
        background: linear-gradient(90deg, #300000 0%, #000000 100%) !important;
        border: 2px solid #ff0000 !important;
        border-radius: 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS ---
if "logado" not in st.session_state: st.session_state.logado = False
if "mensagens" not in st.session_state: st.session_state.mensagens = []
if "global_chat" not in st.session_state: st.session_state.global_chat = []

# --- TELA DE ACESSO ---
if not st.session_state.logado:
    if logo_mago:
        st.markdown(f'<center><img src="data:image/png;base64,{logo_mago}" width="200"></center>', unsafe_allow_html=True)
    st.markdown('<div class="text-3d-giant">MELHOR IA DE<br>GERAR SCRIPT</div>', unsafe_allow_html=True)
    
    u = st.text_input("Usuário 🧙🏻‍♂️")
    p = st.text_input("Senha 🧙🏻‍♂️", type="password")
    if st.button("INJETAR ACESSO MAGO"):
        if u:
            st.session_state.user = u
            st.session_state.logado = True
            st.rerun()
else:
    # --- SIDEBAR LIMPA COM LOGO DO MAGO ---
    with st.sidebar:
        if logo_mago:
            st.image(f"data:image/png;base64,{logo_mago}", width=120)
        st.markdown(f"### 🧙🏻‍♂️ {st.session_state.user}")
        if st.button("LOGOUT"):
            st.session_state.logado = False
            st.rerun()

    # --- ORGANIZAÇÃO DAS ABAS ---
    tab_script, tab_banana, tab_prog, tab_perfil = st.tabs(["📜 SCRIPT", "🎨 NANOBANANA", "💻 PROGRAMAÇÃO", "👤 PERFIL / CHAT GLOBAL"])

    # ABA 1: SCRIPT
    with tab_script:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🧙🏻‍♂️ NOVO SCRIPT"): st.session_state.mensagens = []; st.rerun()
        with c2:
            if st.button("🧙🏻‍♂️ NOVO CHAT"): st.session_state.mensagens = []; st.rerun()

        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Solicite seu Script Rayfield..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                # Uso de {{ }} para evitar erro de sintaxe f-string no Python
                lua = f"""local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = "Mystic Mago | {prompt}",
    LoadingTitle = "Injetando Core...",
    ConfigurationSaving = {{ Enabled = true, FileName = "Mystic" }}
}})
-- Script gerado para {prompt} via Pereira System"""
                full = f"📡 **Terminal Mago:**\n\n```lua\n{lua}\n```"
                st.markdown(full)
                st.session_state.mensagens.append({"role": "assistant", "content": full})

    # ABA 2: NANOBANANA
    with tab_banana:
        st.markdown("<h2 style='color:red; text-align:center;'>🎨 GERADOR NANOBANANA 🧙🏻‍♂️</h2>", unsafe_allow_html=True)
        st.write("Em breve: Geração de logos e artes diretamente aqui.")

    # ABA 3: PROGRAMAÇÃO (ENSINO EM TEMPO REAL)
    with tab_prog:
        st.markdown("<h2 style='color:red; text-align:center;'>💻 AULA DE PROGRAMAÇÃO ONLINE 🧙🏻‍♂️</h2>", unsafe_allow_html=True)
        st.info("Aqui você aprende a criar seus próprios scripts em tempo real.")
        aula = st.selectbox("Escolha o que aprender:", ["Roblox Luau", "Python Básico", "HTML/CSS Hacker"])
        if aula == "Roblox Luau":
            st.code("print('Hello World') -- Isso é o começo de tudo!", language="lua")
            st.write("Dica do Mago: Sempre use variáveis locais para otimizar seu script.")

    # ABA 4: PERFIL / CHAT GLOBAL (VISUAL VERMELHO)
    with tab_perfil:
        st.markdown("<h2 style='color:red; text-align:center;'>🌐 CHAT COMUNIDADE ONLINE 🧙🏻‍♂️</h2>", unsafe_allow_html=True)
        
        # Container de Chat Global
        with st.container(height=350):
            for g in st.session_state.global_chat:
                st.markdown(f"**🧙🏻‍♂️ {g['u']}:** {g['t']}")

        with st.form("global_form", clear_on_submit=True):
            txt = st.text_input("Escreva para outros magos...")
            if st.form_submit_button("ENVIAR 📡"):
                if txt:
                    st.session_state.global_chat.append({"u": st.session_state.user, "t": txt})
                    st.rerun()
