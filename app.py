import streamlit as st
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI", layout="wide", initial_sidebar_state="collapsed")

# --- FUNÇÃO PARA CARREGAR A LOGO ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_mago = get_base64_image("mago.png")

# --- CSS PREMIMUM: LIMPO E SEM EMOJIS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, #000000 0%, #1a0000 50%, #4d0000 100%);
        color: #ff0000;
    }}
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
    /* BARRA DE CHAT REDUZIDA */
    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 80% !important;
        max-width: 650px;
        border: 2px solid #ff0000 !important;
        border-radius: 15px !important;
        background: #000 !important;
        padding: 5px !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #200000;
        border-radius: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ff0000 !important;
        font-weight: bold;
    }}
    .stChatMessage {{
        background: linear-gradient(90deg, #2a0000 0%, #000000 100%) !important;
        border: 1px solid #ff0000 !important;
    }}
    .desc-box {{
        background-color: rgba(255, 0, 0, 0.1);
        border-left: 5px solid #ff0000;
        padding: 10px;
        margin-bottom: 20px;
        font-size: 14px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if "logado" not in st.session_state: st.session_state.logado = False
if "mensagens" not in st.session_state: st.session_state.mensagens = []
if "tedio_chat" not in st.session_state: st.session_state.tedio_chat = []
if "global_chat" not in st.session_state: st.session_state.global_chat = []

# --- TELA DE ACESSO ---
if not st.session_state.logado:
    if logo_mago:
        st.markdown(f'<center><img src="data:image/png;base64,{logo_mago}" width="200"></center>', unsafe_allow_html=True)
    st.markdown('<div class="text-3d-giant">MELHOR IA DE<br>GERAR SCRIPT</div>', unsafe_allow_html=True)
    
    aba_login, aba_cadastro = st.tabs(["ENTRAR", "CRIAR CONTA"])
    with aba_login:
        u = st.text_input("Usuario", key="user_login")
        p = st.text_input("Senha", type="password", key="pass_login")
        if st.button("INJETAR ACESSO"):
            if u: st.session_state.user = u; st.session_state.logado = True; st.rerun()
    with aba_cadastro:
        st.text_input("Novo Usuario")
        st.button("CADASTRAR")
else:
    # --- ABAS COM DESCRICAO ---
    tab_script, tab_global, tab_tedio = st.tabs(["SCRIPT", "CHAT GLOBAL", "CHAT TEDIO"])

    # ABA SCRIPT
    with tab_script:
        st.markdown('<div class="desc-box">TERMINAL DE GERACAO: Digite o nome do jogo ou a funcao desejada para receber um codigo Rayfield funcional para dispositivos moveis.</div>', unsafe_allow_html=True)
        for m in st.session_state.mensagens:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        if prompt := st.chat_input("Solicite seu script...", key="input_script"):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                lua = f"local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()\n-- Codigo para {prompt}"
                res = f"SISTEMA:\n```lua\n{lua}\n```"
                st.markdown(res); st.session_state.mensagens.append({"role": "assistant", "content": res})

    # ABA CHAT GLOBAL
    with tab_global:
        st.markdown('<div class="desc-box">COMUNIDADE: Espaco para interacao em tempo real entre todos os usuarios conectados ao Pereira System.</div>', unsafe_allow_html=True)
        with st.container(height=300):
            for g in st.session_state.global_chat:
                st.markdown(f"**{g['u']}:** {g['t']}")
        with st.form("global_msg", clear_on_submit=True):
            txt = st.text_input("Mensagem")
            if st.form_submit_button("ENVIAR"):
                if txt: st.session_state.global_chat.append({"u": st.session_state.user, "t": txt}); st.rerun()

    # ABA CHAT TEDIO
    with tab_tedio:
        st.markdown('<div class="desc-box">ENTRETENIMENTO: Chat sem filtros para piadas, conselhos, links externos e conversas aleatorias para passar o tempo.</div>', unsafe_allow_html=True)
        with st.container(height=350):
            for t in st.session_state.tedio_chat:
                with st.chat_message(t["role"]): st.markdown(t["content"])
        if tedio_prompt := st.chat_input("Conversar com a IA...", key="input_tedio"):
            st.session_state.tedio_chat.append({"role": "user", "content": tedio_prompt})
            with st.chat_message("assistant"):
                res_tedio = f"Resposta: {tedio_prompt} processado. O que mais deseja saber?"
                st.markdown(res_tedio); st.session_state.tedio_chat.append({"role": "assistant", "content": res_tedio})
