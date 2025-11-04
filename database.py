import sqlite3

# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect("podrao.db")

# Criar a tabela caso não exista
def criar_tabela():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_comida TEXT NOT NULL,
            nota REAL NOT NULL
        )
    """)
    con.commit()
    con.close()

# Inserir uma nova avaliação
def inserir_avaliacao(nome_comida, nota: float):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO avaliacoes (nome_comida, nota) VALUES (?, ?)", (nome_comida, nota))
    con.commit()
    con.close()

# Listar todas as avaliações
def listar_avaliacoes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM avaliacoes")
    dados = cur.fetchall()
    con.close()
    return dados

# Remover uma avaliação pelo ID
def remover_avaliacao(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM avaliacoes WHERE id = ?", (id,))
    con.commit()
    con.close()
