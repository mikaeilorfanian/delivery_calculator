

class BaseDeliveryCalculator():
    
    def __init__(self):
        self.delivery_time = 0
    
    def calculate_delivery_time(self, items_requested, warehouses):
        # to be defined by child class
        pass


class FIFODeliveryCalculator(BaseDeliveryCalculator):
    
    def calculate_delivery_time(self, req_prod_col, *sim_warehouses):

        for warehouse in sim_warehouses:
            count_warehouse_in_arrival_time = False

            for prod_to_deliv in req_prod_col:
                if prod_to_deliv.stock_requested == 0:
                    continue

                if prod_to_deliv._id in warehouse['inventory']:
                    count_warehouse_in_arrival_time = True
                    if prod_to_deliv.stock_requested <= warehouse['inventory'][prod_to_deliv._id]:
                        warehouse['inventory'][prod_to_deliv._id] -= prod_to_deliv.stock_requested
                        prod_to_deliv.stock_requested = 0
                    else:
                        prod_to_deliv.stock_requested -= warehouse['inventory'][prod_to_deliv._id]
                        warehouse['inventory'][prod_to_deliv._id] = 0
            
            if count_warehouse_in_arrival_time:
                self.delivery_time += warehouse['distance']

        return self.delivery_time
