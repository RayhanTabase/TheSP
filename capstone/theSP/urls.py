from django.urls import path
from . import views

app_name = "theSP"

urlpatterns = [
    path('home/', views.home, name="home_query"),
]