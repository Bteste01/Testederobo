import streamlit as st
from datetime import datetime

# =================================
# CONFIGURAÇÃO DA PÁGINA
# =================================
st.set_page_config(
    page_title="Chatbot Web Completo",
    page_icon="🤖",
    layout="centered"
)

# =================================
# INICIALIZAÇÃO DE MEMÓRIA
# =================================
if "registros" not in st.session_state:
    st.session_state.registros = []

# =================================
# NLP SIMPLES
# =================================
def detectar_servico(texto):
    texto = texto.lower()
    if "contrato" in texto:
        return "Contrato"
    if "agenda" in texto or "show" in texto:
        return "Agendamento"
    if "assessoria" in texto:
        return "Assessoria"
    return "Desconhecido"

# =================================
# FLUXO DO CHATBOT
# =================================
def fluxo(step, user_input, data):
    if step == 0:
        data["nome"] = user_input
        return 1, "Qual é a sua cidade?", data

    if step == 1:
        data["cidade"] = user_input
        return 2, "Qual serviço você deseja? (Contrato / Agendamento / Assessoria)", data

    if step == 2:
        servico = detectar_servico(user_input)
        data["servico"] = servico

        if servico == "Contrato":
            return 3, "Qual tipo de contrato? (Parceria / Assessoria / Agendamento)", data

        if servico == "Agendamento":
            return 4, "Qual a data do evento?", data

        if servico == "Assessoria":
            data["finalizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            return 99, "Assessoria registrada com sucesso ✅", data

        return 2, "Não entendi. Pode explicar melhor?", data

    if step == 3:
        data["tipo_contrato"] = user_input
        data["finalizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        return 99, "Contrato registrado com sucesso ✅", data

    if step == 4:
        data["data_evento"] = user_input
        data["finalizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        return 99, "Agendamento registrado com sucesso ✅", data

    return 99, "Atendimento finalizado. Obrigado! 🙌", data

# =================================
# MENU LATERAL
# =================================
menu = st.sidebar.selectbox("Menu", ["🤖 Chatbot", "📊 Área Administrativa"])

# =================================
# CHATBOT
# =================================
if menu == "🤖 Chatbot":
    st.title("🤖 Atendimento Automático")

    if "step" not in st.session_state:
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá 👋 Qual é o seu nome?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Digite aqui...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        step, resposta, dados = fluxo(
            st.session_state.step,
            user_input,
            st.session_state.data
        )

        st.session_state.step = step
        st.session_state.data = dados

        st.session_state.messages.append(
            {"role": "assistant", "content": resposta}
        )
        st.chat_message("assistant").write(resposta)

        if step == 99:
            st.session_state.registros.append(dados)

# =================================
# ÁREA ADMINISTRATIVA
# =================================
if menu == "📊 Área Administrativa":
    st.title("📊 Área Administrativa")

    if not st.session_state.registros:
        st.info("Nenhum atendimento registrado nesta sessão.")
    else:
        st.json(st.session_state.registros)
