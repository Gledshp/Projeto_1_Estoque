from db import conectar
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def previsao_demanda():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT p.nome, v.quantidade, v.data FROM vendas v JOIN produtos p ON p.id = v.produto_id")
    vendas = cur.fetchall()
    conn.close()

    produtos = {}
    for venda in vendas:
        nome, quantidade, data = venda
        if nome not in produtos:
            produtos[nome] = []
        produtos[nome].append((quantidade, data))

    for nome, dados in produtos.items():
        x = np.array([i for i in range(len(dados))]).reshape(-1, 1)
        y = np.array([d[0] for d in dados])

        model = LinearRegression()
        model.fit(x, y)

        previsao = model.predict(np.array([[len(dados)]]))
        print(f"Previsão de demanda para {nome}: {previsao[0]:.2f} unidades")

        plt.plot(x, y, label=nome)
        plt.plot(len(dados), previsao[0], 'ro', label=f"Previsão para {nome}")

    plt.title("Previsão de Demanda por Produto")
    plt.xlabel("Período")
    plt.ylabel("Quantidade Vendida")
    plt.legend()
    plt.tight_layout()
    plt.show()
