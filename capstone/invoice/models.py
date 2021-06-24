import os
from django.db import models
from django.urls import reverse
# from datetime import date, datetime, time, timedelta

from business.models import Business, Employee
from user.models import User
from inventory.models import Inventory


# class CustomerEstimateInvoice(models.Model):
#     business
#     customer
#     customer_comments
#     items

#     business_comment
#     estimate

# class CustomerEstimateItem(models.Model):
#     customerestimate_invoice
#     item
#     image


class Invoice(models.Model):
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, related_name="sale_invoices")
    business_name = models.CharField(max_length=30, blank=True)
    sales_agent = models.ForeignKey(Employee, on_delete = models.SET_NULL, null=True, related_name="created_invoices")
    sales_agent_name = models.CharField(max_length=30, blank=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_invoices")
    customer_name = models.CharField(max_length=30, blank=True)
    customer_contact =  models.CharField(max_length=30, blank=True, null=True)
    total_cost = models.DecimalField(decimal_places=2,max_digits=12, blank=True, null=True)
    invoice_discount = models.DecimalField(decimal_places=2,max_digits=12, default=0)
    employee_created = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp','paid']

    def __str__(self):
        if self.paid:
            payment_status = "paid"
        else:
            payment_status = "unpaid"
        return f"{self.business.name.upper()}[{self.id}] ( {payment_status} )" 

    def get_absolute_url(self):
        return reverse("invoice:manage_invoice",kwargs={
            "business_name":self.business.name,
            "invoice_id":self.id
        })

    def save(self,*args, **kwargs):
        self.business_name = self.business.name
        if self.employee_created:
            #Check sales agent
            if self.sales_agent in self.business.employees.all():
                self.sales_agent_name = self.sales_agent.employee.first_name + " " + self.sales_agent.employee.last_name  
            else:
                raise Exception("Employee is not part of this business")
        else:
            self.sales_agent = None
            self.sales_agent_name = "Created by customer"

        if self.customer:
            self.customer_name = self.customer.first_name + " " + self.customer.last_name 
            if not self.customer_contact:
                self.customer_contact = self.customer.phone_number
        else:
            if not self.customer_name:
                raise Exception("you must provide a customer name")

        super().save(*args, **kwargs)

    #Calculate the total cost of all items minus discount
    def calc_total_payment(self):
        # Check if invoice has been paid first
        if not self.paid:
            items = InvoiceItem.objects.filter(invoice = self)
            total = 0
            for item in items:
                total += item.inventory.price * item.quantity
            if self.invoice_discount:
                total = float(total) - float(self.invoice_discount)

            self.total_cost = total
            self.save()

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete = models.CASCADE, related_name="items")
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True,)
    inventory_name = models.CharField(max_length=30, blank=True)
    quantity = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now=True)
    total = models.DecimalField(decimal_places=2,max_digits=12, default=0,blank=True)
    # If laundry or similar type invoice image of customers item
    image = models.ImageField(null=True,blank=True,upload_to="invoice/customer_items") 
    serviced_item_image_check = models.BooleanField(blank = True, default=False)
    serviced_item_finished = models.BooleanField(blank = True, default=False)

    class Meta:
        ordering = ['invoice','-timestamp']

    def __str__(self):
        return "Invoice: " + str(self.invoice.id) + " Item: " + self.inventory.name

    def save(self,*args, **kwargs):
        self.image = None
        # Only serviced items should have image on invoice
        if self.inventory.serviced_item:
            if self.image:
                self.image.upload_to = f"invoice/customer_items/{self.invoice.id}"

        # Check if invoice has been paid first
        if self.invoice.paid:
            return False

        # Make sure to save only inventory from the business
        business = Business.objects.get(name = self.invoice.business_name)
        if not self.inventory in business.inventory.all():
            raise Exception("Inventory not offered by this business")

        # Check if product item already exist in invoice
        if self.inventory.type == "product":
            # If product already exists then increase quantity
            try:
                print("increased quantity of invoice item")
                invoice_item = InvoiceItem.objects.get(invoice=self.invoice,inventory=self.inventory)
                invoice_item.quantity += self.quantity
                self.total = self.quantity * self.inventory.price
                # To avoid a recursive loop
                invoice_item.mod_save() 
            # Add new product
            except InvoiceItem.DoesNotExist:
                print("add new product to invoice")
                self.inventory_name = self.inventory.name
                self.total = self.quantity * self.inventory.price
                super().save(*args, **kwargs)
                # Calculate invoice total
                self.invoice.calc_total_payment()          
        else:
            self.inventory_name = self.inventory.name
            self.total = self.quantity * self.inventory.price
            super().save(*args, **kwargs)
            # Calculate invoice total
            self.invoice.calc_total_payment()

    # To avoid a recursive loop 
    def mod_save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        # Calculate invoice total
        self.invoice.calc_total_payment()


    def delete(self, *args, **kwargs):
        self.quantity = 0
        super().save(*args, **kwargs)
        self.invoice.calc_total_payment()
        super().delete()

class ServicedItem(models.Model):
    invoice_item = models.OneToOneField(InvoiceItem, on_delete=models.CASCADE, limit_choices_to={
        "inventory__serviced_item":"True"
    })
    serviced_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    employee_name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(null=True,blank=True,upload_to="invoice/customer_items") 

    def save(self,*args, **kwargs):
        # Image save location
        if self.image:
            self.image.upload_to = f"invoice/customer_items/{self.invoice_item.invoice.id}/image_check"

        self.employee_name = self.serviced_by.employee.first_name + " " + self.serviced_by.employee.last_name
        
        # Make sure the employee is part of the business
        if not self.serviced_by in self.invoice_item.invoice.business.employees.all():
            raise Exception("Employee is not part of this business")

        super().save(*args, **kwargs)

    def delete(self):
        if self.image:
            os.remove(self.image.path)
        super().delete()

class RejectedItem(models.Model):
    invoice_item = models.OneToOneField(InvoiceItem, on_delete=models.CASCADE, limit_choices_to={
        "inventory__serviced_item":"True"
    })
    reason = models.TextField()
    rejected_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    employee_name = models.CharField(max_length=30, blank=True)


    def save(self,*args, **kwargs):
        self.employee_name = self.serviced_by.employee.first_name + " " + self.serviced_by.employee.last_name
        
        # Make sure the employee is part of the business
        if not self.serviced_by in self.invoice_item.invoice.business.employees.all():
            raise Exception("Employee is not part of this business")

        super().save(*args, **kwargs)
      




            

