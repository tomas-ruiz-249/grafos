import csv
import pandas as pd
import networkx as nx


def create_location_dict():
    locations = dict()
    with open("data/location_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            locations[row["name"]] = {
                "lat": float(row["lat"]),
                "long": float(row["long"]),
            }
    return locations


def save_graph_weights(G):
    nx.to_pandas_edgelist(G).to_csv("data/edges.csv", index=False)


def load_graph_from_file():
    df = pd.read_csv("data/edges.csv")
    G = nx.from_pandas_edgelist(df, source="source", target="target", edge_attr=True)
    locations = create_location_dict()
    for name, data in locations.items():
        if name in G:
            G.nodes[name]["lat"] = data["lat"]
            G.nodes[name]["long"] = data["long"]
    return G
