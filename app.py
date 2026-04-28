import streamlit as st
import time

# Configuração da Página
st.set_page_config(page_title="HACKER AI - ROBLOX", layout="wide")

# CSS Customizado para o Tema "Cyber Hack Vermelho"
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0000;
        color: #ff0000;
    }
    [data-testid="stSidebar"] {
        background-color: #1a0000;
        border-right: 2px solid #ff0000;
    }
    .stTextInput input {
        background-color: #220000;
        color: #ff4444;
        border: 1px solid #ff0000;
    }
    /* Estilo do Chat */
    .chat-bubble {
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ff0000;
        background: rgba(255, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Estados (Histórico e Scripts Salvos)
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "scripts_salvos" not in st.session_state:
    st.session_state.scripts_salvos = []

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🔴 SYSTEM BY PEREIRA")
    
    aba = st.radio("Navegação", ["💬 Chat AI", "📂 Histórico", "📜 Scripts Salvos"])
    
    st.markdown("---")
    st.info("Status: Online - Bypass Ativo")

# --- LÓGICA DAS ABAS ---
if aba == "💬 Chat AI":
    st.header("🤖 Roblox Script Generator")
    st.write("Digite o jogo ou a função que deseja (ex: Auto Farm Blox Fruits)")

    # Exibição do Chat em Tempo Real
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(f'<div class="chat-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input do Usuário
    prompt = st.chat_input("Comando para o terminal...")

    if prompt:
        # Adiciona pergunta ao histórico
        st.session_state.mensagens.append({"role": "user", "content": prompt})
        
        # Resposta simulando "IA Hacker"
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = f"-- [GERANDO SCRIPT PARA: {prompt.upper()}]\n\n"
            full_res += "loadstring(game:HttpGet('https://raw.githubusercontent.com/PereiraSystem/Main/main/loader.lua'))()"
            
            # Efeito de digitação em tempo real
            typed_res = ""
            for char in full_res:
                typed_res += char
                placeholder.markdown(typed_res + "█")
                time.sleep(0.01)
            placeholder.markdown(typed_res)
            
        st.session_state.mensagens.append({"role": "assistant", "content": full_res})
        
        # Botão para salvar script gerado
        if st.button("💾 Salvar este Script"):
            st.session_state.scripts_salvos.append(full_res)
            st.success("Script armazenado no banco de dados local.")

elif aba == "📂 Histórico":
    st.header("🕒 Logs de Conversa")
    for i, msg in enumerate(st.session_state.mensagens):
        st.text(f"[{i}] {msg['role']}: {msg['content'][:50]}...")

elif aba == "📜 Scripts Salvos":
    st.header("🔥 Seus Scripts")
    if not st.session_state.scripts_salvos:
        st.write("Nenhum script salvo ainda.")
    for idx, sc in enumerate(st.session_state.scripts_salvos):
        st.code(sc, language='lua')
        st.markdown("---")
      
