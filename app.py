import streamlit as st
import time
import datetime

# --- CONFIGURAÇÃO DA PÁGINA (MOBILE/PC) ---
st.set_page_config(title="MYSTIC AI v3.0 👺", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PREMIMUM: ANIMAÇÕES, FUNDO E LAYOUT GEMINI ---
# Inclui: Fundo piscando (keyframe 'pulse'), Bolhas piscando ('sparkle'), Layout Gemini.
st.markdown("""
    <style>
    /* FUNDO ANMADO PISCANDO LENTAMENTE EM VERMELHO */
    @keyframes pulse {
        0% { background-color: #030000; }
        50% { background-color: #0d0000; }
        100% { background-color: #030000; }
    }
    
    .stApp {
        animation: pulse 8s infinite;
        background: #030000;
        color: #ff0000;
    }

    /* BOLINHAS VERMELHAS BRILHANTES PISCANDO (Simuladas via Background-Image) */
    @keyframes sparkle {
        0%, 100% { opacity: 0.1; }
        50% { opacity: 0.2; }
    }
    .stApp::before {
        content: '';
        position: absolute;
        width: 100%; height: 100%;
        background-image: radial-gradient(#ff0000 0.6px, transparent 0.6px);
        background-size: 20px 20px;
        animation: sparkle 4s infinite ease-in-out;
        z-index: 0;
        pointer-events: none;
    }

    /* LAYOUT GEMINI: ÁREA DE CHAT SCROLLÁVEL */
    .chat-wrapper {
        display: flex;
        flex-direction: column-reverse; /* Mensagens de baixo para cima */
        overflow-y: auto;
        height: 75vh;
        padding-bottom: 20px;
        position: relative; z-index: 1;
    }

    /* BOLHAS DE CHAT ESTILIZADAS E NEON */
    .stChatMessage {
        background: rgba(10, 0, 0, 0.9) !important;
        border: 1px solid #ff0000 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.1) !important;
        color: #ff4444 !important;
        margin-bottom: 12px;
    }

    /* ESTILO DO BLOCO DE CÓDIGO (NEON BRANCO/VERMELHO) */
    code { 
        color: #fff !important; 
        background-color: #000 !important; 
        text-shadow: 0 0 5px #ff0000;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stCode { border: 1px solid #440000; border-radius: 8px; }

    /* INPUT DE CHAT FIXO EMBAIXO */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 15px;
        background-color: #000 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 20px !important;
        color: #ff4444 !important;
        font-family: 'Courier New', monospace;
    }

    /* PERFIL E SIDEBAR HACKER */
    .profile-card {
        border: 2px solid #ff0000;
        padding: 15px;
        border-radius: 12px;
        background: rgba(20, 0, 0, 0.9);
        box-shadow: 0 0 25px #ff0000;
        margin-bottom: 20px;
    }
    .vinculado-card {
        background: rgba(100, 0, 0, 0.1);
        border: 1px solid #440000;
        padding: 10px; border-radius: 8px;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE SESSÃO ---
if "logado" not in st.session_state: st.session_state.logado = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "User Hacker", "email": "", "foto": None}
if "contas_vinculadas" not in st.session_state: st.session_state.contas_vinculadas = []
if "messages_script" not in st.session_state: st.session_state.messages_script = []
if "messages_image" not in st.session_state: st.session_state.messages_image = []

# --- SISTEMA DE ACESSO (LOGIN/REGISTRO) ---
def tela_login():
    st.markdown("<h1 style='text-align: center; font-family: Courier;'>👺 MYSTIC ACCESS_</h1>", unsafe_allow_html=True)
    menu = ["_Aceder", "_Registrar"]
    escolha = st.selectbox("", menu)

    col1, col2 = st.columns([1,1])
    with col1:
        user = st.text_input("usuário_id", value=st.session_state.user_data["nome"])
        pw = st.text_input("senha_core", type='password')
    with col2:
        if escolha == "_Registrar":
            email = st.text_input("gmail_core")
            pw2 = st.text_input("confirmar_senha_core", type='password')

    if st.button("_Injetar Acesso"):
        if escolha == "_Aceder":
            st.session_state.logado = True
            st.rerun()
        elif choice == "_Registrar":
            if pw == pw2 and email:
                st.session_state.user_data["nome"] = user
                st.session_state.user_data["email"] = email
                st.success("Conta Registrada no Core.")
            else: st.error("Erro nos Parâmetros.")

# --- INTERFACE PRINCIPAL G35 OPTIMIZED ---
if not st.session_state.logado:
    tela_login()
else:
    # Sidebar com Perfil Hacker
    with st.sidebar:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        # Foto de Perfil
        if st.session_state.user_data["foto"]:
            st.image(st.session_state.user_data["foto"], width=100)
        else:
            st.markdown("<h1 style='color: red;'>👺</h1>", unsafe_allow_html=True)
        st.write(f"### ID: {st.session_state.user_data['nome']}")
        # Input para foto da galeria
        img_file = st.file_uploader("_Mudar_Hacker_Pic", type=['png', 'jpg'])
        if img_file:
            st.session_state.user_data["foto"] = img_file
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.write("⚙️ __STATUS_SYS_")
        st.write(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}")
        st.write(f"📅 {datetime.date.today()}")
        st.write("🔋 85%")
        st.write("📱 G35")
        if st.button("_Desconectar"): 
            st.session_state.logado = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    tab_script, tab_image = st.tabs(["💬 _SCRIPT GEN_", "🎨 _NANO_BANANA_"])

    # --- TAB 1: GERADOR DE SCRIPT LUA ---
    with tab_script:
        st.markdown("👺 __TERMINAL_SCRIPT__V3.0")
        
        # Container de Chat Estilo Gemini
        chat_container = st.container()
        
        # Renderiza as mensagens
        with chat_container:
            for m in st.session_state.messages_script:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])
        
        # Input Gemini Fixo
        if prompt := st.chat_input("Solicite Script (ex: Fly, ESP)..."):
            st.session_state.messages_script.append({"role": "user", "content": prompt})
            st.rerun() # Atualiza para mostrar o prompt do usuário antes da IA

        # Lógica de Resposta da IA (Processa após o rerun do input)
        if st.session_state.messages_script and st.session_state.messages_script[-1]["role"] == "user":
            user_msg = st.session_state.messages_script[-1]["content"]
            
            with st.chat_message("assistant"):
                res_area = st.empty()
                status = st.empty()
                status.markdown("💉 _Injetando decodificador Rayfield...")
                time.sleep(1)
                
                # GERAÇÃO DINÂMICA DE SCRIPT RAYFIELD (Não Loadstring)
                p = user_msg.lower()
                script_raw = "-- [MYSTIC AI_RAYFIELD HUB]\nlocal Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()\n\nlocal Window = Rayfield:CreateWindow({\n    Name = 'Pereira System | RP Utility',\n    LoadingTitle = 'Injetando Core...',\n    LoadingSubtitle = 'pelo Pereira54318-wq',\n    ConfigurationSaving = {\n        Enabled = true,\n        FolderName = 'PereiraSystemConfig',\n        FileName = 'MysticScriptRP'\n    },\n    KeySystem = false\n})\n\nlocal Tab = Window:CreateTab('Principal', 4483362458)\n\nlocal Section = Tab:CreateSection('Visuais')\n"
                
                if "esp" in p:
                    script_raw += "\nTab:CreateButton({\n    Name = 'Ativar ESP (Boxes)',\n    Callback = function()\n        -- Código complexo de renderização de ESP injetado aqui...\n        print('MYSTIC AI: ESP Ativado!')\n    end\n})\n"
                elif "fly" in p:
                    script_raw += "\nTab:CreateButton({\n    Name = 'Ativar Fly Hack',\n    Callback = function()\n        -- Lógica de voo CFrame injetada aqui...\n        print('MYSTIC AI: Voo Ativado!')\n    end\n})\n"
                else:
                    script_raw += f"\nTab:CreateLabel('Solicitação: {user_msg}')\nTab:CreateButton({{\n    Name = 'Ativar Custom',\n    Callback = function()\n        loadstring(game:HttpGet('https://api.mystic.ai'))()\n    end\n}})\n"

                # Efeito Gemini: Digitação de Cima para Baixo
                full_res = f"📡 Código gerado para **{user_msg}** no Terminal Rayfield:\n\n```lua\n{script_raw}\n```"
                displayed = ""
                
                # Divide em linhas para digitação mais natural
                for line in full_res.split('\n'):
                    displayed += line + '\n'
                    res_area.markdown(displayed + "▒")
                    time.sleep(0.01)
                res_area.markdown(full_res)
                st.session_state.messages_script.append({"role": "assistant", "content": full_res})

    # --- TAB 2: GERADOR DE IMAGEM NANO_BANANA ---
    with tab_image:
        st.markdown("🍌 __NANO_BANANA_IMAGE_GEN_")
        
        # Container de Chat Estilo Gemini
        image_chat_container = st.container()
        
        with image_chat_container:
            for m in st.session_state.messages_image:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])
        
        # Input Gemini Fixo
        if desc := st.chat_input("Descreva imagem..."):
            st.session_state.messages_image.append({"role": "user", "content": desc})
            st.rerun()

        # Lógica de Resposta da IA (Processa após o rerun do input)
        if st.session_state.messages_image and st.session_state.messages_image[-1]["role"] == "user":
            user_desc = st.session_state.messages_image[-1]["content"]
            
            with st.chat_message("assistant"):
                res_area_img = st.empty()
                status_img = st.empty()
                status_img.markdown("🎨 _Decodificando NanoBanana Core...")
                time.sleep(2.5)
                
                # Gera Imagem (Simulada via placeholder)
                img_url = f"https://placehold.co/600x400/200000/ff0000?text=MYSTIC_{user_desc.replace(' ', '+')}"
                full_res_img = f"📡 Foto para **{user_desc}** processada:\n\n<img src='{img_url}' width='100%'>"
                
                res_area_img.markdown(full_res_img, unsafe_allow_html=True)
                st.session_state.messages_image.append({"role": "assistant", "content": full_res_img})
