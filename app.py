import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Configurações gerais
criar_tabela()
st.set_page_config(page_title="Avaliações do Podrão", page_icon="🍔")

# 🎨 Estilo Burger King
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&display=swap');

/* Cor de fundo geral */
[data-testid="stAppViewContainer"] {
    background-color: #f8e8c8;
    color: #3e1f00;
    font-family: 'Bebas Neue', sans-serif;
}

/* Banner superior */
.banner {
    background-image: url('https://media.burgerking.fr/nfci/EU/FR/images/common/menu-bg.jpg');
    background-size: cover;
    background-position: center;
    height: 200px;
    border-radius: 0 0 25px 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 20px rgba(255, 0, 0, 0.5);
}

/* Título principal */
.title {
    text-align: center;
    font-size: 64px;
    font-family: 'Anton', sans-serif;
    color: #d62300;
    text-shadow: 3px 3px 0px #f6e372;
    margin-top: -140px;
    margin-bottom: 30px;
}

/* Cards de avaliação */
.card {
    background-color: #ffefcf;
    border-radius: 12px;
    padding: 15px;
    border: 2px solid #d62300;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 15px;
    transition: 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.22);
}

.remove-button {
    font-size: 22px;
    color: #d62300;
    background-color: transparent;
    border: none;
    cursor: pointer;
}

.remove-button:hover {
    transform: scale(1.3);
    color: #a00000;
}

/* Botões */
.stButton>button {
    background-color: #d62300;
    color: #fff;
    font-size: 16px;
    padding: 12px 20px;
    border-radius: 25px;
    border: none;
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 1px;
}

.stButton>button:hover {
    background-color: #b61f00;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #d62300 !important;
}

.stSidebar .css-1v3fvcr {
    color: white;
    font-size: 20px;
}

.stSidebar [data-testid="stHeader"] {
    display: none;
}

.success-anim {
    font-family: 'Bebas Neue', sans-serif;
    color: #1a8f3f;
    font-weight: bold;
    animation: fadeIn 1.8s infinite alternate;
}

@keyframes fadeIn {
    0% { opacity: 0.6; }
    100% { opacity: 1; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# Banner e título
st.markdown("<div class='banner'></div>", unsafe_allow_html=True)
st.markdown("<h1 class='title'>AVALIAÇÕES DO PODRÃO</h1>", unsafe_allow_html=True)

# Função para exibir avaliações
def mostrar_avaliacoes():
    st.subheader("📋 Avaliações realizadas")
    avaliacoes = listar_avaliacoes()
    if not avaliacoes:
        st.info("Nenhuma avaliação cadastrada!")
    else:
        for id, nome_comida, nota, avaliador in avaliacoes:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                    <div class='card'>
                        <h3 style='margin:0;font-family: Anton;'>{nome_comida}</h3>
                        <p style='margin:0;'>Nota: <b>{nota:.1f} ⭐</b></p>
                        <p style='margin:0;'>Avaliador: {avaliador}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"remover_{id}", help="Remover avaliação"):
                    remover_avaliacao(id)
                    st.warning(f"Avaliação do item '{nome_comida}' foi removida!", icon="⚠️")
                    st.rerun()

# Sidebar
st.sidebar.title("🍔 Bem-vindo ao Podrão")
st.sidebar.info("Avalie os lanches e veja o que o pessoal achou!")

# Cardápio
cardapio = ["🍚 Arroz", "🌱 Feijão", "🍝 Macarrão", "🍟 Batata Frita", "🍔 Hambúrguer", "🍕 Pizza", "🧑 Alan"]

# Formulário
with st.form("nova_avaliacao"):
    nome_avaliador = st.text_input("Seu nome (opcional):", placeholder="Anônimo")
    nome = st.radio("Escolha um item do cardápio:", cardapio)
    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)
    enviar = st.form_submit_button("Salvar Avaliação")

    if enviar:
        nome_avaliador = nome_avaliador.strip() or "Anônimo"
        if nota <= 0:
            st.warning("⚠️ Insira uma nota válida maior que 0.")
        else:
            avaliacoes = listar_avaliacoes()
            existentes = [av for av in avaliacoes if av[1] == nome and av[3] == nome_avaliador]
            if existentes:
                notas_previas = [av[2] for av in existentes]
                nova_media = (sum(notas_previas) + nota) / (len(notas_previas) + 1)
                for av in existentes:
                    remover_avaliacao(av[0])
                inserir_avaliacao(nome, nova_media, nome_avaliador)
                st.markdown(f"<div class='success-anim'>🔄 Média atualizada para {nova_media:.2f} ⭐</div>", unsafe_allow_html=True)
            else:
                inserir_avaliacao(nome, nota, nome_avaliador)
                st.markdown(f"<div class='success-anim'>✨ Avaliação salva com sucesso!</div>", unsafe_allow_html=True)

# Mostrar avaliações
mostrar_avaliacoes()
