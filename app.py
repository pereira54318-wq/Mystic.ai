import streamlit as st
import time
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MYSTIC AI 👺", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILO CYBER HACK VERMELHO (UI/UX) ---
st.markdown("""
    <style>
    .stApp {
        background: #050000;
        background-image: radial-gradient(#ff0000 0.8px, transparent 0.8px);
        background-size: 30px 30px;
        color: #ff0000;
    }
    .stChatMessage { background-color: rgba(20, 0, 0, 0.8) !important; border: 1px solid #ff0000 !important; border-radius: 15px; }
    .profile-card { border: 2px solid #ff0000; padding: 20px; border-radius: 15px; background: rgba(30, 0, 0, 0.9); box-shadow: 0 0 20px #ff0000; }
    .stButton>button { background-color: #ff0000; color: white; border-radius: 10px; width: 100%; border: none; }
    .stTextInput input { background-color: #1a0000; color: #ff4444; border: 1px solid #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SESSÃO E LOGIN ---
if "logado" not in st.session_state: st.session_state.logado = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "User", "email": "", "foto": None}
if "contas_vinculadas" not in st.session_state: st.session_state.contas_vinculadas = []

def tela_login():
    st.markdown("<h1 style='text-align: center;'>👺 MYSTIC ACCESS</h1>", unsafe_allow_html=True)
    menu = ["Login", "Criar Conta"]
    escolha = st.selectbox("Selecione", menu)

    if escolha == "Criar Conta":
        new_user = st.text_input("Usuário")
        new_email = st.text_input("Gmail")
        new_pw = st.text_input("Senha", type='password')
        new_pw2 = st.text_input("Confirme a Senha", type='password')
        
        if st.button("Enviar Código para Gmail"):
            if new_pw == new_pw2 and new_email:
                st.success(f"Código enviado para {new_email} (Simulação)")
                cod = st.text_input("Digite o código recebido")
                if st.button("Confirmar Registro"):
                    st.session_state.user_data["nome"] = new_user
                    st.session_state.user_data["email"] = new_email
                    st.success("Conta Criada!")
            else: st.error("Senhas não coincidem")

    else:
        user = st.text_input("Usuário / Gmail")
        pw = st.text_input("Senha", type='password')
        if st.button("Entrar"):
            st.session_state.logado = True
            st.rerun()

# --- INTERFACE PRINCIPAL ---
if not st.session_state.logado:
    tela_login()
else:
    # Sidebar com infos de tempo real
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_data['nome']}")
        st.write(f"📅 Data: {datetime.date.today()}")
        st.write(f"⏰ Hora: {datetime.datetime.now().strftime('%H:%M:%S')}")
        st.write("🔋 Bateria: 85% (Simulado via Browser)")
        st.write("📱 Modelo: Motorola G35 Detected")
        if st.button("Sair"): 
            st.session_state.logado = False
            st.rerun()

    tab_chat, tab_image, tab_perfil = st.tabs(["💬 CHAT AI", "🎨 NANO BANANA", "👤 PERFIL"])

    with tab_chat:
        st.markdown("### 👺 Terminal de Scripts Online")
        if "messages" not in st.session_state: st.session_state.messages = []

        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if p := st.chat_input("Peça um script..."):
            st.session_state.messages.append({"role": "user", "content": p})
            with st.chat_message("assistant"):
                res_area = st.empty()
                code_final = f"-- [MYSTIC GENERATED]\n-- Script: {p}\nprint('Ativando {p}...')\nloadstring(game:HttpGet('https://api.mystic.ai/v2'))()"
                
                # Efeito de digitação tempo real
                full_txt = f"Gerando código para **{p}**:\n\n```lua\n{code_final}\n```"
                displayed = ""
                for c in full_txt:
                    displayed += c
                    res_area.markdown(displayed + "█")
                    time.sleep(0.005)
                res_area.markdown(full_txt)
                st.session_state.messages.append({"role": "assistant", "content": full_txt})

    with tab_image:
        st.subheader("🎨 NanoBanana Image Generator")
        desc_img = st.text_input("Descreva a imagem que deseja criar...")
        if st.button("Gerar Foto"):
            with st.spinner("IA processando imagem..."):
                time.sleep(3)
                st.image("https://placehold.co/600x400/200000/ff0000?text=NanoBanana+AI+Image", caption="Imagem Gerada pela NanoBanana")

    with tab_perfil:
        st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
        st.header("Seu Perfil")
        
        # Mudar foto da galeria
        img_file = st.file_uploader("Trocar Foto de Perfil", type=['png', 'jpg'])
        if img_file:
            st.session_state.user_data["foto"] = img_file
            st.image(img_file, width=150)
        
        st.write(f"**Nome:** {st.session_state.user_data['nome']}")
        st.write(f"**Email:** {st.session_state.user_data['email']}")
        
        st.markdown("---")
        st.subheader("Gerenciar Contas (Máx 5)")
        if len(st.session_state.contas_vinculadas) < 5:
            nova_conta = st.text_input("Adicionar Novo Usuário")
            if st.button("Vincular"):
                st.session_state.contas_vinculadas.append(nova_conta)
        
        for conta in st.session_state.contas_vinculadas:
            st.code(f"Conta Ativa: {conta}")
        st.markdown("</div>", unsafe_allow_html=True)
