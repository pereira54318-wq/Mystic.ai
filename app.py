import streamlit as st
import time
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI v4.1 👺", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILO CSS CLEAN RED (LISO) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #1a0000 60%, #330000 100%);
        color: #ff0000;
    }
    .text-3d-giant {
        font-family: 'Arial Black', sans-serif;
        font-size: 50px;
        line-height: 0.8;
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: -4px;
        text-shadow: 0 4px 15px rgba(255,0,0,0.7);
        margin-bottom: 30px;
    }
    .stChatMessage {
        background: linear-gradient(90deg, #1a0000 0%, #000000 100%) !important;
        border: 2px solid #ff0000 !important;
        border-radius: 15px !important;
    }
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 25px;
        border: 2px solid #ff0000 !important;
        border-radius: 30px !important;
        background: #000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO DO SISTEMA ---
if "logado" not in st.session_state: st.session_state.logado = False
if "mensagens" not in st.session_state: st.session_state.mensagens = []
if "global_chat" not in st.session_state: st.session_state.global_chat = []

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown('<div class="text-3d-giant">MELHOR IA DE<br>GERAR SCRIPT</div>', unsafe_allow_html=True)
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("INJETAR ACESSO"):
        if u: 
            st.session_state.user = u
            st.session_state.logado = True
            st.rerun()
else:
    # --- INTERFACE PRINCIPAL ---
    tab_ia, tab_perfil = st.tabs(["💬 TERMINAL", "👤 PERFIL / CHAT GLOBAL"])

    with tab_ia:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ NOVO SCRIPT"): st.session_state.mensagens = []; st.rerun()
        with col2:
            if st.button("🔄 NOVO CHAT"): st.session_state.mensagens = []; st.rerun()

        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Solicite seu Script Rayfield..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                placeholder = st.empty()
                # CORREÇÃO: Usando {{ }} para evitar o SyntaxError do Streamlit
                lua_code = f"""local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = "MYSTIC HUB | {prompt}",
    LoadingTitle = "Pereira System Injetando...",
    ConfigurationSaving = {{ Enabled = true, FileName = "MysticConfig" }}
}})
local Tab = Window:CreateTab("Scripts", 4483362458)
Tab:CreateButton({{
    Name = "Ativar {prompt}",
    Callback = function()
        print("Ativado via Mystic AI")
    end
}})"""
                full_res = f"📡 **Script Gerado:**\n\n```lua\n{lua_code}\n```"
                placeholder.markdown(full_res)
                st.session_state.mensagens.append({"role": "assistant", "content": full_res})

    with tab_perfil:
        st.markdown("<h3 style='color:red;'>🌐 CHAT COMUNIDADE (REAL TIME)</h3>", unsafe_allow_html=True)
        # Mostrar mensagens globais
        for g_msg in st.session_state.global_chat:
            st.write(f"**{g_msg['user']}:** {g_msg['text']}")
        
        with st.form("msg_comu", clear_on_submit=True):
            t_msg = st.text_input("Diga algo para a galera...")
            if st.form_submit_button("ENVIAR"):
                st.session_state.global_chat.append({"user": st.session_state.user, "text": t_msg})
                st.rerun()
