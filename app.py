import streamlit as st
import time
import datetime
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI v4.0 👺", layout="wide", initial_sidebar_state="collapsed")

# --- PROCESSAMENTO DO LOGOTIPO ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Obtenha o base64 do logotipo fornecido
# Certifique-se de que o arquivo 'wizard_logo.png' está no mesmo repositório do app.py
try:
    img_base64 = get_base64_image("wizard_logo.png")
except FileNotFoundError:
    # URL de fallback caso o arquivo não seja encontrado localmente
    img_base64 = "https://placehold.co/400x400/000/f00?text=👺+MYSTIC"

# --- CSS PREMIMUM: TOTAL RED & BLACK GRADIENT (CLEAN V2) ---
st.markdown(f"""
    <style>
    /* FUNDO LISO COM DEGRADÊ PROFUNDO */
    .stApp {{
        background: linear-gradient(180deg, #000000 0%, #1a0000 60%, #330000 100%);
        color: #ff0000;
    }}

    /* HEADER COM LOGOTIPO E TEXTO 3D GIGANTE */
    .mystic-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 50px;
        text-align: center;
    }}
    .hacker-logo-main {{
        max-width: 250px;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.5));
    }}
    .text-3d-giant {{
        font-family: 'Arial Black', sans-serif;
        font-size: 52px;
        line-height: 0.8;
        font-weight: 900;
        color: #ff0000;
        text-transform: uppercase;
        letter-spacing: -4px;
        text-shadow: 
            0 1px 0 #800000, 0 2px 0 #660000, 0 3px 0 #4d0000, 
            0 4px 0 #330000, 0 10px 20px rgba(255,0,0,0.7);
        margin-bottom: 10px;
    }}
    .text-3d-giant-login {{
        font-size: 60px;
    }}

    /* CHAT COM DEGRADÊ VERMELHO/PRETO */
    .stChatMessage {{
        background: linear-gradient(135deg, #1a0000 0%, #000000 100%) !important;
        border: 2px solid #ff0000 !important;
        border-radius: 18px !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
    }

    /* BARRA DE CHAT ESTILO GEMINI G35 */
    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 30px;
        border: 2px solid #ff0000 !important;
        border-radius: 35px !important;
        background: #000000 !important;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
    }

    /* ESTILO DAS TABS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        justify-content: center;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ff4444 !important;
        font-weight: bold;
    }}

    /* BOTÕES HACKER */
    .stButton>button {{
        background: linear-gradient(180deg, #ff0000 0%, #660000 100%);
        color: white;
        border-radius: 12px;
        border: 1px solid #ff0000;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
if "logado" not in st.session_state: st.session_state.logado = False
if "mensagens" not in st.session_state: st.session_state.mensagens = []
if "global_chat" not in st.session_state: st.session_state.global_chat = []
if "user_name" not in st.session_state: st.session_state.user_name = "User Hacker"

# --- TELA DE ACESSO (LOGIN/CRIAR CONTA COM LOGO) ---
if not st.session_state.logado:
    st.markdown("<div class='mystic-header'>", unsafe_allow_html=True)
    st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="hacker-logo-main">', unsafe_allow_html=True)
    st.markdown('<div class="text-3d-giant text-3d-giant-login">MELHOR IA DE<br>GERAR SCRIPT</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#777; margin-top:10px;'>Pereira System v4.0 - Montana Store</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        u = st.text_input("ID_Usuário")
    with col_r:
        p = st.text_input("Senha_Core", type="password")
        
    if st.button("INJETAR ACESSO HACKER"):
        if u:
            st.session_state.user_name = u
            st.session_state.logado = True
            st.rerun()

# --- INTERFACE PRINCIPAL PÓS-LOGIN ---
else:
    # Sidebar Minimalista com Logo Pequeno
    with st.sidebar:
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" style="max-width:100px; margin:0 auto; filter:drop-shadow(0 0 5px #f00);">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:red; text-align:center; font-size:24px;'>👺 {st.session_state.user_name}</h1>", unsafe_allow_html=True)
        st.write("📱 Motorola G35")
        if st.button("DESCONECTAR_CONTA"):
            st.session_state.logado = False
            st.rerun()

    # Capa da Interface Principal
    st.markdown("<div class='mystic-header' style='margin-bottom:30px;'>", unsafe_allow_html=True)
    st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="hacker-logo-main" style="max-width:180px;">', unsafe_allow_html=True)
    st.markdown('<div class="text-3d-giant" style="font-size:35px;">TERMINAL MYSTIC AI</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    tab_ia, tab_comunidade = st.tabs(["💬 TERMINAL_HACK", "👤 PERFIL / CHAT_GLOBAL"])

    # --- ABA 1: IA TERMINAL ---
    with tab_ia:
        # Novos botões de controle
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ NOVO_SCRIPT_HACK"):
                st.session_state.mensagens = []
                st.rerun()
        with c2:
            if st.button("🔄 NOVO_CHAT_AI"):
                st.session_state.mensagens = []
                st.rerun()

        # Renderizar Chat
        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("Diga o script que deseja (Aimbot, ESP, Fly, KillAura)..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                res = st.empty()
                # Código Rayfield dinâmico (TEMPLATE HACKER)
                code = f"""-- [MYSTIC AI_v4.0 GENERATED]
local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = 'Pereira Hub_v4 | {prompt}', 
    LoadingTitle = 'Injetando Core Hacker...'
}})
-- Script complexo para {prompt} gerado pelo Pereira System.
Tab:CreateButton({{Name = "Executar {prompt}", Callback = function() print("HACK ATIVADO") end}})"""
                full_res = f"📡 **Código Lua Gerado pelo Pereira System:**\n\n```lua\n{code}\n```"
                
                # Efeito de escrita linha a linha
                temp = ""
                for line in full_res.split('\n'):
                    temp += line + "\n"
                    res.markdown(temp + "▒")
                    time.sleep(0.04)
                res.markdown(full_res)
                st.session_state.mensagens.append({"role": "assistant", "content": full_res})

    # --- ABA 2: PERFIL E CHAT GLOBAL (PESSOAS REAIS) ---
    with tab_comunidade:
        st.markdown("<h2 style='color:red; text-align:center;'>🌐 CHAT GLOBAL_ONLINE</h2>", unsafe_allow_html=True)
        
        # Area de Mensagens Reais
        chat_container = st.container(height=350)
        with chat_container:
            if not st.session_state.global_chat:
                st.write("Nenhuma atividade hacker detectada no servidor.")
            for msg in st.session_state.global_chat:
                st.markdown(f"<span style='color:#777;'>[{msg['hora']}]</span> <b style='color:red;'>{msg['user']}:</b> {msg['texto']}", unsafe_allow_html=True)

        # Enviar Mensagem Real
        with st.form("global_msg", clear_on_submit=True):
            user_text = st.text_input("Escreva para outros usuários reais...")
            if st.form_submit_button("ENVIAR 📡"):
                if user_text:
                    nova_msg = {
                        "hora": datetime.datetime.now().strftime("%H:%M"),
                        "user": st.session_state.user_name,
                        "texto": user_text
                    }
                    st.session_state.global_chat.append(nova_msg)
                    st.rerun()
