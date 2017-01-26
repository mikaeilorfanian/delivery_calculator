import csv

from deliv_calc.models import Connection, Inventory, Product, Warehouse


def load_warehouses():
    with open('connections.csv') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]
        rows = rows[1:]

        for row in rows:
            if row:
                Warehouse.objects.get_or_create(name=row[0])
                Warehouse.objects.get_or_create(name=row[1])


def load_connections():
    with open('connections.csv') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]
        rows = rows[1:]

        for row in rows:
            if row:
                wh1 = Warehouse.objects.filter(name=row[0]).first()
                wh2 = Warehouse.objects.filter(name=row[1]).first()
                Connection.objects.get_or_create(
                    start=wh1, end=wh2, distance=int(row[2]))


def load_products():
    with open('stocks.csv') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]
        rows = rows[1:]

        for row in rows:
            if row:
                Product.objects.get_or_create(id=row[1])


def load_inventory():
    with open('stocks.csv') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]
        rows = rows[1:]

        for row in rows:
            if row:
                wh = Warehouse.objects.filter(name=row[0]).first()
                prod = Product.objects.filter(id=row[1]).first()
                Inventory.objects.get_or_create(
                    warehouse=wh, product=prod, quantity=int(row[2])
                )
