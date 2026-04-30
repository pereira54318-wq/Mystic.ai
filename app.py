import asyncio
import streamlit as st
import random

# --- LOGICA DA IA ---
class ModernAI:
    def __init__(self):
        self.name = "Gemini-Style Bot"

    async def generate_response(self, query: str):
        """Simula uma resposta fluida com delay estilo streaming"""
        # Aqui você substituiria pela chamada real da API do Gemini
        responses = [
            f"Analisando sua pergunta sobre '{query}'...",
            "Com base nos dados atuais, posso dizer que...",
            "Essa é uma questão interessante. Aqui está o que encontrei:"
        ]
        base_text = random.choice(responses) + "\n\n"
        full_response = base_text + "Este é um exemplo de resposta estruturada em **Markdown**.\n\n* Ponto 1: Agilidade\n* Ponto 2: Inteligência\n\nComo posso ajudar mais?"
        
        # Simulando o efeito de 'digitação'
        current_text = ""
        for word in full_response.split(" "):
            current_text += word + " "
            yield current_text
            await asyncio.sleep(0.05)

# --- INTERFACE MODERNA ---
st.set_page_config(page_title="Gemini Clone", page_icon="✨", layout="centered")

# Estilo CSS para esconder o menu chato e deixar mais limpo
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Gemini Pro Simulator")
st.caption("Modelo de IA assíncrono com streaming de alta performance")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte algo..."):
    # Adiciona pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        placeholder = st.empty() # Para o efeito de streaming
        ai = ModernAI()
        
        # Corrigindo o erro de loop: Usando uma função auxiliar para rodar o gerador
        async def run_ai():
            full_res = ""
            async for chunk in ai.generate_response(prompt):
                full_res = chunk
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            return full_res

        # Execução segura para Streamlit Cloud
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            final_response = loop.run_until_complete(run_ai())
            loop.close()
            
            st.session_state.messages.append({"role": "assistant", "content": final_response})
        except Exception as e:
            st.error(f"Erro de processamento: {e}")
