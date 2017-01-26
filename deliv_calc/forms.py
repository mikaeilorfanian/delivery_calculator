from django import forms


class DestinationWarehouseForm(forms.Form):
    dest_wh = forms.CharField(label='Destination', max_length=2, required=True)


class DeliveryCalcForm(forms.Form):
    prod_id = forms.CharField(label='Product ID', max_length=6)
    quantity = forms.IntegerField(label='Quantity', min_value=1)
