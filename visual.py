import matplotlib.pyplot as plt
import numpy as np


def generate_weight_histogram(G):
    weights = [w for _, _, w in G.edges(data="weight")]

    plt.hist(weights, bins=100, color="skyblue", edgecolor="black")

    mean = np.mean(weights, dtype=float)
    sd = np.std(weights, dtype=float)

    plt.axvline(
        mean,
        color="purple",
        linestyle="dashed",
        linewidth=2,
        label=f"Media: {mean:.3f}",
    )

    plt.axvline(
        sd + mean,
        color="green",
        linestyle="dashed",
        linewidth=2,
        label=f"μ+σ: {mean + sd:.3f}",
    )
    plt.axvline(
        mean - sd,
        color="green",
        linestyle="dashed",
        linewidth=2,
        label=f"μ-σ: {mean - sd:.3f}",
    )

    plt.xlabel("Costo")
    plt.ylabel("Frecuencia")
    plt.title("Frecuencia de los costos de aristas")
    plt.legend()
    plt.show()
