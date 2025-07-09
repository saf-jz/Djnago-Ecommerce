"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from cart import views
app_name='cart'

urlpatterns = [
    path('addcart/<int:i>',views.AddCartView.as_view(),name='addcart'),
    path('cartview',views.CartView.as_view(),name='cartview'),
    path('decrementcart/<int:i>',views.DecrementCartView.as_view(),name='deccart'),
    path('removecart/<int:i>',views.RemoveCartView.as_view(),name='removecart'),
    path('orderform',views.OrderFormView.as_view(),name='orderform'),
    path('paymentsuccess/<i>',views.PaymentSuccessView.as_view(),name='paymentsuccess'),
    path('ordersummary',views.OrderSummaryView.as_view(),name='ordersummary')
]


