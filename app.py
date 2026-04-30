import asyncio
import streamlit as st
from typing import Dict, Any

# --- CONFIGURAÇÃO DA IA ---
class RealTimeAI:
    async def process_request(self, query: str) -> str:
        # Simula o processamento da IA
        await asyncio.sleep(0.8) 
        return f"Eu processei sua pergunta: '{query}'"

@st.cache_resource
def get_ai_instance():
    return RealTimeAI()

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Chat AI", page_icon="🤖")
st.title("🤖 Meu Assistente Real-Time")

ai = get_ai_instance()

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens salvas no histórico (para não sumirem ao recarregar)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Como posso ajudar?"):
    # 1. Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gera a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            # Rodando o método assíncrono dentro do fluxo do Streamlit
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response_data = loop.run_until_complete(ai.process_request(prompt))
            
            st.markdown(response_data)
            
    # 3. Salva a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": response_data})
