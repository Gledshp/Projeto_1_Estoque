import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        codigo TEXT UNIQUE,
        descricao TEXT,
        categoria TEXT,
        fornecedor TEXT,
        preco_compra REAL,
        preco_venda REAL,
        quantidade INTEGER,
        estoque_minimo INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimentos (
        id INTEGER PRIMARY KEY,
        produto_id INTEGER,
        tipo TEXT,
        quantidade INTEGER,
        data TEXT,
        motivo TEXT,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        login TEXT UNIQUE,
        senha TEXT,
        nivel TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY,
        produto_id INTEGER,
        quantidade INTEGER,
        data TEXT,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    conn.commit()
    conn.close()
