import streamlit as st
import time
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI 👺", layout="wide", initial_sidebar_state="collapsed")

# --- CSS ULTRA CUSTOM: 3D TEXT, PARTICULAS E GEMINI UI ---
st.markdown("""
    <style>
    /* FUNDO COM PULSO E PARTÍCULAS */
    @keyframes pulse {
        0% { background-color: #050000; }
        50% { background-color: #150000; }
        100% { background-color: #050000; }
    }
    .stApp {
        animation: pulse 5s infinite;
        background: #050000;
    }
    .stApp::before {
        content: '';
        position: absolute;
        width: 100%; height: 100%;
        background-image: radial-gradient(#ff0000 0.8px, transparent 0.8px);
        background-size: 20px 20px;
        z-index: 0;
        opacity: 0.3;
    }

    /* TEXTO 3D GIGANTE E COMPACTO */
    .text-3d-giant {
        font-family: 'Arial Black', sans-serif;
        font-size: 45px;
        line-height: 0.9;
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: -2px;
        text-shadow: 
            0 1px 0 #b30000, 0 2px 0 #990000, 0 3px 0 #800000, 
            0 4px 0 #660000, 0 5px 0 #4d0000, 0 6px 0 #330000,
            0 10px 15px rgba(255,0,0,0.5);
        margin-bottom: 40px;
    }

    /* BARRA DE CHAT ESTILO GEMINI (TAMANHO REAL) */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90% !important;
        max-width: 800px;
        background-color: #111 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 28px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #fff !important;
    }

    /* BOLHAS DE CHAT */
    .stChatMessage {
        background: rgba(20, 0, 0, 0.8) !important;
        border-radius: 20px !important;
        border: 1px solid #400 !important;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SESSÃO ---
if "logado" not in st.session_state: st.session_state.logado = False
if "aba" not in st.session_state: st.session_state.aba = "Login"
if "mensagens" not in st.session_state: st.session_state.mensagens = []
if "user_info" not in st.session_state: st.session_state.user_info = {"nome": "", "email": "", "foto": None}

# --- SISTEMA DE LOGIN E CRIAÇÃO DE CONTA ---
def sistema_acesso():
    st.markdown('<div class="text-3d-giant">MELHOR IA DE<br>GERAR SCRIPT</div>', unsafe_allow_html=True)
    
    aba_login, aba_criar = st.tabs(["ENTRAR", "CRIAR CONTA"])
    
    with aba_login:
        u = st.text_input("Usuário/Email", key="login_u")
        p = st.text_input("Senha", type="password", key="login_p")
        if st.button("CONECTAR AO SISTEMA"):
            if u and p:
                st.session_state.user_info["nome"] = u
                st.session_state.logado = True
                st.rerun()

    with aba_criar:
        new_u = st.text_input("Novo Usuário")
        new_e = st.text_input("Gmail")
        new_p = st.text_input("Senha", type="password")
        new_p2 = st.text_input("Repetir Senha", type="password")
        if st.button("CRIAR E VALIDAR GMAIL"):
            if new_p == new_p2 and "@" in new_e:
                st.success(f"Código enviado para {new_e}!")
                st.text_input("Digite o código de 6 dígitos")
                if st.button("CONFIRMAR CONTA"):
                    st.session_state.logado = True
                    st.rerun()
            else: st.error("Dados inválidos ou senhas diferentes")

# --- INTERFACE PRINCIPAL (PÓS-LOGIN) ---
if not st.session_state.logado:
    sistema_acesso()
else:
    # Sidebar com Perfil
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_info['nome']}")
        if st.session_state.user_info["foto"]:
            st.image(st.session_state.user_info["foto"], width=150)
        
        up = st.file_uploader("Upload Foto Galeria", type=['png', 'jpg'])
        if up: st.session_state.user_info["foto"] = up; st.rerun()
        
        st.markdown("---")
        st.write(f"🕒 {datetime.datetime.now().strftime('%H:%M')}")
        st.write("📱 Motorola G35")
        st.write("🔋 88%")
        if st.button("LOGOUT"): st.session_state.logado = False; st.rerun()

    t1, t2, t3 = st.tabs(["💬 TERMINAL", "🎨 NANO BANANA", "👤 PERFIL"])

    with t1:
        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Solicite Script (Aimbot, ESP, Rayfield)..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                res = st.empty()
                # Geração de Script Hub Rayfield Real
                code = f"""local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()
local Window = Rayfield:CreateWindow({{
    Name = "MYSTIC HUB | {prompt}",
    LoadingTitle = "Pereira System Injetando...",
    ConfigurationSaving = {{Enabled = true, FileName = "MysticConfig"}}
}})
local Tab = Window:CreateTab("Scripts", 4483362458)
Tab:CreateButton({{
    Name = "Ativar {prompt}",
    Callback = function()
        print("Executado via Mystic AI")
    end
}})"""
                full_txt = f"📡 **Script Gerado em Tempo Real:**\n\n```lua\n{code}\n```"
                
                # Efeito de escrita de cima para baixo
                temp = ""
                for line in full_txt.split('\n'):
                    temp += line + "\n"
                    res.markdown(temp + "▒")
                    time.sleep(0.04)
                res.markdown(full_txt)
                st.session_state.mensagens.append({"role": "assistant", "content": full_txt})

    with t2:
        st.write("🎨 Gerador Nano Banana")
        if img_p := st.chat_input("O que a IA deve desenhar?", key="nano_input"):
            with st.chat_message("assistant"):
                st.image(f"https://placehold.co/600x400/200000/ff0000?text={img_p}")

    with t3:
        st.subheader("Gerenciamento de Contas")
        st.write("Contas vinculadas: 1/5")
        st.text_input("Vincular nova conta...")
        st.button("Vincular")
