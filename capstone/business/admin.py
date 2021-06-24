from django.contrib import admin

from .models import Business, Employee, BusinessPermissions, BusinessPosition

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name','creator')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('business', 'employee', 'position')

class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('business', 'position', 'allowed')

class PositionsAdmin(admin.ModelAdmin):
    list_display = ('business', 'position')


admin.site.register(Business, BusinessAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(BusinessPermissions, PermissionsAdmin)
admin.site.register(BusinessPosition, PositionsAdmin)
