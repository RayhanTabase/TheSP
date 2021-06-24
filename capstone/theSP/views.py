from django.shortcuts import render

from inventory.models import Inventory

def home(request, query="all"):
    query = query.lower()
    'business_name'
    'service_name'
    if query == "all":
        index = Inventory.objects.all()
    else:
        index = Inventory.objects.filter(name__icontains = query)
    context ={
        "inventory": index
    }
    return render(request,"theSP/index.html", context)