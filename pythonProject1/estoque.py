from db import conectar
from datetime import datetime

def registrar_movimento(produto_id, tipo, quantidade, motivo):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("INSERT INTO movimentos (produto_id, tipo, quantidade, data, motivo) VALUES (?, ?, ?, ?, ?)",
                (produto_id, tipo, quantidade, datetime.now().isoformat(), motivo))

    if tipo == 'entrada':
        cur.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto_id))
    elif tipo == 'saida':
        cur.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))

    conn.commit()
    conn.close()

def verificar_estoque_baixo():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome, quantidade, estoque_minimo FROM produtos WHERE quantidade <= estoque_minimo")
    alertas = cur.fetchall()
    conn.close()
    return alertas

def registrar_venda(produto_id, quantidade):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO vendas (produto_id, quantidade, data) VALUES (?, ?, ?)",
                (produto_id, quantidade, datetime.now().isoformat()))
    conn.commit()
    conn.close()
