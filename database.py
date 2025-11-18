import sqlite3

# Criar tabela com campo avaliador
def criar_tabela():
    conn = sqlite3.connect("avaliacoes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comida TEXT NOT NULL,
            nota REAL NOT NULL,
            avaliador TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Inserir avaliação com avaliador
def inserir_avaliacao(comida, nota, avaliador):
    conn = sqlite3.connect("avaliacoes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO avaliacoes (comida, nota, avaliador) VALUES (?, ?, ?)",
                   (comida, nota, avaliador))
    conn.commit()
    conn.close()

# Listar avaliações (inclui avaliador)
def listar_avaliacoes():
    conn = sqlite3.connect("avaliacoes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, comida, nota, avaliador FROM avaliacoes")
    avaliacoes = cursor.fetchall()
    conn.close()
    return avaliacoes

# Remover avaliação
def remover_avaliacao(id):
    conn = sqlite3.connect("avaliacoes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM avaliacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
