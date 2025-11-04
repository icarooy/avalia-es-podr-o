import sqlite3

def conectar():
    return sqlite3.connect("podrao.db")

def inserir_avaliacao(nome_comida, nota: float):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO avaliacoes (nome_comida, nota) VALUES (?, ?)", (nome_comida, nota))
    con.commit()
    con.close()

def listar_avaliacoes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM avaliacoes")
    dados = cur.fetchall()
    con.close()
    return dados
