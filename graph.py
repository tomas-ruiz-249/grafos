from itertools import combinations
import networkx as nx
import random

from config import ALPHA, BETA, GAMMA
import api
import data_handling


def create_graph_api():
    G = nx.Graph()
    G.add_nodes_from(
        (name, {"lat": data["lat"], "long": data["long"]})
        for name, data in api.location_data.items()
    )

    pairs = list(combinations(list(G), 2))
    raw = {}

    min_dist = min_time = min_traffic = float("inf")
    max_dist = max_time = max_traffic = 0

    for a, b in pairs:
        print("calling api for: " + a + " to " + b)
        dist, time, traffic = api.get_traffic_data(a, b)
        raw[(a, b)] = (dist, time, traffic)
        min_dist = min(dist, min_dist)
        min_time = min(time, min_time)
        min_traffic = min(traffic, min_traffic)
        max_dist = max(dist, max_dist)
        max_time = max(time, max_time)
        max_traffic = max(traffic, max_traffic)

    for (a, b), (dist, time, traffic) in raw.items():
        norm_dist = (
            (dist - min_dist) / (max_dist - min_dist) if max_dist != min_dist else 0
        )
        norm_time = (
            (time - min_time) / (max_time - min_time) if max_time != min_time else 0
        )
        norm_traffic = (
            (traffic - min_traffic) / (max_traffic - min_traffic)
            if max_traffic != min_traffic
            else 0
        )
        cost = ALPHA * norm_dist + BETA * norm_time + GAMMA * norm_traffic
        G.add_edge(
            a, b, dist=norm_dist, time=norm_time, traffic=norm_traffic, weight=cost
        )

    return G


def create_mock_graph(locations=None):
    if locations is None or locations == []:
        locations = ["A", "B", "C", "D", "E"]

    def rand_normal():
        return max(0.0, min(1.0, random.gauss(0.5, 0.167)))

    G = nx.Graph()
    G.add_nodes_from(
        (loc, {"lat": rand_normal(), "long": rand_normal()})
        for loc in locations
    )

    for a, b in combinations(locations, 2):
        dist = rand_normal()
        time = rand_normal()
        traffic = rand_normal()
        cost = ALPHA * dist + BETA * time + GAMMA * traffic
        G.add_edge(a, b, dist=dist, time=time, traffic=traffic, weight=cost)

    return G


def create_graph_file():
    return data_handling.load_graph_from_file()


def analyze_graph(G):
    print("\n----Análisis estructural del grafo----")

    print(f"\nNodos: {G.number_of_nodes()}")
    print(f"Aristas: {G.number_of_edges()}")

    print(f"\nDensidad: {nx.density(G):.4f}")

    print(f"\nConexo: {nx.is_connected(G)}")
    if nx.is_connected(G):
        print(f"Conectividad de nodos: {nx.node_connectivity(G)}")
        print(f"Conectividad de aristas: {nx.edge_connectivity(G)}")

    print("\nGrado de cada vértice:")
    for node, degree in sorted(G.degree(), key=lambda x: x[1], reverse=True):
        print(f"  {node}: {degree}")
