import streamlit as st
from database import inserir_avaliacao, listar_avaliacoes

st.set_page_config(page_title="The Podrão - Avaliações", layout="centered")
st.title("The Podrão 🍔 - Avalie sua comida!")

st.subheader("Deixe sua nota:")
nome_comida = st.text_input("Nome da comida")
nota = st.slider("Nota (0 a 10)", 0.0, 10.0, step=0.1)  

if st.button("Enviar avaliação"):
    if nome_comida:
        inserir_avaliacao(nome_comida, float(nota))
        st.success(f"Avaliação registrada para '{nome_comida}' com nota {nota:.1f}")
    else:
        st.error("Por favor, insira o nome da comida.")

st.subheader("📋 Avaliações registradas")
avaliacoes = listar_avaliacoes()
if avaliacoes:
    for id, comida, nota in avaliacoes:
        st.write(f"🍽️ {comida} — Nota: {nota:.1f}/10")
else:
    st.info("Nenhuma avaliação registrada ainda.")
