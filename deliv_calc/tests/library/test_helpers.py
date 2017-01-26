from django.test import TestCase

from deliv_calc.library.helpers import get_connected_warehouses
from deliv_calc.models import Connection, Warehouse


class TestConnectedWarehouseFinder(TestCase):

    def test_lone_warehouse(self):
        AA = Warehouse.objects.create(name='AA')

        conctd_warehouses = get_connected_warehouses(AA)

        self.assertIn(AA, conctd_warehouses)
        self.assertEqual(len(conctd_warehouses), 1)

    def test_two_connected(self):
        AA = Warehouse.objects.create(name='AA')
        BC = Warehouse.objects.create(name='BC')

        Connection.objects.create(start=BC, end=AA, distance=5)

        conctd_warehouses = get_connected_warehouses(AA)

        self.assertIn(AA, conctd_warehouses)
        self.assertIn(BC, conctd_warehouses)
        self.assertEqual(len(conctd_warehouses), 2)

    def test_one_lone_wh_two_connected_warehouses(self):
        AA = Warehouse.objects.create(name='AA')
        BC = Warehouse.objects.create(name='BC')
        DC = Warehouse.objects.create(name='DC')

        Connection.objects.create(start=BC, end=AA, distance=5)

        AAconctd_warehouses = get_connected_warehouses(AA)

        self.assertIn(AA, AAconctd_warehouses)
        self.assertIn(BC, AAconctd_warehouses)
        self.assertEqual(len(AAconctd_warehouses), 2)

        DCconctd_warehouses = get_connected_warehouses(DC)

        self.assertIn(DC, DCconctd_warehouses)
        self.assertEqual(len(DCconctd_warehouses), 1)

    def test_two_sets_of_disconnectd_warehouses(self):
        AA = Warehouse.objects.create(name='AA')
        BC = Warehouse.objects.create(name='BC')
        DC = Warehouse.objects.create(name='DC')

        EF = Warehouse.objects.create(name='EF')
        GI = Warehouse.objects.create(name='GI')
        KG = Warehouse.objects.create(name='KG')

        Connection.objects.create(start=BC, end=AA, distance=5)
        Connection.objects.create(start=BC, end=DC, distance=5)

        Connection.objects.create(start=EF, end=GI, distance=5)
        Connection.objects.create(start=KG, end=GI, distance=5)

        first_conctd_warehouses = get_connected_warehouses(AA)

        self.assertIn(AA, first_conctd_warehouses)
        self.assertIn(BC, first_conctd_warehouses)
        self.assertIn(DC, first_conctd_warehouses)
        self.assertEqual(len(first_conctd_warehouses), 3)

        second_conctd_warehouses = get_connected_warehouses(KG)

        self.assertIn(KG, second_conctd_warehouses)
        self.assertIn(GI, second_conctd_warehouses)
        self.assertIn(EF, second_conctd_warehouses)
        self.assertEqual(len(second_conctd_warehouses), 3)
