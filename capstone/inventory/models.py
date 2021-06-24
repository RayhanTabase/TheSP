import os
from django.db import models
from django.urls import reverse

from business.models import Business

class Inventory(models.Model):
    TYPE = (
        ("product","PRODUCT"),
        ("service", "SERVICE")   
    )

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='inventory')
    type = models.CharField(max_length=10, choices=TYPE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=12)
    unit = models.CharField(max_length=15, default="other")
    image = models.ImageField(null=True,blank=True,upload_to="inventory")
    serviced_item = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business','name'],
                name='unique inventory name'

            )
        ]
        ordering = ["business","name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("inventory:inventory",kwargs={"inventory_id":self.id})
    
    def serialize(self):
        image = None
        if self.image:
            image = self.image.url 
        return {
            "id":self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description, 
            "price": self.price,    
            "unit":self.unit,
            "image":image,
            "url_page": self.get_absolute_url()
        }
        
    def save(self, *args, **kwargs):
        self.price = float(self.price)
        if not self.unit:
            self.unit = "other"
        # Products can't be serviced items
        if self.type == "product":
            self.serviced_item = False
        # Price must always be greater than 0
        if self.price <= 0:
            raise Exception("Price must be greater than zero")
            
        # save name in lowercase
        self.name = self.name.lower()
        super().save(*args, **kwargs)
        

    def delete(self):
        if self.image:
            os.remove(self.image.path)
        super().delete()
    