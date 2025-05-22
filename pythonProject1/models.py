from db import conectar

def adicionar_produto():
    nome = input("Nome: ")
    codigo = input("Código: ")
    descricao = input("Descrição: ")
    categoria = input("Categoria: ")
    fornecedor = input("Fornecedor: ")
    preco_compra = float(input("Preço de compra: "))
    preco_venda = float(input("Preço de venda: "))
    quantidade = int(input("Quantidade inicial: "))
    estoque_minimo = int(input("Estoque mínimo: "))

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO produtos (nome, codigo, descricao, categoria, fornecedor, preco_compra, preco_venda, quantidade, estoque_minimo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (nome, codigo, descricao, categoria, fornecedor, preco_compra, preco_venda, quantidade, estoque_minimo))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, quantidade FROM produtos")
    for row in cur.fetchall():
        print(row)
    conn.close()

def listar_vendas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT produto_id, quantidade, data FROM vendas")
    for row in cur.fetchall():
        print(row)
    conn.close()

def login_existe(login_usuario):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM usuarios WHERE login = ?", (login_usuario,))
    existe = cur.fetchone() is not None
    conn.close()
    return existe

def cadastrar_usuario_no_banco(nome, login_usuario, senha, nivel):
    if login_existe(login_usuario):
        raise RuntimeError(f"Login '{login_usuario}' já está em uso.")
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO usuarios (nome, login, senha, nivel)
            VALUES (?, ?, ?, ?)
        """, (nome, login_usuario, senha, nivel))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        conn.rollback()
        raise RuntimeError(f"Erro ao cadastrar usuário no banco: {e}")
    finally:
        conn.close()
