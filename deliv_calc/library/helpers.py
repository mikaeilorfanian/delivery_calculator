from deliv_calc.library.distance_algorithm import Dijkstra
from deliv_calc.models import Connection, Warehouse


def get_connected_warehouses(wh):
    connected_warehouses = []
    dijkstra = Dijkstra()
    warehouses = Warehouse.objects.all()

    for wareh in warehouses:
        # dijkstra throws TypeError when two warehouses(edges) are disconnected
        try:
            dijkstra.get_shortest_distance(wh.name, wareh.name)
            connected_warehouses.append(wareh)
        except TypeError:
            pass

    return connected_warehouses


def turn_edges_into_connections(edges):
    for edge in edges:
        start_wh = Warehouse.objects.get_or_create(name=edge[0])[0]
        end_wh = Warehouse.objects.get_or_create(name=edge[1])[0]
        Connection.objects.create(
            start=start_wh, end=end_wh, distance=edge[2])
