from django.contrib import admin

from .models import Invoice, InvoiceItem, ServicedItem, RejectedItem

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["business_name","id","customer_name","total_cost","paid"]


class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ["invoice","inventory_name","quantity"]
    actions = ["really_delete_selected"]

    def get_actions(self, request):
        actions = super(InvoiceItemAdmin,self).get_actions(request)
        del actions["delete_selected"]
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
            obj.invoice.calc_total_payment()
        if queryset.count() == 1:
            message_bit = " 1 invoice item"
        else:
            message_bit = f" {queryset.count} invoice items"
        self.message_user(request,f" successfully deleted {message_bit}")

    really_delete_selected.short_description = "Delete selected entries"

admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(ServicedItem)
admin.site.register(RejectedItem)

