import streamlit as st
from database import criar_tabela, inserir_avaliacao, listar_avaliacoes, remover_avaliacao

# Garante que a tabela exista
criar_tabela()

st.title("🍔 Avaliações do Podrão")

# Formulário para inserir avaliação
with st.form("nova_avaliacao"):
    nome = st.text_input("Nome da comida")
    nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)
    enviar = st.form_submit_button("Salvar")
    if enviar:
        if nome.strip() != "":
            inserir_avaliacao(nome, nota)
            st.success(f"Avaliação de '{nome}' salva com sucesso!")
        else:
            st.error("Digite o nome da comida antes de salvar.")

st.subheader("📋 Avaliações já feitas")

avaliacoes = listar_avaliacoes()
if not avaliacoes:
    st.info("Nenhuma avaliação cadastrada ainda.")
else:
    for id, nome_comida, nota in avaliacoes:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{nome_comida}**")
        with col2:
            st.write(f"Nota: {nota}")
        with col3:
            if st.button("Remover", key=f"remover_{id}"):
                remover_avaliacao(id)
                st.warning(f"Avaliação '{nome_comida}' removida!")
                st.rerun()

