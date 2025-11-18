import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Configurações e tabelas
criar_tabela()
st.set_page_config(page_title="Avaliações do Podrão", page_icon="🍔")

# 🎨 Estilo customizado
CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)),
                      url("https://images.pexels.com/photos/70497/pexels-photo-70497.jpeg");
	background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: #e6e6e6;
}

[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.9) !important;
}

.block-container {
    background-color: transparent !important;
}

.title {
    text-align: center;
    font-family: 'Helvetica Neue', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: #ffdd57;
}

.card {
    background-color: rgba(32, 32, 32, 0.92);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.8);
    transition: transform 0.2s ease;
}

.card:hover {
    transform: scale(1.02);
}

.remove-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 22px;
    color: #ff4b4b;
    transition: transform 0.2s;
}

.remove-button:hover {
    transform: scale(1.2);
}

.success-anim {
    color: #00ff88;
    font-weight: bold;
    animation: fadeInOut 1.2s ease;
}

@keyframes fadeInOut {
    0% { opacity: 0.2; }
    50% { opacity: 1; }
    100% { opacity: 0.2; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Título
st.markdown("<h1 class='title'>Avaliações do Podrão</h1>", unsafe_allow_html=True)

# Ops gerais
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
                        <h3 style='margin:0;'>{nome_comida}</h3>
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
st.sidebar.title("📌 Olá!")
st.sidebar.info("Avalie os pratos do cardápio e veja o que já foi avaliado!")

# Cardápio
cardapio = ["🍚 Arroz", "🌱 Feijão", "🍝 Macarrão", "🍟 Batata frita", "🍔 Hambúrguer", "🍕 Pizza", "🧑 Alan"]

# Formulário
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
                st.markdown(f"<div class='success-anim'>🔄 {nome_avaliador} já avaliou '{nome}'. Média atualizada: {nova_media:.2f} ⭐</div>", unsafe_allow_html=True)
            else:
                inserir_avaliacao(nome, nota, nome_avaliador)
                st.markdown(f"<div class='success-anim'>✨ Avaliação de '{nome}' registrada com sucesso por {nome_avaliador}!</div>", unsafe_allow_html=True)

# Mostrar avaliações
mostrar_avaliacoes()
