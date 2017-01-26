

def simulate_warehouse(warehouse, distance):
    simulated_wh = {'name': warehouse.name, 'distance': distance}
    simulated_wh['inventory'] = warehouse.get_inventory()

    return simulated_wh

