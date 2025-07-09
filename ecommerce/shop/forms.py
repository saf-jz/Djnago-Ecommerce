from django import forms

from django.contrib.auth.forms import UserCreationForm
from shop.models import CustomUser
class SignupForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','password1','password2','email','first_name','last_name','phone']

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


from shop.models import Category,Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','description','image','price','stock','category']

