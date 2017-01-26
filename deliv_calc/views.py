from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render

from deliv_calc.forms import DeliveryCalcForm, DestinationWarehouseForm
from deliv_calc.library.delivery_calculator import FIFODeliveryCalculator
from deliv_calc.library.distance_algorithm import Dijkstra
from deliv_calc.library.helpers import get_connected_warehouses
from deliv_calc.library.requested_item import (
    OutOfStockException,
    ProductDoesNotExist,
    RequestedProductCollection,
    turn_formset_into_requested_prods,
)
from deliv_calc.library.warehouse_simulator import simulate_warehouse
from deliv_calc.library.warehouse_sort import WarehouseSorter
from deliv_calc.models import Warehouse


def index(request):

    if request.method == 'POST':

        dest_form = DestinationWarehouseForm(request.POST)

        if dest_form.is_valid():
            dest_warehouse = Warehouse.objects.filter(
                name=dest_form.cleaned_data['dest_wh']).first()
            if not dest_warehouse:
                return HttpResponse('Destination warehouse does not exist!')

        DeliverCalcFormset = formset_factory(
            DeliveryCalcForm, extra=4, min_num=1, validate_min=1)
        deliv_calc_formset = DeliverCalcFormset(request.POST)
        
        if deliv_calc_formset.is_valid():

            avail_warehouses = get_connected_warehouses(dest_warehouse)
            req_prods = turn_formset_into_requested_prods(deliv_calc_formset)
            req_prods_coll = RequestedProductCollection()

            try:
                req_prods_coll.add_items(req_prods, avail_warehouses)
            except (ProductDoesNotExist, OutOfStockException) as e:
                return HttpResponse(str(e))

            distance_alg = Dijkstra()
            wh_sorter = WarehouseSorter(distance_alg, avail_warehouses)
            sortd_warehouses = wh_sorter.sort(dest_warehouse)
            sim_sortd_wh = [
                simulate_warehouse(wh, dist) for wh, dist in sortd_warehouses]

            deliv_calc = FIFODeliveryCalculator()
            deliv_time = deliv_calc.calculate_delivery_time(
                req_prods_coll, *sim_sortd_wh)

            return render(
                request, 
                'home.html', 
                {
                    'dest_form': dest_form, 
                    'formset': deliv_calc_formset, 
                    'deliv_time': str(deliv_time),
                }
            )

    else:
        dest_form = DestinationWarehouseForm(request.POST)
        DeliverCalcFormset = formset_factory(
            DeliveryCalcForm, extra=4, min_num=1, validate_min=1)
        deliv_calc_formset = DeliverCalcFormset()
    
    return render(request, 
        'home.html', {'dest_form': dest_form, 'formset': deliv_calc_formset})
