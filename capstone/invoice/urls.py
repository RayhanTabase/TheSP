from django.urls import path
from . import views

app_name = "invoice"
urlpatterns =[
    path("business/<str:business_name>/invoices/create/", views.create_invoice, name="create"),
    path("business/<str:business_name>/manage_invoice/<int:invoice_id>/", views.manage_invoice, name="manage_invoice"),
    path("business/<str:business_name>/index_invoices/", views.index_invoices, name="invoices_index"),
    path("business/<str:business_name>/user_estimate/", views.user_estimate, name="user_estimate"),
]