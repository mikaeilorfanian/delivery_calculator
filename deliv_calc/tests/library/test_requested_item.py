from django.test import TestCase

from deliv_calc.models import Inventory, Product, Warehouse
from deliv_calc.library.requested_item import (
    OutOfStockException,
    RequestedProduct,
    RequestedProductCollection
)


class TestRequestedProductCollection(TestCase):
    
    def setUp(self):
        p1 = Product.objects.create(id='A')
        p2 = Product.objects.create(id='B')
        wh = Warehouse.objects.create(name='XYZ')
        Inventory.objects.create(warehouse=wh, product=p1, quantity=5)
        Inventory.objects.create(warehouse=wh, product=p2, quantity=3)
    
    def test_collecction_with_no_duplicates(self):    
        item1 = RequestedProduct('A', 2)
        item2 = RequestedProduct('B', 3)
        wh = Warehouse.objects.filter(name='XYZ').first()

        collection = RequestedProductCollection()
        collection.add_items([item1, item2], [wh])

        self.assertEqual(collection.items[0]._id, 'A')
        self.assertEqual(collection.items[1]._id, 'B')
        self.assertEqual(collection.items[0].stock_requested, 2)
        self.assertEqual(collection.items[1].stock_requested, 3)

    def test_collecction_with_duplicates(self):    
        item1 = RequestedProduct('A', 2)
        item2 = RequestedProduct('A', 3)
        item3 = RequestedProduct('B', 1)
        wh = Warehouse.objects.filter(name='XYZ').first()

        collection = RequestedProductCollection()
        collection.add_items([item1, item2, item3], [wh])

        assert len(collection.items) == 2
        assert collection.items[0]._id == 'A'
        assert collection.items[1]._id == 'B'
        assert collection.items[0].stock_requested == 5
        assert collection.items[1].stock_requested == 1

    def test_collection_with_out_of_stock_item(self):
        Product.objects.create(id='C')
        wh = Warehouse.objects.create(name='TUY')
        
        item = RequestedProduct('C', 10)
        collection = RequestedProductCollection()
        self.assertRaises(
            OutOfStockException, collection.add_items, [item], [wh])
