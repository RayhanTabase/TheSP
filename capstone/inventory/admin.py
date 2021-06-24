from django.contrib import admin

from .models import Inventory

class InventoryAdmin(admin.ModelAdmin):
    list_display = ["business","type","name","price","unit"]

admin.site.register(Inventory, InventoryAdmin)
