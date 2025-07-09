from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from cart.models import Cart
from shop.models import Product




class AddCartView(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')


class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        return render(request,'cart.html',{'cart':c,'total':total})


class DecrementCartView(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        c=Cart.objects.get(user=u,product=p)
        if c.quantity>1:
            c.quantity-=1
            c.save()
        else:
            c.delete()

        return redirect('cart:cartview')


class RemoveCartView(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        c=Cart.objects.get(user=u,product=p)
        c.delete()

        return redirect('cart:cartview')


def check_stock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
    return stock

from cart.forms import OrderForm
from cart.models import Order_items
import razorpay
from django.contrib import messages
class OrderFormView(View):
    def get(self,request):
        form_instance=OrderForm()
        return render(request,'orderform.html',{'form':form_instance})

    def post(self,request):
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            order_obj=form_instance.save(commit=False)
            u = request.user
            order_obj.user=u
            order_obj.save()
            c=Cart.objects.filter(user=u)
            stock=check_stock(c) # to check the stock before the order

            if stock:
                for i in c:
                    o=Order_items.objects.create(order=order_obj,product=i.product,quantity=i.quantity)
                    o.save()

                total=0
                for i in c:
                    total+=i.quantity*i.product.price

                if order_obj.payment_method=='ONLINE':
                # RAZOR PAYMENT : online payment gateway

                    #create client connection
                    client=razorpay.Client(auth=('rzp_test_6gbGoBUyWtAO14','KbPJOTMaiSgmwBL5xH4DW3YY'))

                    #order creation
                    response_payment=client.order.create(dict(amount=total*100,currency='INR'))

                    print(response_payment)

                    order_id=response_payment['id']
                    order_obj.order_id=order_id
                    order_obj.is_ordered=False
                    order_obj.amount=total
                    order_obj.save()

                elif order_obj.payment_method=='COD':
                    order_obj.is_ordered=True
                    order_obj.save()

                    items = Order_items.objects.filter(order=order_obj)
                    for i in items:
                        i.product.stock -= i.quantity  # to decrement the stock after the order is completed
                        i.product.save()

                    # to delete the cart of the current user
                    c = Cart.objects.filter(user=u)
                    c.delete()

                    return redirect('shop:categories')

                else:
                    pass

                return render(request,'payment.html',{'payment':response_payment,'name':u.username})

            else:
                messages.error(request,'Currently item is not available')
                return render(request,'payment.html')


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from shop.models import CustomUser
from django.contrib.auth import login
from cart.models import Order,Order_items
@method_decorator(csrf_exempt,name='dispatch') #to avoid csrf token error
class PaymentSuccessView(View):
    def post(self,request,i):
        user=CustomUser.objects.get(username=i)
        login(request, user) # to add the current user to the session agin

        response=request.POST #payment confirmation sent by razorpay to our app
                                # order_id,payment_id,signature
        print(response)

        o=Order.objects.get(order_id=response['razorpay_order_id'])
        o.is_ordered=True
        o.save()

        # to change the stock
        items=Order_items.objects.filter(order=o)
        for i in items:
            i.product.stock-=i.quantity # to decrement the stock after the order is completed
            i.product.save()

        # to delete the cart of the current user
        c=Cart.objects.filter(user=user)
        c.delete()

        return render(request,'payment_success.html')


class OrderSummaryView(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        return render(request,'ordersummary.html',{'orders':o})