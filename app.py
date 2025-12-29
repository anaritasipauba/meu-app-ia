import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Minha IA", page_icon="🤖")

st.title("🤖 Minha IA Personalizada")
st.write("Diga oi para começar!")

# --- SEGREDO DA CHAVE (NÃO MEXA AQUI) ---
# A chave será puxada do site de hospedagem para segurança
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Chave de API não encontrada. Configure nos 'Secrets' do Streamlit.")
    st.stop()

# --- SUAS REGRAS (O CÉREBRO DA IA) ---
# Cole aqui o texto que você fez no Google AI Studio (antigo)
INSTRUCAO_SISTEMA = """
Atue como o CosturaAI, um consultor sênior e engenheiro de software especializado no ERP 3VEZES7 para facções de costura, adotando um tom profissional, resolutivo e amigável que entende profundamente as etapas de produção (corte, costura, acabamento) e as necessidades de gestão (estoque de tecidos, financeiro e clientes). Suas respostas devem ser concisas, focadas em soluções práticas, e suas atualizações de código devem priorizar uma estética impecável (UI/UX), funcionalidade minimalista e conformidade técnica rigorosa, garantindo que o sistema seja offline-first, acessível e responsivo. Utilize exclusivamente os modelos gemini-3-flash-preview para tarefas gerais e gemini-3-pro-preview para raciocínio complexo, operando sempre com a chave process.env.API_KEY sem jamais solicitá-la ao usuário, e mantenha a integridade da lógica de pedidos multi-itens, anexos técnicos em base64 e gestão dinâmica de categorias. Todas as alterações de software devem seguir o formato XML especificado, respeitando a estrutura de arquivos atual e assegurando que a Ordem de Serviço (OS) e os painéis de controle ofereçam uma visão clara e profissional para o crescimento do negócio de confecção.

"""

# Configuração do Modelo
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=INSTRUCAO_SISTEMA)

# --- LÓGICA DO CHAT (HISTÓRICO) ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Mostra as mensagens antigas
for message in st.session_state.chat.history:
    role = "🤖" if message.role == "model" else "👤"
    st.write(f"**{role}**: {message.parts[0].text}")

# Campo de entrada do usuário
prompt = st.chat_input("Digite sua mensagem...")

if prompt:
    # Mostra o que o usuário digitou
    st.write(f"**👤**: {prompt}")
    
    # A IA pensa e responde
    try:
        response = st.session_state.chat.send_message(prompt)
        st.write(f"**🤖**: {response.text}")
    except Exception as e:
        st.error(f"Erro na IA: {e}")