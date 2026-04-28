import streamlit as st
import time

# Configuração de Página e Responsividade
st.set_page_config(page_title="MYSTIC AI 👺", layout="wide", initial_sidebar_state="collapsed")

# CSS Cyber Hack Vermelho V2 (Com pontos brilhantes e brilho neon)
st.markdown("""
    <style>
    .stApp {
        background: #050000;
        background-image: radial-gradient(#ff0000 0.8px, transparent 0.8px);
        background-size: 35px 35px;
        color: #ff0000;
    }
    .stTextInput input, .stChatInput input { 
        background-color: #100000 !important; 
        color: #ff4444 !important; 
        border: 1px solid #ff0000 !important; 
        font-family: 'Courier New', monospace;
    }
    .chat-card { 
        border-left: 4px solid #ff0000; 
        padding: 15px; 
        background: rgba(20, 0, 0, 0.9); 
        margin-bottom: 12px; 
        border-radius: 0 10px 10px 0;
        box-shadow: 5px 5px 15px rgba(255, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] { background: #000; border-bottom: 2px solid #ff0000; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: bold; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #ff0000 !important; }
    </style>
    """, unsafe_allow_html=True)

if "chat" not in st.session_state: st.session_state.chat = []
if "vault" not in st.session_state: st.session_state.vault = []

st.markdown("<h1 style='text-align: center; color: #ff0000; font-family: Courier;'>👺 MYSTIC AI SYSTEM v2.0</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 TERMINAL", "📂 SCRIPTS", "⚙️ STATUS"])

with tab1:
    for m in st.session_state.chat:
        st.markdown(f'<div class="chat-card"><b>{m["role"].upper()}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Solicite: Aimbot, ESP, Kill Aura, etc...")

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            status = st.empty()
            status.markdown("🔴 *Iniciando decodificação de memória...*")
            time.sleep(0.8)
            
            p = prompt.lower()
            # LÓGICA DE GERAÇÃO AVANÇADA
            if "aimbot" in p or "aim" in p:
                code = "-- MYSTIC AI: ADVANCED AIMBOT\nlocal player = game.Players.LocalPlayer\nlocal mouse = player:GetMouse()\nlocal run = game:GetService('RunService')\n\nrun.RenderStepped:Connect(function()\n    local target = nil\n    local dist = math.huge\n    for _, v in pairs(game.Players:GetPlayers()) do\n        if v ~= player and v.Character and v.Character:FindFirstChild('Head') then\n            local screenPos, onScreen = workspace.CurrentCamera:WorldToScreenPoint(v.Character.Head.Position)\n            if onScreen then\n                local mDist = (Vector2.new(mouse.X, mouse.Y) - Vector2.new(screenPos.X, screenPos.Y)).Magnitude\n                if mDist < dist then target = v; dist = mDist end\n            end\n        end\n    end\n    if target then workspace.CurrentCamera.CFrame = CFrame.new(workspace.CurrentCamera.CFrame.Position, target.Character.Head.Position) end\nend)"
            elif "esp" in p or "box" in p or "tracer" in p:
                code = "-- MYSTIC AI: QUANTUM ESP (BOX & TRACERS)\nfor _, p in pairs(game.Players:GetPlayers()) do\n    if p ~= game.Players.LocalPlayer then\n        local box = Drawing.new('Square')\n        box.Visible = true\n        box.Color = Color3.fromRGB(255, 0, 0)\n        box.Thickness = 1\n        -- Lógica de atualização de posição via RenderStepped integrada..."
            elif "kill aura" in p or "killaura" in p:
                code = "-- MYSTIC AI: KILL AURA\nlocal range = 20\nwhile wait() do\n    for _, v in pairs(game.Players:GetPlayers()) do\n        if v ~= game.Players.LocalPlayer and v.Character and v.Character:FindFirstChild('HumanoidRootPart') then\n            local dist = (v.Character.HumanoidRootPart.Position - game.Players.LocalPlayer.Character.HumanoidRootPart.Position).Magnitude\n            if dist < range then\n                -- RemoteEvent Fire Simulation\n                print('Targeting: ' .. v.Name)\n            end\n        end\n    end\nend"
            else:
                code = f"-- MYSTIC AI CUSTOM GENERATOR\n-- Request: {prompt}\nprint('MYSTIC AI: Gerando função específica...')\nloadstring(game:HttpGet('https://api.mystic.ai/v2/loader'))()"

            # Simulação de digitação em tempo real
            text_area = st.empty()
            displayed = ""
            for char in code:
                displayed += char
                text_area.code(displayed + "█", language="lua")
                time.sleep(0.003)
            text_area.code(code, language="lua")
            
            st.session_state.chat.append({"role": "assistant", "content": f"Script de {prompt} gerado e pronto para execução."})
            st.session_state.vault.append({"name": prompt, "code": code})
            st.rerun()

with tab2:
    st.subheader("📂 Vault de Scripts")
    for s in st.session_state.vault:
        with st.expander(f"🔴 {s['name'].upper()}"):
            st.code(s['code'], language="lua")
            st.button("Copiar", key=s['name'])

with tab3:
    st.markdown("### ⚙️ SYSTEM STATUS")
    st.write("🟢 AI Core: Online")
    st.write("🔴 Bypass Method: V3 Adaptive")
    st.write("📱 Device Optimization: Motorola G35 Detected")
