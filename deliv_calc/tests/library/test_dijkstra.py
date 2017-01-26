from django.test import TestCase

from deliv_calc.library.distance_algorithm import (
    Dijkstra,
    turn_edges_into_connections,
)

class TestDijkstra(TestCase):

    def test_dijkstra_find_correct_distance_for_simple_graph(self):
        edges = [
            ('A', 'B', 2),
            ('A', 'C', 1),
            ('C', 'B', 2)
        ]
        turn_edges_into_connections(edges)
        dist_algo = Dijkstra()

        self.assertEqual(dist_algo.get_shortest_distance('A', 'B'), 2)

    def test_dijkstra_finds_correct_distance_for_graph_with_two_equal_shortest_paths(self):
        edges = [
            ('A', 'B', 2),
            ('A', 'C', 1),
            ('C', 'B', 1)
        ]
        turn_edges_into_connections(edges)
        dist_algo = Dijkstra()

        self.assertEqual(dist_algo.get_shortest_distance('A', 'B'), 2)

    def test_dijkstra_works_correctly_for_complicated_graph(self):
        edges = [
            ("A", "B", 7),
            ("A", "D", 5),
            ("B", "C", 8),
            ("B", "D", 9),
            ("B", "E", 7),
            ("C", "E", 5),
            ("D", "E", 15),
            ("D", "F", 6),
            ("E", "F", 8),
            ("E", "G", 9),
            ("F", "G", 11)
        ]
        turn_edges_into_connections(edges)
        dist_algo = Dijkstra()

        self.assertEqual(dist_algo.get_shortest_distance('A', 'E'), 14)
        self.assertEqual(dist_algo.get_shortest_distance('F', 'G'), 11)

    def test_distance_to_self_equals_to_zero(self):
        edges = [
            ("A", "B", 7),
            ("A", "D", 5),
        ]
        turn_edges_into_connections(edges)
        dist_algo = Dijkstra()

        self.assertEqual(dist_algo.get_shortest_distance('A', 'A'), 0)

    def test_distance_to_disconnected_nodes_raises_exception(self):
        edges = [
            ("A", "B", 7),
            ("A", "D", 5),
            ("E", "F", 2)
        ]
        turn_edges_into_connections(edges)
        dist_algo = Dijkstra()

        self.assertRaises(
            TypeError,
            dist_algo.get_shortest_distance,
            'A',
            'F',
        )
