import csv
import pickle
from pathlib import Path

import matplotlib.pyplot as plt

QTABLE_PATH = Path(__file__).parent / "agents" / "qtable.pkl"
CSV_OUTPUT = Path(__file__).parent / "qtable_export.csv"
CHART_OUTPUT = Path(__file__).parent / "qtable_distribution.png"

FEATURE_NAMES = [
    "perigo_reto",
    "perigo_esquerda",
    "perigo_direita",
    "direcao_cima",
    "direcao_baixo",
    "direcao_esquerda",
    "direcao_direita",
    "maca_esquerda",
    "maca_direita",
    "maca_cima",
    "maca_baixo",
]
ACTIONS = ["straight", "left", "right"]


def describe_state(state) -> str:
    ativos = [name for name, value in zip(FEATURE_NAMES, state) if value]
    return ", ".join(ativos) if ativos else "nenhuma feature ativa"


def main():
    with open(QTABLE_PATH, "rb") as f:
        q_table = pickle.load(f)

    ordenado = sorted(q_table.items(), key=lambda item: max(item[1]), reverse=True)

    # exporta q table pra csv
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FEATURE_NAMES + ["Q_straight", "Q_left", "Q_right", "melhor_acao"])
        for state, q_values in ordenado:
            melhor_acao = ACTIONS[q_values.index(max(q_values))]
            writer.writerow(list(state) + [round(v, 3) for v in q_values] + [melhor_acao])

    print(f"\nTabela completa exportada para: {CSV_OUTPUT}")

    # gera grafico de visualização dos q values
    todos_valores = [v for q_values in q_table.values() for v in q_values]

    plt.figure(figsize=(8, 5))
    plt.hist(todos_valores, bins=40, color="#4c72b0", edgecolor="black")
    plt.title("Distribuição dos Q-valores aprendidos")
    plt.xlabel("Q-valor")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.savefig(CHART_OUTPUT, dpi=150)
    print(f"Gráfico salvo em: {CHART_OUTPUT}")


if __name__ == "__main__":
    main()