import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def plot_graph(G):
    pos = {node: (data["long"], data["lat"]) for node, data in G.nodes(data=True)}
    weights = [G[u][v]["weight"] for u, v in G.edges()]

    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color="steelblue")
    nx.draw_networkx_labels(G, pos, font_size=6)
    edge_width = max(1.0, 30 / len(G))
    edge_alpha = min(1.0, 6 / len(G))
    nx.draw_networkx_edges(G, pos, width=edge_width, alpha=edge_alpha, edge_color=weights, edge_cmap=plt.cm.YlOrRd)
    plt.title("Grafo de distribución")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.tight_layout()
    plt.show()


def plot_cycle(G, cycle):
    pos = {node: (data["long"], data["lat"]) for node, data in G.nodes(data=True)}
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    edge_width = max(1.0, 30 / len(G))
    edge_alpha = min(1.0, 6 / len(G))

    cycle_edges = list(zip(cycle[:-1], cycle[1:]))

    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color="steelblue")
    nx.draw_networkx_labels(G, pos, font_size=6)
    nx.draw_networkx_edges(G, pos, width=edge_width, alpha=edge_alpha, edge_color=weights, edge_cmap=plt.cm.YlOrRd)
    nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, width=edge_width + 1, edge_color="blue", arrows=True)
    plt.title("Ruta encontrada")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.tight_layout()
    plt.show()


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


def generate_benchmark_plots(results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for name, data in results.items():
        if not data["sizes"]:
            continue
        ax1.plot(data["sizes"], data["times"], marker="o", label=name)
        ax2.plot(data["sizes"], data["costs"], marker="o", label=name)

    ax1.set_xlabel("Número de nodos")
    ax1.set_ylabel("Tiempo de ejecución (s)")
    ax1.set_title("Tiempo de ejecución vs tamaño del grafo")
    ax1.legend()
    ax1.grid(True)

    ax2.set_xlabel("Número de nodos")
    ax2.set_ylabel("Costo del ciclo")
    ax2.set_title("Calidad de solución vs tamaño del grafo")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
