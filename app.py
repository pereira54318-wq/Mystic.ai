import streamlit as st
import time
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI v3.1 👺", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PREMIMUM: 3D TEXT, ANIMAÇÕES E FUNDO ---
st.markdown("""
    <style>
    @keyframes pulse {
        0% { background-color: #030000; }
        50% { background-color: #120000; }
        100% { background-color: #030000; }
    }
    
    .stApp {
        animation: pulse 6s infinite;
        background: #030000;
        color: #ff0000;
    }

    /* TEXTO 3D NEGRITO */
    .text-3d {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.5em;
        font-weight: bold;
        color: #ff0000;
        text-align: center;
        text-transform: uppercase;
        text-shadow: 
            0 1px 0 #800000, 0 2px 0 #700000, 
            0 3px 0 #600000, 0 4px 0 #500000, 
            0 5px 0 #400000, 0 6px 1px rgba(0,0,0,.1), 
            0 0 5px rgba(255,0,0,.2), 0 1px 3px rgba(255,0,0,.3), 
            0 3px 5px rgba(255,0,0,.2), 0 5px 10px rgba(255,0,0,.25), 
            0 10px 10px rgba(255,0,0,.2), 0 20px 20px rgba(255,0,0,.15);
        margin-bottom: 30px;
    }

    /* BOLINHAS BRILHANTES */
    .stApp::before {
        content: '';
        position: absolute;
        width: 100%; height: 100%;
        background-image: radial-gradient(#ff0000 0.7px, transparent 0.7px);
        background-size: 25px 25px;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
    }

    /* INPUT GEMINI EMBAIXO */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        z-index: 99;
    }

    .stChatMessage {
        background: rgba(15, 0, 0, 0.9) !important;
        border: 1px solid #ff0000 !important;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if "logado" not in st.session_state: st.session_state.logado = False
if "user_name" not in st.session_state: st.session_state.user_name = "Hacker"
if "msg_script" not in st.session_state: st.session_state.msg_script = []
if "foto_perfil" not in st.session_state: st.session_state.foto_perfil = None

# --- TELA DE LOGIN ---
def mostrar_login():
    st.markdown('<div class="text-3d">MELHOR IA DE GERAR SCRIPT</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>👺 MYSTIC LOGIN</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("Usuário")
    with col2:
        p = st.text_input("Senha", type="password")
    
    if st.button("INJETAR ACESSO"):
        if u:
            st.session_state.user_name = u
            st.session_state.logado = True
            st.rerun()

# --- INTERFACE PRINCIPAL ---
if not st.session_state.logado:
    mostrar_login()
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"<h2 style='color:red;'>👺 {st.session_state.user_name}</h2>", unsafe_allow_html=True)
        if st.session_state.foto_perfil:
            st.image(st.session_state.foto_perfil, width=150)
        
        f = st.file_uploader("Trocar Foto", type=['png', 'jpg'])
        if f: 
            st.session_state.foto_perfil = f
            st.rerun()
            
        st.write(f"📱 Motorola G35")
        st.write(f"🔋 85%")
        if st.button("SAIR"):
            st.session_state.logado = False
            st.rerun()

    t1, t2 = st.tabs(["💬 TERMINAL", "🎨 IMAGEM"])

    with t1:
        # Área de Chat
        for m in st.session_state.msg_script:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("Diga o que quer hackear..."):
            st.session_state.msg_script.append({"role": "user", "content": prompt})
            
            with st.chat_message("assistant"):
                placeholder = st.empty()
                # GERAÇÃO RAYFIELD REAL
                script = f"""-- [MYSTIC AI v3.1]
local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = "Pereira System | {prompt}",
    LoadingTitle = "Injetando...",
    ConfigurationSaving = {{Enabled = true, FolderName = "Mystic", FileName = "Config"}}
}})
local Tab = Window:CreateTab("Scripts", 4483362458)
Tab:CreateButton({{
    Name = "Executar {prompt}",
    Callback = function()
        print("Ativado pelo Pereira54318-wq")
    end
}})"""
                full_res = f"📡 **Script Gerado:**\n\n```lua\n{script}\n```"
                
                # Efeito de digitação de cima para baixo
                temp_text = ""
                for line in full_res.split('\n'):
                    temp_text += line + "\n"
                    placeholder.markdown(temp_text + "▒")
                    time.sleep(0.05)
                placeholder.markdown(full_res)
                st.session_state.msg_script.append({"role": "assistant", "content": full_res})

    with t2:
        st.write("🎨 Gerador NanoBanana")
        if img_p := st.chat_input("Descreva a imagem...", key="img_input"):
             with st.chat_message("assistant"):
                 st.write(f"Gerando: {img_p}")
                 st.image(f"https://placehold.co/600x400/200000/ff0000?text={img_p}")
                 
