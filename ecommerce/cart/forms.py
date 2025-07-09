from django import forms

from cart.models import Order
from django.forms import RadioSelect


class OrderForm(forms.ModelForm):
    choices=(('COD','COD'),('ONLINE','ONLINE'))
    payment_method=forms.ChoiceField(choices=choices,widget=RadioSelect)
    class Meta:
        model=Order
        fields=['address','phone','payment_method']

