import graph
import algorithms as algo
import visual
import data_handling
import time


def main():
    while True:
        print("----Menú principal-----")
        print("0.Salir")
        print("1.Generar grafo con datos almacenados")
        print(
            "2.Generar grafo consultando api y guardar datos obtenidos (Toma mucho tiempo)"
        )
        print("3.Generar grafo de pruebas (mock)")
        print("4.Ejecutar benchmark")

        option = int(input())
        if option == 0:
            print("Adios")
            return
        elif option == 4:
            run_benchmark()
            continue

        G = construct_graph(option)

        if len(G) > 0:
            graph.analyze_graph(G)
            visual.plot_graph(G)
            visual.generate_weight_histogram(G)

        while True:
            print("----Algoritmos de TSP-----")
            print("0.Volver al menú principal")
            print("1.Ejecutar algoritmo de fuerza bruta")
            print("2.Ejecutar algoritmo de vecino más cercano")
            print("3.Ejecutar algoritmo de inserción más cercana")
            print("4.Ejecutar algoritmo geometrico")
            print("5.Ejecutar algoritmo 2-opt")

            option = int(input())
            two_opt = -1
            if option == 0:
                break
            elif option == 5:
                print("Que algoritmo desea mejorar con 2-opt?")
                print("1.Usar algoritmo de fuerza bruta")
                print("2.Usar algoritmo de vecino más cercano")
                print("3.Usar algoritmo de inserción más cercana")
                print("4.Usar algoritmo geometrico")
                two_opt = int(input())

            start = time.perf_counter()
            cycle, cost = execute_algorithm(G, option, two_opt)
            end = time.perf_counter()

            print("El ciclo encontrado fue")
            print(*cycle, f"con costo de {cost}.", sep="\n")
            print(f"El tiempo de ejecución fue de {end - start:.4f} segundos.")
            visual.plot_cycle(G, cycle)


def construct_graph(option):
    while True:
        if option == 1:
            G = graph.create_graph_file()
            return G

        elif option == 2:
            G = graph.create_graph_api()
            data_handling.save_graph_weights(G)
            return G
        elif option == 3:
            nodes = input(
                "Ingrese los nodos que desea añadir al grafo separados por espacios.\n"
                + "Ingrese una linea en blanco si desea usar los nodos por defecto."
            ).split()
            G = graph.create_mock_graph(locations=nodes)
            return G

        print("Opcion invalida, intenta de nuevo")


def execute_algorithm(G, option, two_opt_algorithm=-1):
    while True:
        if option == 1:
            return algo.brute_force(G)
        elif option == 2:
            return algo.nearest_neighbor(G)
        elif option == 3:
            return algo.nearest_insertion(G)
        elif option == 4:
            return algo.geometric(G)
        elif option == 5 and two_opt_algorithm in [1, 2, 3, 4]:
            cycle, _ = execute_algorithm(G, two_opt_algorithm)
            return algo.two_opt(G, cycle)

        print("Opcion invalida, intenta de nuevo")


def _record(results, name, size, t, cost):
    results[name]["sizes"].append(size)
    results[name]["times"].append(t)
    results[name]["costs"].append(cost)
    print(f"{name}: costo={cost:.4f}, tiempo de ejecucion={t:.4f}s")


def run_benchmark():
    sizes = [5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50, 60]
    bf_max = 10

    names = [
        "Vecino más cercano",
        "Inserción más cercana",
        "Geométrico",
        "Fuerza bruta",
        "2-opt (Vecino más cercano)",
        "2-opt (Inserción más cercana)",
        "2-opt (Geométrico)",
        "2-opt (Fuerza bruta)",
    ]
    results = {name: {"sizes": [], "times": [], "costs": []} for name in names}

    for size in sizes:
        print(f"\n-------{size} nodos------------")
        G = graph.create_mock_graph(locations=list(range(size)))

        t0 = time.perf_counter()
        nn_cycle, cost = algo.nearest_neighbor(G)
        _record(results, "Vecino más cercano", size, time.perf_counter() - t0, cost)

        t0 = time.perf_counter()
        ni_cycle, cost = algo.nearest_insertion(G)
        _record(results, "Inserción más cercana", size, time.perf_counter() - t0, cost)

        t0 = time.perf_counter()
        geo_cycle, cost = algo.geometric(G)
        _record(results, "Geométrico", size, time.perf_counter() - t0, cost)

        bf_cycle = None
        if size <= bf_max:
            t0 = time.perf_counter()
            bf_cycle, cost = algo.brute_force(G)
            _record(results, "Fuerza bruta", size, time.perf_counter() - t0, cost)

        t0 = time.perf_counter()
        _, cost = algo.two_opt(G, nn_cycle)
        _record(
            results, "2-opt (Vecino más cercano)", size, time.perf_counter() - t0, cost
        )

        t0 = time.perf_counter()
        _, cost = algo.two_opt(G, ni_cycle)
        _record(
            results,
            "2-opt (Inserción más cercana)",
            size,
            time.perf_counter() - t0,
            cost,
        )

        t0 = time.perf_counter()
        _, cost = algo.two_opt(G, geo_cycle)
        _record(results, "2-opt (Geométrico)", size, time.perf_counter() - t0, cost)

        if bf_cycle is not None:
            t0 = time.perf_counter()
            _, cost = algo.two_opt(G, bf_cycle)
            _record(
                results, "2-opt (Fuerza bruta)", size, time.perf_counter() - t0, cost
            )

    visual.generate_benchmark_plots(results)


if __name__ == "__main__":
    main()
