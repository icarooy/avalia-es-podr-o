import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Configuração inicial
criar_tabela()
st.set_page_config(page_title="Avaliações do Podrão", page_icon="🍔", layout="wide")

# CSS estilo BK
CSS = """
<style>
/* Importando fontes */
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Roboto:wght@400;700&display=swap');

/* Estilo do app */
[data-testid="stAppViewContainer"] {
    background-color: #faf4e6;
    background-image: url('https://media.burgerking.fr/nfci/EU/FR/images/common/menu-bg.jpg');
    background-size: cover;
    background-position: center;
    color: #3a1f05;
    font-family: 'Roboto', sans-serif;
}

/* Banner no topo */
.banner {
    background-image: url('https://static.burgerking.com.br/images/whopper_web_home.png');
    background-size: contain;
    background-repeat: no-repeat;
    height: 200px;
    margin-bottom: 20px;
}

/* Título estilo BK */
.title {
    font-family: 'Anton', sans-serif;
    font-size: 58px;
    letter-spacing: 2px;
    text-align: center;
    color: #e21a27;
    text-shadow: 3px 3px 0px #ffcc00;
    margin-bottom: 10px;
}

/* Card das avaliações */
.card {
    background-color: #fff5e6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    border: 3px solid #5e3b1f;
    box-shadow: 3px 3px 0px #ffcc00;
}

.card h3 {
    font-family: 'Anton';
    font-size: 24px;
    color: #5e3b1f;
    margin-bottom: 5px;
}

/* Botões personalizados */
.stButton>button {
    background-color: #e21a27;
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 40px;
    border: none;
    cursor: pointer;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #5e3b1f;
}

.remove-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 22px;
    color: #e21a27;
    transition: transform 0.2s;
}

.remove-button:hover {
    transform: scale(1.2);
    color: #5e3b1f;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #5e3b1f !important;
    color: #fff;
}

.stSidebar [data-testid="stHeader"] {
    display: none;
}

.stSidebar h1, .stSidebar h2 {
    color: #ffcc00;
}

/* Inputs */
div[data-testid="stTextInput"] input {
    border: 2px solid #5e3b1f;
}

[data-testid="stRadio"] label {
    font-weight: bold;
    color: #5e3b1f;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Banner
st.markdown("<div class='banner'></div>", unsafe_allow_html=True)

# Título
st.markdown("<div class='title'>Avaliações do Podrão 🍔</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🍟 Faça sua avaliação!")
st.sidebar.info("Selecione um prato e deixe sua nota sobre ele!")

# Cardápio
cardapio = ["🍚 Arroz", "🌱 Feijão", "🍝 Macarrão", "🍟 Batata frita", "🍔 Hambúrguer", "🍕 Pizza", "🧑 Alan"]

# Formulário
with st.form("nova_avaliacao"):
    nome_avaliador = st.text_input("Seu nome (opcional)")
    nome = st.radio("Escolha um item do cardápio", cardapio)
    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)
    enviar = st.form_submit_button("Salvar avaliação")

    if enviar:
        nome_avaliador = nome_avaliador.strip() if nome_avaliador.strip() else "Anônimo"
        if nota <= 0:
            st.warning("⚠️ Por favor, insira uma nota maior que 0.")
        else:
            avaliacoes = listar_avaliacoes()
            existentes = [av for av in avaliacoes if av[1] == nome and av[3] == nome_avaliador]
            
            if existentes:
                notas_previas = [av[2] for av in existentes]
                nova_media = (sum(notas_previas) + nota) / (len(notas_previas) + 1)
                for av in existentes:
                    remover_avaliacao(av[0])

                inserir_avaliacao(nome, nova_media, nome_avaliador)
                st.success(f"🔄 Média atualizada para {nova_media:.2f} ⭐ por {nome_avaliador}")
            else:
                inserir_avaliacao(nome, nota, nome_avaliador)
                st.success(f"✨ Avaliação registrada com sucesso por {nome_avaliador}!")

# Listar avaliações
st.subheader("📋 Avaliações já feitas")

avaliacoes = listar_avaliacoes()
if not avaliacoes:
    st.info("Nenhuma avaliação cadastrada ainda.")
else:
    for id, nome_comida, nota, avaliador in avaliacoes:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
                <div class='card'>
                    <h3>{nome_comida}</h3>
                    <p><b>Nota:</b> {nota:.1f} ⭐</p>
                    <p><b>Avaliador:</b> {avaliador}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"remover_{id}", help="Remover avaliação",):
                remover_avaliacao(id)
                st.warning(f"Avaliação de '{nome_comida}' removida!")
                st.rerun()
