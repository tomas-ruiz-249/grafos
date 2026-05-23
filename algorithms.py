import networkx as nx
from scipy.spatial import ConvexHull
from itertools import combinations, permutations


def calc_cycle_cost(G, cycle):
    if cycle[0] != cycle[-1]:
        raise ValueError("cycle no contiene un ciclo")
    total = 0
    for i in range(len(cycle) - 1):
        total += G[cycle[i]][cycle[i + 1]]["weight"]
    return total


def brute_force(G: nx.Graph):
    nodes = list(G.nodes())
    start_node = nodes.pop()
    enumeration = {node: i for i, node in enumerate(nodes)}

    min_cost = float("inf")
    best_cycle = []

    if len(nodes) >= 9:
        print(
            "ADVERTENCIA: Hay mas de 10 nodos, el algoritmo puede demorarse mucho tiempo..."
        )

    for p in permutations(nodes):
        if enumeration[p[0]] > enumeration[p[-1]]:
            current_cycle = [start_node] + list(p) + [start_node]
            current_cost = calc_cycle_cost(G, current_cycle)
            if current_cost < min_cost:
                min_cost = current_cost
                best_cycle = current_cycle
    return best_cycle, min_cost


def nearest_neighbor(G):
    path = nx.approximation.greedy_tsp(G)
    return path, calc_cycle_cost(G, path)


def nearest_insertion(G):
    nodes = list(G.nodes())
    pairs = list(combinations(nodes, 2))

    A, B = "", ""
    min_cost = float("inf")

    for a, b in pairs:
        current_cost = G[a][b]["weight"]
        if min_cost > current_cost:
            min_cost = current_cost
            A, B = a, b

    cycle = [A, B, A]
    visited = set([A, B])

    min_dist_to_cycle = {
        C: min(G[A][C]["weight"], G[B][C]["weight"]) for C in set(nodes) - visited
    }

    while len(cycle) != len(nodes) + 1:
        closest_node = min(min_dist_to_cycle, key=lambda n: min_dist_to_cycle[n])

        min_insertion_cost = float("inf")
        insertion_index = -1
        for i in range(len(cycle) - 1):
            a = cycle[i]
            b = cycle[i + 1]
            current_insertion_cost = (
                G[a][closest_node]["weight"]
                + G[closest_node][b]["weight"]
                - G[a][b]["weight"]
            )

            if min_insertion_cost > current_insertion_cost:
                min_insertion_cost = current_insertion_cost
                insertion_index = i

        cycle.insert(insertion_index + 1, closest_node)
        visited.add(closest_node)
        min_dist_to_cycle = {
            C: min(G[closest_node][C]["weight"], min_dist_to_cycle[C])
            for C in set(nodes) - visited
        }

    return cycle, calc_cycle_cost(G, cycle)


def geometric(G):
    nodes = list(G.nodes())

    coords = [(G.nodes[n]["lat"], G.nodes[n]["long"]) for n in nodes]
    hull = ConvexHull(coords)
    cycle = [nodes[i] for i in hull.vertices]
    cycle.append(cycle[0])

    visited = set(cycle)

    min_dist_to_cycle = {}
    for node in set(nodes) - visited:
        min_dist_to_cycle[node] = min(
            G[node][hull_node]["weight"] for hull_node in cycle
        )

    while len(cycle) != len(nodes) + 1:
        closest_node = min(min_dist_to_cycle, key=lambda n: min_dist_to_cycle[n])

        min_insertion_cost = float("inf")
        insertion_index = -1
        for i in range(len(cycle) - 1):
            a = cycle[i]
            b = cycle[i + 1]
            current_insertion_cost = (
                G[a][closest_node]["weight"]
                + G[closest_node][b]["weight"]
                - G[a][b]["weight"]
            )

            if min_insertion_cost > current_insertion_cost:
                min_insertion_cost = current_insertion_cost
                insertion_index = i

        cycle.insert(insertion_index + 1, closest_node)
        visited.add(closest_node)
        min_dist_to_cycle = {
            C: min(G[closest_node][C]["weight"], min_dist_to_cycle[C])
            for C in set(nodes) - visited
        }

    return cycle, calc_cycle_cost(G, cycle)


def two_opt(G, cycle):
    n = len(G.nodes())
    improvement = True
    while improvement:
        improvement = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_cycle = cycle[:i] + cycle[i : j + 1][::-1] + cycle[j + 1 :]
                if calc_cycle_cost(G, new_cycle) < calc_cycle_cost(G, cycle):
                    improvement = True
                    cycle = new_cycle
    return cycle, calc_cycle_cost(G, cycle)
