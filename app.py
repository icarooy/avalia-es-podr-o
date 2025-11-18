import streamlit as st
from streamlit_lottie import st_lottie
import requests
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Função para carregar animação Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

criar_tabela()

# 🎨 Título animado
st.markdown("<h1 style='text-align:center; color:#FF5733;'>🍔 Avaliações do Podrão 🍟</h1>", unsafe_allow_html=True)

# 🔥 Carregar animação Lottie (hambúrguer divertido)
lottie_burger = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_1pxqjqps.json")
st_lottie(lottie_burger, height=200, key="burger")

# Sidebar
st.sidebar.title("📌 Menu")
st.sidebar.info("Aqui você pode avaliar os pratos do cardápio e ver quem já avaliou!")

# Cardápio fixo com emojis
cardapio = [
    "🍚 Arroz",
    "🌱 Feijão",
    "🍝 Macarrão",
    "🍟 Batata frita",
    "🍔 Hambúrguer",
    "🍕 Pizza",
    "🧑 Alan"
]

# Formulário para inserir avaliação
with st.form("nova_avaliacao"):
    nome_avaliador = st.text_input("Seu nome (ou deixe em branco para ser anônimo)")
    nome = st.selectbox("Escolha um item do cardápio", cardapio)
    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)
    enviar = st.form_submit_button("Salvar")
    if enviar:
        if nota > 0:
            if nome_avaliador.strip() == "":
                nome_avaliador = "Anônimo"
            inserir_avaliacao(nome, nota, nome_avaliador)
            st.success(f"Avaliação de '{nome}' por {nome_avaliador} salva com sucesso!")
        else:
            st.warning("⚠️ Por favor, insira uma nota maior que 0 para salvar.")

st.subheader("📋 Avaliações já feitas")

avaliacoes = listar_avaliacoes()
if not avaliacoes:
    st.info("Nenhuma avaliação cadastrada ainda.")
else:
    for id, nome_comida, nota, avaliador in avaliacoes:
        st.markdown(
            f"""
            <div style='background-color:#fff; padding:15px; border-radius:12px; margin-bottom:12px;
                        box-shadow:2px 2px 8px rgba(0,0,0,0.1); transition:transform 0.2s;'>
                <h3 style='margin:0;'>{nome_comida}</h3>
                <p style='margin:0;'>Nota: <b>{nota}</b></p>
                <p style='margin:0;'>Avaliador: {avaliador}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Remover", key=f"remover_{id}"):
            remover_avaliacao(id)
            st.warning(f"Avaliação '{nome_comida}' removida!")
            st.rerun()