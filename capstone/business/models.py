from django.db import models
from django.urls import reverse

from user.models import User
import os

# Only signed in users can create a business
class Business(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    logo = models.ImageField(blank=True , null=True, upload_to="business/logo")
    country_code = models.CharField(max_length=30, blank=True, default="233") 
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    location =  models.TextField() 
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp","name"]

    def __str__(self):
        return f"{self.name} -{self.creator}"

    def save(self,*args, **kwargs):
        # Save all name in uppercase
        self.name = self.name.lower()  
        
        # Phone number must be atleast 9 digits 
        if len(self.phone) < 9 : 
            raise Exception("Phone number must be atleast 9 characters")

        super().save(*args, **kwargs)
        try:
            # Add creator to employees
            employee = Employee.objects.create(
                business = self,
                employee = self.creator
            )
            employee.save()
        except Exception as e:
            print("Not added creator to employees - ", e)


    def delete(self):
        if self.logo:
            try:
                os.remove(self.logo.path)
            except Exception:
                print("could not delete logo")
        super().delete()

    def get_absolute_url(self):
        return reverse("inventory:index_business",kwargs={"business_name":self.name})

    def get_admin_url(self):
        return reverse("business:business_admin",kwargs={"business_name":self.name, "page":"profile"})
    
class BusinessPosition(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="positions")
    position = models.CharField(max_length=30)

    class Meta:
        ordering = ("business",)
        constraints = [
            models.UniqueConstraint(
                fields=['business','position'],
                name='unique position'
            )
        ]

    def save(self,*args, **kwargs):
        self.position = self.position.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.position

    def serialize(self):
        permissions = BusinessPermissions.objects.filter(business=self.business, position=self)       
        return {
            "id":self.id,
            "name": self.position,
            "permissions": [permission.serialize() for permission in permissions]
        }


class Employee(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField(max_length=150, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employed")
    position = models.ForeignKey(BusinessPosition, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-business","-timestamp"]
        constraints = [
            models.UniqueConstraint(
                fields=['business','employee'],
                name='unique business employee'
            )
        ]

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name
    
    def save(self,*args, **kwargs):
        self.name = self.employee.first_name.lower() +" "+ self.employee.last_name.lower()
        super().save(*args, **kwargs)
          

    def serialize(self):
        if self.position:
            position = self.position.position
        else:
            position = "None"

        if self.employee.profile_picture:
            image = self.employee.profile_picture.url
        else:
            image = None
        return {
            "id":self.id,
            "name": self.employee.first_name +" "+self.employee.last_name,
            "image":image,
            "phone":self.employee.phone_number,
            "position": position,     
            "date_added":self.timestamp,
        }

# class EmployeeAssessment(models.Model):
#     business
#     employee
#     assessor
#     assessment
#     timestamp


class BusinessPermissions(models.Model):
    PERMISSIONS = (
        ('manage inventory','MANAGE INVENTORY'),
        ('make sales','MAKE SALES'),
        ('manage sales','MANAGE SALES'),
        ('access accounts', 'ACCESS ACCOUNTS'),
        ('manage accounts', 'MANAGE ACCOUNTS'),
        ('manage employees', 'MANAGE EMPLOYEES')
    )

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="permissions")
    position = models.ForeignKey(BusinessPosition, on_delete=models.CASCADE, related_name="position_permissions")
    allowed = models.CharField(max_length=30, choices=PERMISSIONS)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business','position','allowed'],
                name='unique employee permissions'
            )
        ]

    def serialize(self):
        return{
            "permission": self.allowed
        }
        

# class Log(models.Model):
#     action = models.CharField(max_length=10)
#     description = models.TextField()
#     user = models.CharField(max_length=150, choices=PERMISSIONS)
#     timestamp = models.DateTimeField(auto_now_add = True)
    
#     class Meta:
#         ordering = ["-timestamp"]
        
