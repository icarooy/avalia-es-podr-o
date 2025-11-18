import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

criar_tabela()

# 🎨 Estilo customizado com CSS
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(
            rgba(0,0,0,0.6),
            rgba(0,0,0,0.6)
        ),
        url("https://arkasnews.com/wp-content/uploads/2022/07/hamburger.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f5f5f5;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent; /* deixa o body aparecer */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎨 Estilo customizado com CSS
st.markdown(
    """
    <style>
    /* Título animado RGB */
    .titulo {
        text-align: center;
        font-family: "Comic Sans MS", cursive;
        font-size: 50px;
        font-weight: bold;
        background: linear-gradient(270deg, red, orange, yellow, green, cyan, blue, violet);
        background-size: 1400% 1400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rgbShift 8s ease infinite;
    }
    @keyframes rgbShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Card das avaliações */
    .card {
        background-color: rgba(17,17,17,0.85);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 2px 2px 12px rgba(255,255,255,0.05);
        transition: transform 0.2s;
        color: #f5f5f5;
    }
    .card:hover {
        transform: scale(1.01);
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
        transform: scale(1.2);
    }

    /* Selectbox animado */
    [data-testid="stSelectbox"] {
        animation: fadeIn 1s ease;
        transition: all 0.3s ease;
    }
    [data-testid="stSelectbox"] select:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Mensagem de sucesso animada */
    .success-anim {
        color: #00ff88;
        font-weight: bold;
        animation: popUp 0.5s ease;
    }
    @keyframes popUp {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Letreiro estilizado
st.markdown(
    "<h1><span>🍔</span> <span class='titulo'>Avaliações do Podrão</span> <span>🍟</span></h1>",
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("📌 Bem vindo!")
st.sidebar.info("Aqui você pode avaliar os pratos do cardápio e ver quem já avaliou!")

# Cardápio fixo
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
    nome = st.radio("Escolha um item do cardápio", cardapio)
    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)
    enviar = st.form_submit_button("Salvar")
    if enviar:
        if nota > 0:
            if nome_avaliador.strip() == "":
                nome_avaliador = "Anônimo"

            avaliacoes_existentes = listar_avaliacoes()
            avaliacoes_usuario = [
                av_nota for _, av_nome, av_nota, av_avaliador in avaliacoes_existentes
                if av_nome == nome and av_avaliador == nome_avaliador
            ]

            if avaliacoes_usuario:
                soma = sum(avaliacoes_usuario) + nota
                qtd = len(avaliacoes_usuario) + 1
                media = soma / qtd

                for id, av_nome, av_nota, av_avaliador in avaliacoes_existentes:
                    if av_nome == nome and av_avaliador == nome_avaliador:
                        remover_avaliacao(id)

                inserir_avaliacao(nome, media, nome_avaliador)
                st.markdown(
                    f"<div class='success-anim'>✅ {nome_avaliador} já avaliou '{nome}'. Média atualizada para {media:.2f} ⭐</div>",
                    unsafe_allow_html=True
                )
            else:
                inserir_avaliacao(nome, nota, nome_avaliador)
                st.markdown(
                    f"<div class='success-anim'>✅ Avaliação de '{nome}' por {nome_avaliador} salva com sucesso!</div>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("⚠️ Por favor, insira uma nota maior que 0 para salvar.")

st.subheader("📋 Avaliações já feitas")

avaliacoes = listar_avaliacoes()
if not avaliacoes:
    st.info("Nenhuma avaliação cadastrada ainda.")
else:
    for id, nome_comida, nota, avaliador in avaliacoes:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(
                f"""
                <div class='card'>
                    <h3 style='margin:0;'>{nome_comida}</h3>
                    <p style='margin:0;'>Nota: <b>{nota:.2f}</b></p>
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
