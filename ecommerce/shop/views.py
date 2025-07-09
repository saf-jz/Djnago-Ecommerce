from django.shortcuts import render,redirect

from django.views.generic import View

from shop.models import Category
class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'category':c})

class ProductsView(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        return render(request,'products.html',{'category':c})


from shop.models import Product
class ProductDetailView(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        return render(request,'prod_detail.html',{'product':p})


from shop.forms import SignupForm
from django.core.mail import send_mail
class SignupView(View):
    def get(self,request):
        form_instance=SignupForm()
        return render(request,'signup.html',{'form':form_instance})

    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            user=form_instance.save(commit=False)
            user.is_active=False # after otp verification it will set to True
            user.save()
            user.gen_otp()
            send_mail(
                'Ecommerce OTP',
                user.otp,
                'sj50025010@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('shop:otpverify')


from shop.models import CustomUser
from django.contrib import messages
class OtpVerficationView(View):
    def get(self,request):
        return render(request,'otp.html')

    def post(self,request):
        o=request.POST.get('otp')
        print(o)
        try:
            u=CustomUser.objects.get(otp=o)
            u.is_active=True
            u.is_verified=True
            u.otp=None
            u.save()
            return redirect('shop:categories')
        except:
            #print('Invalid OTP')
            messages.error(request,'Invalid OTP')
            return redirect('shop:otpverify')


from shop.forms import LoginForm
from django.contrib.auth import authenticate,login
class SigninView(View):
    def get(self,request):
        form_instance=LoginForm()
        return render(request,'login.html',{'form':form_instance})

    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd=form_instance.cleaned_data['password']
            print(name,pwd)
            user=authenticate(username=name,password=pwd)

            if user and user.is_superuser==True:
                login(request,user)
                u=request.user
                return redirect('shop:categories')
            elif user and user.is_superuser==False:
                login(request,user)
                u=request.user
                return redirect('shop:categories')
            else:
                print('Invalid User Creditials')

        return redirect('shop:categories')


from django.contrib.auth import logout
class SignoutView(View):
    def get(self,request):
        logout(request)
        return redirect('shop:signin')


from shop.forms import CategoryForm,ProductForm

class AddCategoryView(View):
    def get(self,request):
        form_instance=CategoryForm()
        return render(request,'addcategory.html',{'form':form_instance})

    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            form_instance=CategoryForm() #if we need new form instead of the filled data form
            return render(request,'addcategory.html',{'form':form_instance})

class AddProductView(View):
    def get(self,request):
        form_instance=ProductForm()
        return render(request,'addproduct.html',{'form':form_instance})

    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')



