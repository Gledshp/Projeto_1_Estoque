import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db import criar_tabelas, conectar
from estoque import verificar_estoque_baixo, registrar_movimento, registrar_venda
from models import adicionar_produto, listar_produtos, cadastrar_usuario_no_banco

def validar_login_banco(usuario, senha):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT senha FROM usuarios WHERE login = ?", (usuario,))
    resultado = cur.fetchone()
    conn.close()
    if resultado is None:
        return False
    senha_armazenada = resultado[0]
    return senha == senha_armazenada

def login():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(login_window, text="Senha:").grid(row=1, column=0, padx=10, pady=10)

    user_entry = tk.Entry(login_window)
    user_entry.grid(row=0, column=1, padx=10, pady=10)

    pass_entry = tk.Entry(login_window, show="*")
    pass_entry.grid(row=1, column=1, padx=10, pady=10)

    def validate_login():
        usuario = user_entry.get()
        senha = pass_entry.get()
        if validar_login_banco(usuario, senha):
            login_window.destroy()
            menu()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas")

    def abrir_cadastro():
        login_window.destroy()
        cadastro_usuario()

    tk.Button(login_window, text="Login", command=validate_login).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(login_window, text="Cadastrar Novo Usuário", command=abrir_cadastro).grid(row=3, column=0, columnspan=2)

    login_window.mainloop()

def cadastro_usuario():
    cadastro_window = tk.Tk()
    cadastro_window.title("Cadastrar Usuário")
    cadastro_window.geometry("350x200")

    tk.Label(cadastro_window, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(cadastro_window, text="Login:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(cadastro_window, text="Senha:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(cadastro_window, text="Nível (admin/comum):").grid(row=3, column=0, padx=10, pady=5)

    nome_entry = tk.Entry(cadastro_window)
    nome_entry.grid(row=0, column=1, padx=10, pady=5)
    login_entry = tk.Entry(cadastro_window)
    login_entry.grid(row=1, column=1, padx=10, pady=5)
    senha_entry = tk.Entry(cadastro_window, show="*")
    senha_entry.grid(row=2, column=1, padx=10, pady=5)
    nivel_entry = tk.Entry(cadastro_window)
    nivel_entry.grid(row=3, column=1, padx=10, pady=5)

    def salvar_usuario():
        nome = nome_entry.get()
        login_usuario = login_entry.get()
        senha = senha_entry.get()
        nivel = nivel_entry.get()

        if not all([nome, login_usuario, senha, nivel]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
            return

        try:
            sucesso = cadastrar_usuario_no_banco(nome, login_usuario, senha, nivel)
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                cadastro_window.destroy()
                login()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar usuário no banco.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar usuário:\n{e}")

    tk.Button(cadastro_window, text="Salvar", command=salvar_usuario).grid(row=4, column=0, columnspan=2, pady=10)

    cadastro_window.mainloop()

def menu():
    root = tk.Tk()
    root.title("Controle de Estoque")
    root.geometry("300x300")

    tk.Label(root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Adicionar Produto", width=25, command=adicionar_produto_interface).pack(pady=5)
    tk.Button(root, text="Listar Produtos", width=25, command=listar_produtos_interface).pack(pady=5)
    tk.Button(root, text="Realizar Entrada de Estoque", width=25, command=realizar_entrada_interface).pack(pady=5)
    tk.Button(root, text="Realizar Saída de Estoque", width=25, command=realizar_saida_interface).pack(pady=5)
    tk.Button(root, text="Ver Alertas de Estoque Baixo", width=25, command=alertas_interface).pack(pady=5)
    tk.Button(root, text="Sair", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

def adicionar_produto_interface():
    window = tk.Toplevel()
    window.title("Adicionar Produto")
    window.geometry("400x400")

    labels = ["Nome", "Código", "Descrição", "Categoria", "Fornecedor", "Preço de compra", "Preço de venda", "Quantidade inicial", "Estoque mínimo"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(window, text=label + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def salvar():
        try:
            nome = entries[0].get()
            codigo = entries[1].get()
            descricao = entries[2].get()
            categoria = entries[3].get()
            fornecedor = entries[4].get()
            preco_compra = float(entries[5].get())
            preco_venda = float(entries[6].get())
            quantidade = int(entries[7].get())
            estoque_minimo = int(entries[8].get())

            if not all([nome, codigo, descricao, categoria, fornecedor]):
                messagebox.showerror("Erro", "Preencha todos os campos de texto.")
                return

            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO produtos (nome, codigo, descricao, categoria, fornecedor, preco_compra, preco_venda, quantidade, estoque_minimo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, codigo, descricao, categoria, fornecedor, preco_compra, preco_venda, quantidade, estoque_minimo))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar produto:\n{e}")

    tk.Button(window, text="Salvar", command=salvar).grid(row=len(labels), column=0, columnspan=2, pady=10)

def listar_produtos_interface():
    window = tk.Toplevel()
    window.title("Lista de Produtos")
    window.geometry("600x400")

    tree = ttk.Treeview(window, columns=("ID", "Nome", "Quantidade"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, quantidade FROM produtos")
    for row in cur.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def realizar_entrada_interface():
    window = tk.Toplevel()
    window.title("Realizar Entrada de Estoque")
    window.geometry("300x200")

    tk.Label(window, text="ID do Produto:").pack(pady=5)
    id_entry = tk.Entry(window)
    id_entry.pack(pady=5)

    tk.Label(window, text="Quantidade:").pack(pady=5)
    qtd_entry = tk.Entry(window)
    qtd_entry.pack(pady=5)

    def salvar():
        try:
            produto_id = int(id_entry.get())
            quantidade = int(qtd_entry.get())
            registrar_movimento(produto_id, 'entrada', quantidade, 'Compra')
            messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar entrada:\n{e}")

    tk.Button(window, text="Registrar Entrada", command=salvar).pack(pady=10)

def realizar_saida_interface():
    window = tk.Toplevel()
    window.title("Realizar Saída de Estoque")
    window.geometry("300x200")

    tk.Label(window, text="ID do Produto:").pack(pady=5)
    id_entry = tk.Entry(window)
    id_entry.pack(pady=5)

    tk.Label(window, text="Quantidade:").pack(pady=5)
    qtd_entry = tk.Entry(window)
    qtd_entry.pack(pady=5)

    def salvar():
        try:
            produto_id = int(id_entry.get())
            quantidade = int(qtd_entry.get())
            registrar_movimento(produto_id, 'saida', quantidade, 'Venda')
            messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar saída:\n{e}")

    tk.Button(window, text="Registrar Saída", command=salvar).pack(pady=10)

def alertas_interface():
    window = tk.Toplevel()
    window.title("Alertas de Estoque Baixo")
    window.geometry("400x300")

    alertas = verificar_estoque_baixo()

    if not alertas:
        tk.Label(window, text="Nenhum produto com estoque baixo.").pack(pady=20)
        return

    tree = ttk.Treeview(window, columns=("Produto", "Quantidade", "Estoque Mínimo"), show="headings")
    tree.heading("Produto", text="Produto")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Estoque Mínimo", text="Estoque Mínimo")
    tree.pack(fill=tk.BOTH, expand=True)

    for nome, qtd, min_estoque in alertas:
        tree.insert("", "end", values=(nome, qtd, min_estoque))

if __name__ == "__main__":
    criar_tabelas()
    login()

