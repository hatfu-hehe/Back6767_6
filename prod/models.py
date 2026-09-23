from django.db import models
from users.models import CustomUser
from common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=155)
    
    def __str__(self):
        return self.name
    

class Product(BaseModel):
    title = models.CharField(max_length=155)
    description = models.TextField()
    price = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=((i, i * '* ') for i in range(1, 6)), default=5)
    
    def __str__(self):
        return f"prod rev"
    
    
