from django.test import TestCase

from deliv_calc.models import Inventory, Product, Warehouse
from deliv_calc.library.warehouse_simulator import simulate_warehouse


class TestWarehouseSimulator(TestCase):

    def setUp(self):
        p1 = Product.objects.create(id='A')
        p2 = Product.objects.create(id='B')
        wh1 = Warehouse.objects.create(name='XYZ')
        wh2 = Warehouse.objects.create(name='TUY')
        wh3 = Warehouse.objects.create(name='DIY')
        Inventory.objects.create(warehouse=wh1, product=p1, quantity=5)
        Inventory.objects.create(warehouse=wh1, product=p2, quantity=2)
        Inventory.objects.create(warehouse=wh3, product=p2, quantity=3)

    def test_warehouse_with_one_inventory(self):
        wh = Warehouse.objects.filter(name='DIY').first()
        simulated_wh = simulate_warehouse(wh, distance=5)

        self.assertEqual(simulated_wh['name'], 'DIY')
        self.assertEqual(simulated_wh['distance'], 5)
        self.assertEqual(len(simulated_wh['inventory']), 1)
        self.assertEqual(simulated_wh['inventory']['B'], 3)

    def test_warehouse_with_two_inventories(self):
        wh = Warehouse.objects.filter(name='XYZ').first()
        simulated_wh = simulate_warehouse(wh, distance=18)

        self.assertEqual(simulated_wh['name'], 'XYZ')
        self.assertEqual(simulated_wh['distance'], 18)
        self.assertEqual(len(simulated_wh['inventory']), 2)
        self.assertEqual(simulated_wh['inventory']['B'], 2)
        self.assertEqual(simulated_wh['inventory']['A'], 5)

    def test_warehouse_with_three_inventories_two_same_product(self):
        wh = Warehouse.objects.filter(name='XYZ').first()
        pA = Product.objects.filter(id='A').first()
        Inventory.objects.create(warehouse=wh, product=pA, quantity=3)
        simulated_wh = simulate_warehouse(wh, distance=20)

        self.assertEqual(simulated_wh['name'], 'XYZ')
        self.assertEqual(simulated_wh['distance'], 20)
        self.assertEqual(len(simulated_wh['inventory']), 2)
        self.assertEqual(simulated_wh['inventory']['B'], 2)
        self.assertEqual(simulated_wh['inventory']['A'], 8)
