import graph
import algorithms as algo
import visual
import data_handling
import time


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


def main():
    print("----Construcción del grafo-----")
    print("1.Generar grafo con datos almacenados")
    print(
        "2.Generar grafo consultando api y guardar datos obtenidos (Toma mucho tiempo)"
    )
    print("3.Generar grafo de pruebas (mock)")

    option = int(input())
    G = construct_graph(option)

    if len(G) > 0:
        graph.analyze_graph(G)
        visual.generate_weight_histogram(G)

    while True:
        print("----Algoritmos de TSP-----")
        print("0.Salir")
        print("1.Ejecutar algoritmo de fuerza bruta")
        print("2.Ejecutar algoritmo de vecino más cercano")
        print("3.Ejecutar algoritmo de inserción más cercana")
        print("4.Ejecutar algoritmo geometrico")
        print("5.Ejecutar algoritmo 2-opt")

        option = int(input())
        two_opt = -1
        if option == 0:
            print("Adios")
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


if __name__ == "__main__":
    main()
