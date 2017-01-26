from django.db import models
from django.core.validators import MinValueValidator


class Warehouse(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return "<Warehouse: %s>" % self.name

    def get_inventory(self):
        inventory = {}
        
        for stock in self.inventories.all():
            if stock.product.id not in inventory:
                inventory[stock.product.id] = stock.quantity
            else:
                inventory[stock.product.id] += stock.quantity
        
        return inventory


class Connection(models.Model):
    start = models.ForeignKey(Warehouse, related_name='one_leg')
    end = models.ForeignKey(Warehouse, related_name='second_leg')
    distance = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('start', 'end')

    def __str__(self):
        return "start: %s, end: %s, distance: %s" \
            % (self.start, self.end, self.distance)


class Product(models.Model):
    id = models.CharField(max_length=6, primary_key=True)

    def __str__(self):
        return "ID: %s" % self.id


class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name="inventories")
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return "warehouse %s, prod_ID: %s, quantity: %s" \
            % (self.warehouse, self.product, self.quantity)
