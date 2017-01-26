from collections import defaultdict
from heapq import *

from deliv_calc.models import Connection, Warehouse


class BaseDistanceAlgorithm:
    # to be defined by child class
    def get_shortest_distance(self, start_wh, end_wh):
        pass


class Dijkstra(BaseDistanceAlgorithm):

    def __init__(self):
        self.edges = self._turn_connections_to_edges()

    def get_shortest_distance(self, start_wh, end_wh):
        return self._dijkstra(start_wh, end_wh)[0]

    def _turn_connections_to_edges(self):
        connections = Connection.objects.all()
        edges = []
        for c in connections:
            edges.append((c.start.name, c.end.name, c.distance))
            edges.append((c.end.name, c.start.name, c.distance))

        return edges

    def _dijkstra(self, f, t):

        g = defaultdict(list)
        for l, r, c in self.edges:
            g[l].append((c, r))

        q, seen = [(0, f, ())], set()
        while q:
            (cost, v1, path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == t:
                    return cost, path

                for c, v2 in g.get(v1, ()):
                    if v2 not in seen:
                        heappush(q, (cost+c, v2, path))

        return float("inf")

