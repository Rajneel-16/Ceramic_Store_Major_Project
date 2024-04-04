from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Catagory(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    
    def __str__(self) -> str:
        return f"{self.name}"

class Product(models.Model):
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE,max_length=100)
    name=models.CharField(max_length=100)
    detaile=models.TextField(max_length=1000)
    image = models.ImageField(upload_to="kitchen",null=True)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10,decimal_places=3)
    def __str__(self) -> str:
        return f"{self.catagory} {self.name}"


class PurchaseDetaile(models.Model):
    username = models.CharField(max_length=100,blank=False)
    name = models.CharField(max_length=100,blank=False)
    length = models.DecimalField(max_digits=10,decimal_places=5)
    breadth = models.DecimalField(max_digits=10,decimal_places=5)
    area = models.DecimalField(max_digits=10,decimal_places=5)
    address=models.TextField(max_length=2000)