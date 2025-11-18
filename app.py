import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Configurações e tabelas
criar_tabela()
st.set_page_config(page_title="Avaliações do Podrão", page_icon="🍔")

# 🎨 Tema Cyberpunk
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

/* Fundo cyberpunk com overlay escuro */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(15, 0, 35, 0.85), rgba(0, 0, 0, 0.9)),
                      url("https://images.unsplash.com/photo-1508804185872-f9cf40e475b4");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: #e0e0ff;
    font-family: 'Orbitron', sans-serif;
}

/* Sidebar futurista */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(10, 0, 40, 0.95), rgba(44, 0, 100, 0.85));
    color: #c3b5ff;
    border-right: 2px solid #8800ff;
}

/* Remove fundo branco */
.block-container {
    background-color: transparent !important;
}

/* Título neon */
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    text-shadow: 0px 0px 15px #ff00f7, 0px 0px 25px #f700ff;
    color: #ff00f7;
    letter-spacing: 2px;
}

/* Cards neon */
.card {
    background-color: rgba(12, 12, 30, 0.85);
    border: 2px solid #ff00f7;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    box-shadow: 0px 0px 20px rgba(255, 0, 241, 0.3);
    transition: transform 0.2s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 35px rgba(255, 0, 241, 0.6);
}

/* Select e input neon */
input, select, textarea, [role="radiogroup"] {
    background-color: rgba(20, 20, 40, 0.8) !important;
    color: #e0e0ff !important;
    border: 1px solid #bb00ff !important;
    box-shadow: 0px 0px 10px #bb00ff;
    border-radius: 5px;
}

/* Botão remover neon */
.remove-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: #ff006f;
    font-size: 22px;
    text-shadow: 0px 0px 8px #ff4bdf;
    transition: transform 0.2s ease;
}
.remove-button:hover {
    transform: scale(1.2) rotate(-5deg);
}

/* Animação de sucesso */
.success-anim {
    color: #00eaff;
    font-weight: bold;
    text-shadow: 0px 0px 10px #00eaff, 0px 0px 30px #00caff;
    animation: glow 1.2s infinite alternate ease-in-out;
}
@keyframes glow {
    0% { text-shadow: 0px 0px 5px #00eaff; opacity: 0.7; }
    100% { text-shadow: 0px 0px 20px #00eaff; opacity: 1; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Título
st.markdown("<h1 class='title'>⚡ Avaliações do Podrão ⚡</h1>", unsafe_allow_html=True)

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
st.sidebar.title("📌 Bem vindo!")
st.sidebar.info("Avalie os pratos do cardápio e veja quem já deu sua opinião!")

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
                st.markdown(f"<div class='success-anim'>🔄 Média atualizada: {nova_media:.2f} ⭐ ({nome_avaliador})</div>", unsafe_allow_html=True)
            else:
                inserir_avaliacao(nome, nota, nome_avaliador)
                st.markdown(f"<div class='success-anim'>✨ Avaliação de '{nome}' registrada por {nome_avaliador}!</div>", unsafe_allow_html=True)

# Mostrar avaliações
mostrar_avaliacoes()

