from django import forms


class OrderForm(forms.Form):
    desc = forms.CharField()
    amount = forms.DecimalField(max_digits=20, decimal_places=2)
