from django import forms

from .models import Invoice, InvoiceItem

class InvoiceForm(forms.ModelForm): 
    class Meta:
        model = Invoice
        fields = ('customer','customer_name',)
        