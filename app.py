import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Meu Gemini Clone", page_icon="🤖")
st.title("🤖 Gemini Clone")

# Configurar a API
genai.configure(api_key="AIzaSyD31Z7baF6-rjvl5BoLMtJTttoyuYOqNTg") # <--- COLE SUA CHAVE AQUI
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicializar o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Como posso te ajudar hoje?"):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta da IA
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Enviar histórico completo para manter o contexto
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(prompt)
        full_response = response.text
        placeholder.markdown(full_response)
    
    # Adicionar resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
