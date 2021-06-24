from django.forms import widgets
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import Invoice, InvoiceItem

class InvoiceResource(resources.ModelResource): 
    id = Field(attribute="id", column_name = "INVOICE ID")
    customer_name = Field(attribute="customer_name", column_name = "CUSTOMER NAME")
    customer_contact = Field(attribute="customer_contact", column_name = "CUSTOMER CONTACT")
    invoice_discount = Field(attribute="invoice_discount", column_name = "DISCOUNT")
    total_cost = Field(attribute="total_cost", column_name = "TOTAL")
    paid = Field(attribute="paid", column_name = "PAID")
    timestamp = Field(attribute="timestamp", column_name = "DATE", widget=DateWidget(format='%d/%B/%Y'))
    class Meta:
        model = Invoice
        clean_model_instances = True
        fields = ('id','customer_name','customer_contact','invoice_discount','total_cost','paid','timestamp')
        export_order = ('id','customer_name','customer_contact','invoice_discount','total_cost','paid','timestamp')

    def dehydrate_paid(self,invoice):
        paid = "No"
        if invoice.paid:
            paid = "Yes"
        return paid

    def get_queryset(self):
        return self._meta.model.objects.order_by('timestamp')

class InvoiceItemsResource(resources.ModelResource): 
    unit_price = Field()
    total = Field()
    customer = Field()
    contact = Field()
    class Meta:
        model = InvoiceItem
        clean_model_instances = True
        fields = ('invoice','inventory_name','quantity')
        export_order = ('invoice','customer','contact','inventory_name','unit_price','quantity','total')


    def dehydrate_unit_price(self,invoiceItem):
        return invoiceItem.inventory.price
    
    def dehydrate_total(self,invoiceItem):
        return (float(invoiceItem.inventory.price) * float(invoiceItem.quantity))
    
    def dehydrate_customer(self,invoiceItem):
        return invoiceItem.invoice.customer_name
    
    def dehydrate_contact(self,invoiceItem):
        return invoiceItem.invoice.customer_contact

