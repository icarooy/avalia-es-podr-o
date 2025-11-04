import sqlite3

con = sqlite3.connect("podrao.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_comida TEXT NOT NULL,
    nota REAL NOT NULL CHECK(nota BETWEEN 0 AND 10)
)
""")

con.commit()
con.close()
