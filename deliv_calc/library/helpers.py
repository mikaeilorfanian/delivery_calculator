from deliv_calc.library.distance_algorithm import Dijkstra
from deliv_calc.models import Warehouse


def get_connected_warehouses(wh):
    connected_warehouses = []
    dijkstra = Dijkstra()
    warehouses = Warehouse.objects.all()

    for wareh in warehouses:
        try:
            dijkstra.get_shortest_distance(wh.name, wareh.name)
            connected_warehouses.append(wareh)
        except TypeError:
            pass
    return connected_warehouses
