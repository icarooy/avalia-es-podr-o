from database import conectar

def atualizar_avaliacao(id_avaliacao, nova_nota):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE avaliacoes SET nota = ? WHERE id = ?", (nova_nota, id_avaliacao))
    con.commit()
    con.close()
    print(f"✅ Avaliação com ID {id_avaliacao} atualizada para nota {nova_nota}!")

if __name__ == "__main__":
    atualizar_avaliacao(2, 9.5)  
