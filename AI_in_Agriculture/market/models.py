from django.db import models
from django.contrib.auth.models import User


class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.user.username


class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name