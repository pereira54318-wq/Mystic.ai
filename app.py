import asyncio
import streamlit as st
import json
from typing import Dict, Any

class RealTimeAI:
    def __init__(self):
        self.model = None 
        
    async def process_request(self, request_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Simula delay de processamento
            await asyncio.sleep(0.5)
            query = payload.get("query", "")
            return {
                "request_id": request_id,
                "status": "success",
                "response": f"Processado: {query}"
            }
        except Exception as e:
            return {"request_id": request_id, "status": "error", "error": str(e)}

# 1. Cache para evitar que a classe seja reiniciada a cada clique
@st.cache_resource
def get_ai_instance():
    return RealTimeAI()

async def run_tasks(ai, num_requests):
    tasks = []
    for i in range(num_requests):
        task = ai.process_request(f"req_{i}", {"query": f"Pergunta {i}"})
        tasks.append(task)
    # gather funciona normalmente dentro de uma função async chamada corretamente
    return await asyncio.gather(*tasks)

# Interface Streamlit
st.title("IA Real-Time com Asyncio")

ai = get_ai_instance()

if st.button("Executar 10 Requisições"):
    with st.spinner("Processando assincronamente..."):
        # 2. A forma correta de rodar async no Streamlit moderno:
        results = asyncio.run(run_tasks(ai, 10))
        
        st.success("Concluído!")
        st.json(results)
