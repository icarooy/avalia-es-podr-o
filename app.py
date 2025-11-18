import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Configurações gerais
criar_tabela()
st.set_page_config(page_title="Avaliações do Podrão", page_icon="🍔")

# 🎨 Estilo customizado inspirado no Burger King
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Orbitron:wght@400;700&display=swap');

[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(20, 10, 0, 0.85), rgba(20, 10, 0, 0.85)),
                      url("https://images.unsplash.com/photo-1586190848861-99aa4a171e90");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: #fff3d4;
}

[data-testid="stSidebar"] {
    background: rgba(24, 8, 2, 0.95) !important;
}

.block-container {
    background-color: rgba(0, 0, 0, 0.3) !important;
    border-radius: 12px;
    padding-top: 20px;
}

.title {
    text-align: center;
    font-family: 'Anton', sans-serif;
    font-size: 62px;
    font-weight: bold;
    letter-spacing: 3px;
    color: #ffcc00;
    text-shadow: 4px 4px 0px rgba(255, 0, 0, 0.5);
}

.card {
    background-color: rgba(255, 112, 67, 0.15);
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 12px;
    box-shadow: 5px 5px 20px rgba(255, 204, 0, 0.25);
    border: 1px solid rgba(255, 160, 0, 0.5);
    transition: transform 0.15s ease-in-out;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 6px 6px 25px rgba(255, 160, 0, 0.35);
}

.remove-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 24px;
    color: #ff6b6b;
    transition: scale 0.2s ease;
}

.remove-button:hover {
    transform: scale(1.3);
    color: red;
}

.success-anim {
    font-family: 'Orbitron', sans-serif;
    color: #00ff99;
    font-weight: bold;
    animation: fadeInOut 1.5s infinite ease;
}

@keyframes fadeInOut {
    0% { opacity: 0.15; }
    50% { opacity: 1; }
    100% { opacity: 0.15; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='title'>AVALIAÇÕES DO PODRÃO</h1>", unsafe_allow_html=True)

# Função para exibir avaliações
def mostrar_avaliacoes():
    st.subheader("📋 Avaliações cadastradas")
    avaliacoes = listar_avaliacoes()
    if not avaliacoes:
        st.info("Nenhuma avaliação cadastrada ainda.")
    else:
        for id, nome_comida, nota, avaliador in avaliacoes:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                    <div class='card'>
                        <h3 style='margin: 0; font-family: Anton, sans-serif;'>{nome_comida}</h3>
                        <p style='margin:0;'>Nota: <b>{nota:.1f}</b> ⭐</p>
                        <p style='margin:0;'>Avaliador: {avaliador}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"remover_{id}"):
                    remover_avaliacao(id)
                    st.warning(f"Avaliação de '{nome_comida}' removida!")
                    st.rerun()

# Sidebar
st.sidebar.title("🍔 Bem-vindo!")
st.sidebar.info("Avalie os itens do cardápio e veja o que já foi avaliado!")

# Cardápio
cardapio = ["🍚 Arroz", "🌱 Feijão", "🍝 Macarrão", "🍟 Batata frita", "🍔 Hambúrguer", "🍕 Pizza", "🧑 Alan"]

# Formulário de avaliação
with st.form("nova_avaliacao"):
    nome_avaliador = st.text_input("Seu nome (opcional)", placeholder="Anônimo")
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
                st.markdown(f"<div class='success-anim'>🔄 Avaliação atualizada! Nova média: {nova_media:.2f} ⭐</div>", unsafe_allow_html=True)
            else:
                inserir_avaliacao(nome, nota, nome_avaliador)
                st.markdown(f"<div class='success-anim'>✨ Avaliação registrada com sucesso!</div>", unsafe_allow_html=True)

# Mostrar avaliações
mostrar_avaliacoes()
