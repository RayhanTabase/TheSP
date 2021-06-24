from django.urls import path
from . import  views

app_name = "business"
urlpatterns =[
    path('user/businesses/', views.user_businesses, name="user_businesses"),
    path("business/<str:business_name>/admin/<str:page>/", views.business_admin, name="business_admin"),

    #API REQUESTS 
    path("business/<str:business_name>/employee_management/employees/<str:query>/<int:page_number>/", views.employees , name = "employees"),
    path("business/<str:business_name>/employee_management/positions/", views.positions, name="positions"),
]