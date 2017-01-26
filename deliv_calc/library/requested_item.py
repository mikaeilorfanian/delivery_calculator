from django.db.models import Sum

from deliv_calc.models import Product


class ProductDoesNotExist(Exception):
    pass


class RequestedProduct:
    
    def __init__(self, item_id, stock_requested):
        self._id = item_id
        self.stock_requested = stock_requested

    def available_in_stock(self, connctd_warehouses):
        prod = Product.objects.filter(id=self._id).first()
        if not prod:
            raise ProductDoesNotExist('%s is not in any warehouse!' % self._id)

        availbl_stock = prod.inventory_set.filter(warehouse__in=connctd_warehouses).aggregate(Sum('quantity'))
        if availbl_stock['quantity__sum'] < self.stock_requested:
            raise OutOfStockException('%s is out of stock!' % self._id)

        return

    def __str__(self):
        return '<RequestProduct name: %s, amount: %s>' \
            % (self._id, self.stock_requested)


class OutOfStockException(Exception):
    pass


class RequestedProductCollection:

    def __init__(self):
        self.items = []

    def add_items(self, requested_items, avail_warehouses):
        for new_requested_item in requested_items:
            self.add_item(new_requested_item, avail_warehouses)

    def add_item(self, new_requested_item, connctd_warehouses):
        new_requested_item.available_in_stock(connctd_warehouses)

        for item in self.items:
            if item._id == new_requested_item._id:
                item.stock_requested += new_requested_item.stock_requested
                return

        self.items.append(new_requested_item)

    def __iter__(self):
        for prod in self.items:
            yield prod

    def __str__(self):
        text = '<<<ReqProdColl: \n'
        for item in self.items:
            text += str(item)
            text += '\n'
        text += '>>>'
        return text


def turn_formset_into_requested_prods(formset):
    requested_items = []

    for form in formset:
        name = form.cleaned_data.get('prod_id')
        quantity = form.cleaned_data.get('quantity')

        if name and quantity:
            added = False
            for req_prod in requested_items:
                if req_prod._id == name:
                    req_prod.stock_requested += quantity
                    added = True
                    break

            if not added:
                req_prod = RequestedProduct(name, quantity)
                requested_items.append(req_prod)

    return requested_items
