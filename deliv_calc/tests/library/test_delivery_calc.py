from django.test import TestCase

from deliv_calc.library.delivery_calculator import FIFODeliveryCalculator
from deliv_calc.models import Inventory, Product, Warehouse
from deliv_calc.library.requested_item import (
    RequestedProduct,
    RequestedProductCollection
)
from deliv_calc.library.warehouse_simulator import simulate_warehouse


class TestFIFODeliveryCalculator(TestCase):

    def setUp(self):
        p1 = Product.objects.create(id='A')
        p2 = Product.objects.create(id='B')
        wh1 = Warehouse.objects.create(name='XYZ')
        Warehouse.objects.create(name='TUY')
        Warehouse.objects.create(name='QRS')
        Inventory.objects.create(warehouse=wh1, product=p1, quantity=5)
        Inventory.objects.create(warehouse=wh1, product=p2, quantity=3)

    def test_all_products_already_in_destination_warehouse(self):
        req_prod1 = RequestedProduct('A', stock_requested=5)
        req_prod2 = RequestedProduct('B', stock_requested=3)
        req_prod_col = RequestedProductCollection()
        
        wh = Warehouse.objects.filter(name='XYZ').first()
        simulated_wh = simulate_warehouse(wh, distance=0)

        req_prod_col.add_items([req_prod1, req_prod2], [wh])

        deliv_cal = FIFODeliveryCalculator()
        deliv_time = deliv_cal.calculate_delivery_time(req_prod_col, 
            simulated_wh)
        
        self.assertEqual(deliv_time, 0)

    def test_no_products_in_destination_warehouse(self):
        req_prod1 = RequestedProduct('A', stock_requested=5)
        req_prod2 = RequestedProduct('B', stock_requested=3)
        req_prod_col = RequestedProductCollection()

        dest_wh = Warehouse.objects.filter(name='TUY').first()
        sim_dest_wh = simulate_warehouse(dest_wh, distance=0)

        other_wh = Warehouse.objects.filter(name='XYZ').first()
        sim_other_wh = simulate_warehouse(other_wh, distance=5)

        req_prod_col.add_items(
            [req_prod1, req_prod2], [dest_wh, other_wh])

        deliv_cal = FIFODeliveryCalculator()
        deliv_time = deliv_cal.calculate_delivery_time(req_prod_col, 
            sim_dest_wh, sim_other_wh)
        
        self.assertEqual(deliv_time, 5)

    def test_one_product_in_more_than_one_other_warehouse(self):
        req_prod1 = RequestedProduct('A', stock_requested=8)
        req_prod2 = RequestedProduct('B', stock_requested=3)

        dest_wh = Warehouse.objects.filter(name='TUY').first()
        sim_dest_wh = simulate_warehouse(dest_wh, distance=0)

        first_other_wh = Warehouse.objects.filter(name='XYZ').first()
        first_sim_other_wh = simulate_warehouse(first_other_wh, distance=5)

        second_other_wh = Warehouse.objects.filter(name='QRS').first()
        prod = Product.objects.filter(id='A').first()
        Inventory.objects.create(warehouse=second_other_wh, 
            product=prod, quantity=5)
        sec_sim_other_wh = simulate_warehouse(second_other_wh, distance=10)

        req_prod_col = RequestedProductCollection()
        req_prod_col.add_items(
            [req_prod1, req_prod2],
            [dest_wh, first_other_wh, second_other_wh]
        )

        deliv_cal = FIFODeliveryCalculator()
        deliv_time = deliv_cal.calculate_delivery_time(req_prod_col, 
            sim_dest_wh, first_sim_other_wh, sec_sim_other_wh)
        
        self.assertEqual(deliv_time, 15)

    def test_all_prods_in_dest_but_other_warehouses_also_have_it(self):
        req_prod1 = RequestedProduct('A', stock_requested=2)
        req_prod2 = RequestedProduct('B', stock_requested=3)

        dest_wh = Warehouse.objects.filter(name='XYZ').first()
        sim_dest_wh = simulate_warehouse(dest_wh, distance=0)

        first_other_wh = Warehouse.objects.filter(name='TUY').first()
        first_sim_other_wh = simulate_warehouse(first_other_wh, distance=5)

        second_other_wh = Warehouse.objects.filter(name='QRS').first()
        prod = Product.objects.filter(id='A').first()
        Inventory.objects.create(warehouse=second_other_wh, 
            product=prod, quantity=5)
        sec_sim_other_wh = simulate_warehouse(second_other_wh, distance=10)

        req_prod_col = RequestedProductCollection()
        req_prod_col.add_items([req_prod1, req_prod2],
                               [dest_wh, first_other_wh, second_other_wh])

        deliv_cal = FIFODeliveryCalculator()
        deliv_time = deliv_cal.calculate_delivery_time(req_prod_col, 
            sim_dest_wh, first_sim_other_wh, sec_sim_other_wh)

        self.assertEqual(deliv_time, 0)

    def test_one_prod_in_dest_wh_other_prod_in_another_wh(self):
        req_prod1 = RequestedProduct('A', stock_requested=2)
        req_prod2 = RequestedProduct('B', stock_requested=5)

        dest_wh = Warehouse.objects.filter(name='XYZ').first()
        sim_dest_wh = simulate_warehouse(dest_wh, distance=0)

        first_other_wh = Warehouse.objects.filter(name='TUY').first()
        first_sim_other_wh = simulate_warehouse(first_other_wh, distance=5)

        second_other_wh = Warehouse.objects.filter(name='QRS').first()
        prod = Product.objects.filter(id='B').first()
        Inventory.objects.create(warehouse=second_other_wh, 
            product=prod, quantity=5)
        sec_sim_other_wh = simulate_warehouse(second_other_wh, distance=100)

        req_prod_col = RequestedProductCollection()
        req_prod_col.add_items(
            [req_prod1, req_prod2],
            [dest_wh, first_other_wh, second_other_wh]
        )

        deliv_cal = FIFODeliveryCalculator()
        deliv_time = deliv_cal.calculate_delivery_time(req_prod_col, 
            sim_dest_wh, first_sim_other_wh, sec_sim_other_wh)

        self.assertEqual(deliv_time, 100)
