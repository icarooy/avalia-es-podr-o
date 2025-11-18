import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

criar_tabela()

# 🎨 Estilo customizado com CSS
st.markdown(
    """
    <style>
    /* Fundo preto total */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #f5f5f5;
    }

    /* Título animado com desfoque */
    .titulo {
        text-align: center;
        color: #FFDD55;
        font-family: "Comic Sans MS", cursive;
        font-size: 50px;
        animation: pulse 2s infinite;
        backdrop-filter: blur(4px);
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 12px;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Card das avaliações com brilho pulsante e fundo desfocado */
    .card {
        background-color: rgba(17, 17, 17, 0.6);
        backdrop-filter: blur(6px);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.05);
        transition: transform 0.2s;
        color: #f5f5f5;
        animation: pulseCard 3s infinite;
    }

    @keyframes pulseCard {
        0% { box-shadow: 0 0 10px rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 20px rgba(255,255,255,0.3); }
        100% { box-shadow: 0 0 10px rgba(255,255,255,0.1); }
    }

    /* Botão de remover estilizado */
    .remove-button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        font-size: 24px;
        color: #ff4b4b;
        transition: transform 0.2s;
    }
    .remove-button:hover {
        transform: scale(1.3);
    }

    /* Sidebar escura */
    [data-testid="stSidebar"] {
        background-color: #000000;
        color: #f5f5f5;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Letreiro estilizado
st.markdown("<h1 class='titulo'>🍔 Avaliações do Podrão 🍟</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📌 Bem vindo!")
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
        col1, col2 = st.columns([5, 1])  # precisa estar dentro do for
        with col1:
            st.markdown(
                f"""
                <div class='card'>
                    <h3 style='margin:0;'>{nome_comida}</h3>
                    <p style='margin:0;'>Nota: <b>{nota}</b></p>
                    <p style='margin:0;'>Avaliador: {avaliador}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            if st.button("🗑️", key=f"remover_{id}"):
                remover_avaliacao(id)
                st.warning(f"Avaliação '{nome_comida}' removida!")
                st.rerun()

