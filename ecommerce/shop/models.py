from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField()
    image=models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='products')
    description=models.TextField()
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True) # date time get created when the product is created at first
    updated=models.DateTimeField(auto_now=True) # each time the record is updated auto date time gets updated
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')

    def __str__(self):
        return self.name


from django.contrib.auth.models import AbstractUser
from random import randint
class CustomUser(AbstractUser):
    phone=models.IntegerField(default=0)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=10,null=True,blank=True)

    def gen_otp(self):
        otp_no=str(randint(1000,9999))+str(self.id)
        self.otp=otp_no
        self.save()
