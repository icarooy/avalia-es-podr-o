from database import conectar

def excluir_avaliacao(id_avaliacao):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM avaliacoes WHERE id = ?", (id_avaliacao,))
    con.commit()
    con.close()
    print(f"Avaliação com ID {id_avaliacao} excluída com sucesso ✅.")

if __name__ == "__main__":

    excluir_avaliacao(1)
