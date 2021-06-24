from django.urls import path
from . import views


app_name = "inventory"
urlpatterns = [
    path("", views.index, name="index"),
    path("index/<str:business_name>/", views.index, name="index_business"),
    path("inventory/<int:inventory_id>/", views.inventory, name="inventory"),
    path("business/<str:business_name>/inventory_management/", views.inventory_management, name="inventory_management"),
    
    # API get json of business inventory
    path("business/<str:business_name>/inventory/<str:query>/<str:page_number>/", views.business_inventory, name="business_inventory"),
]