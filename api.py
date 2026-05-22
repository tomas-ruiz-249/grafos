import requests as rq
import data_handling as dh
import config

TOM_TOM_URL = "https://api.tomtom.com"
location_data = dh.create_location_dict()


def get_traffic_data(location_1, location_2):
    l1 = location_data[location_1]
    l2 = location_data[location_2]
    r = rq.get(
        TOM_TOM_URL
        + f"/routing/1/calculateRoute/{l1["lat"]},{l1["long"]}:{l2["lat"]},{l2["long"]}/json?"
        + f"key={config.TOM_TOM_API_KEY}"
        + "&computeTravelTimeFor=all"
        + "&language=es-ES"
    )
    routes = r.json()["routes"]
    route = routes[0]["summary"]

    dist = route["lengthInMeters"]
    time = route["travelTimeInSeconds"]
    traffic = route["trafficLengthInMeters"]

    return dist, time, traffic
