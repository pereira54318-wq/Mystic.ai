import streamlit as st
import time
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

    /* BARRA DE CHAT GIGANTE COM CONTORNO VERMELHO */
    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 95% !important;
        max-width: 1000px;
        border: 4px solid #ff0000 !important;
        border-radius: 40px !important;
        background: #000 !important;
        padding: 15px !important;
        z-index: 999;
    }}

    /* AJUSTE PARA O CONTEÚDO */
    .main .block-container {{
        padding-bottom: 150px;
    }}

    /* TABS VERMELHAS */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #200000;
        border-radius: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ff0000 !important;
        font-weight: bold;
    }}
    
    .stChatMessage {{
        background: linear-gradient(90deg, #2a0000 0%, #000000 100%) !important;
        border: 2px solid #ff0000 !important;
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
    
    aba_login, aba_cadastro = st.tabs(["ENTRAR", "CRIAR CONTA"])
    
    with aba_login:
        u = st.text_input("Usuário", key="user_login")
        p = st.text_input("Senha", type="password", key="pass_login")
        if st.button("INJETAR ACESSO MAGO"):
            if u:
                st.session_state.user = u
                st.session_state.logado = True
                st.rerun()
                
    with aba_cadastro:
        st.text_input("Escolha um Usuário")
        st.text_input("Seu Gmail")
        st.text_input("Crie uma Senha", type="password")
        if st.button("CRIAR MINHA CONTA"):
            st.success("Conta criada com sucesso!")

else:
    # --- SIDEBAR ---
    with st.sidebar:
        if logo_mago:
            st.image(f"data:image/png;base64,{logo_mago}", width=120)
        st.markdown(f"###  {st.session_state.user}")
        if st.button("SAIR"):
            st.session_state.logado = False
            st.rerun()

    # --- APENAS SCRIPT E PERFIL ---
    tab_script, tab_perfil = st.tabs(["SCRIPT", "CHAT GLOBAL"])

    # ABA 1: SCRIPT (TERMINAL LIMPO)
    with tab_script:
        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Diga o script que deseja..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                # Uso de {{ }} para evitar erro de f-string
                lua = f"""local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = "Mystic Mago | {prompt}",
    LoadingTitle = "Pereira System",
}})
-- Script Hub para {prompt} gerado."""
                full = f" **Mago Terminal:**\n\n```lua\n{lua}\n```"
                st.markdown(full)
                st.session_state.mensagens.append({"role": "assistant", "content": full})

    # ABA 2: PERFIL / CHAT GLOBAL
    with tab_perfil:
        st.markdown("<h2 style='color:red; text-align:center;'> CHAT GLOBAL ONLINE </h2>", unsafe_allow_html=True)
        
        with st.container(height=400):
            for g in st.session_state.global_chat:
                st.markdown(f"** {g['u']}:** {g['t']}")

        with st.form("global_msg", clear_on_submit=True):
            txt = st.text_input("Escreva para a comunidade...")
            if st.form_submit_button("ENVIAR"):
                if txt:
                    st.session_state.global_chat.append({"u": st.session_state.user, "t": txt})
                    st.rerun()
                    
