

class WarehouseSorter:

    def __init__(self, distance_algo, warehouses):
        self.distance_algo = distance_algo
        self.warehouses = warehouses
        self.sortd_warehouses = []  # [(Warehouse: distance),]

    def sort(self, dest_warehouse):
        self.sortd_warehouses.append((dest_warehouse, 0))

        for wh in self.warehouses:
            distance = self.distance_algo.get_shortest_distance(
                dest_warehouse.name, wh.name)
            self._add_wh_to_sortd_list(wh, distance)

        return self.sortd_warehouses

    def _add_wh_to_sortd_list(self, wh, distance):
        if distance == 0:
            return

        for i in range(len(self.sortd_warehouses)):
            if distance < self.sortd_warehouses[i][1]:
                self.sortd_warehouses.insert(i, (wh, distance))
                return

        self.sortd_warehouses.append((wh, distance))
