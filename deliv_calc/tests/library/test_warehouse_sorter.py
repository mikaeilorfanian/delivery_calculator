from django.test import TestCase

from deliv_calc.library.distance_algorithm import Dijkstra
from deliv_calc.library.warehouse_sort import WarehouseSorter
from deliv_calc.models import Connection, Warehouse


class TestWarehouseSorter(TestCase):

    def test_sorts_one_wh_correctly(self):
        wh = Warehouse.objects.create(name='AB')

        dijkstra = Dijkstra()
        wh_sorter = WarehouseSorter(dijkstra, [wh])
        sortd_wh = wh_sorter.sort(wh)

        self.assertEqual(len(sortd_wh), 1)
        self.assertEqual(sortd_wh[0][0].name, 'AB')
        self.assertEqual(sortd_wh[0][1], 0)

    def test_sorts_more_than_one_wh_correctly(self):
        AB = Warehouse.objects.create(name='AB')
        CD = Warehouse.objects.create(name='CD')
        EF = Warehouse.objects.create(name='EF')
        GH = Warehouse.objects.create(name='GH')
        IJ = Warehouse.objects.create(name='IJ')
        KL = Warehouse.objects.create(name='KL')
        MN = Warehouse.objects.create(name='MN')

        Connection.objects.create(
            start=AB, end=CD, distance=4)
        Connection.objects.create(
            start=AB, end=EF, distance=7)
        Connection.objects.create(
            start=AB, end=GH, distance=3)
        Connection.objects.create(
            start=GH, end=CD, distance=1)
        Connection.objects.create(
            start=EF, end=CD, distance=1)
        Connection.objects.create(
            start=AB, end=IJ, distance=1)
        Connection.objects.create(
            start=KL, end=IJ, distance=1)
        Connection.objects.create(
            start=MN, end=AB, distance=4)

        dijkstra = Dijkstra()
        wh_sorter = WarehouseSorter(dijkstra, [AB,CD,EF,GH,IJ,KL,MN])
        sortd_wh = wh_sorter.sort(AB)
        correct_response = [
            (AB, 0),
            (IJ, 1),
            (KL, 2),
            (GH, 3),
            (CD, 4),
            (MN, 4),
            (EF, 5)
        ]

        self.assertEqual(sortd_wh, correct_response)
