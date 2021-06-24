import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.db.models import Q

from .models import Inventory
from .forms import InventoryForm
from business.models import Business
from business.views import get_user_permissions

# Get all index or pertaining to a business with query 
def index(request, *args, **kwargs):
    # Get query value or set it to empty
    print(args, kwargs)
    business_name =''
    if kwargs:
        # Set business name to business name received from kwargs
        business_name = kwargs["business_name"].lower()
    try:
        query = request.GET['query'].strip().lower()
    except Exception:
        query = ""
    # If no query value return all
    if not query:
        if business_name:
            try:
                index = Inventory.objects.filter(business__name = business_name)
            except Exception:
                index = Inventory.objects.all()
        else:
            index = Inventory.objects.all()
    # Return item with query name or business with query name
    else:
        if business_name:
            index = Inventory.objects.filter(business__name = business_name, name__icontains = query)
        else :
            index = Inventory.objects.filter( Q(name__icontains = query) | Q(business__name__icontains = query))
    business_id = None
    if business_name and index:
        business_id = index[0].business.id
    paginator = Paginator(index, 10) # Show 10 items per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'page_obj': page_obj,
        # 'index':index,
        'business_name': business_name,
        'business_id': business_id
    }
    return render(request,"inventory/index.html", context)


# Get Business Inventory pagnated in json 
@login_required(login_url = 'user:login')
def business_inventory(request,business_name,query,page_number):
    business_name = business_name.lower()
    # Check if business exists
    try:
        business = Business.objects.get(name = business_name)
    except Business.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        query = query.lower()
        if query == "all":
            inventory = Inventory.objects.filter(business=business)
        else:
            inventory = Inventory.objects.filter(business=business).filter(name__contains=query)
        p = Paginator(inventory, 4)
        all_inventory = p.get_page(page_number)
        if all_inventory.has_next():
            next_page = all_inventory.number + 1
        else:
            next_page = 0
        if all_inventory.has_previous():
            prev_page = all_inventory.number - 1
        else:
            prev_page = 0
        return JsonResponse([[item.serialize() for item in all_inventory],[{
                "has_next": all_inventory.has_next() ,
                "has_previous":all_inventory.has_previous(),
                "number":all_inventory.number, 
                "num_pages":all_inventory.paginator.num_pages,
                "next_page_number":next_page,
                "previous_page_number":prev_page,

            }]],safe=False)  
    return HttpResponse(status=403)
    
# Display individual inventory
def inventory(request, inventory_id):
    inventory = Inventory.objects.get(id = inventory_id)
    context={
        "inventory":inventory,
    }
    return render(request, "inventory/inventory.html", context)

@login_required(login_url = 'user:login')
def inventory_management(request,business_name):
    business_name = business_name.lower()
    display = "body"
    error_messages = []
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
    except Business.DoesNotExist:
        raise Http404
        
    # Check if user is an employee and get permissions
    is_employee,permissions = get_user_permissions(request.user,business)

    if not is_employee:      
        # message = "You do not have access to this page"
        # return render(request,"theSP/error.html",context={"message":message})
        raise Http404

    if not "creator_access" in permissions and not "manage inventory" in permissions:
        # message = "You do not have access to this page"
        # return render(request,"theSP/error.html",context={"message":message})
        raise Http404

    if request.method == "POST":
        try:
            inventory_id = request.POST["id"]
        except:
            inventory_id = None

        # If no id was passed then request was from new inventory form
        if not inventory_id:
            print("new inventory save")
            display = "form"
            form = InventoryForm(request.POST, request.FILES)
            if form.is_valid():  
                try:
                    new_inventory = Inventory.objects.create(
                        business=business,
                        type = "service",
                        name = form.cleaned_data["name"],
                        description = form.cleaned_data["description"],
                        price = float(form.cleaned_data["price"]),
                        unit = form.cleaned_data["unit"],
                        image = form.cleaned_data["image"],
                        serviced_item = form.cleaned_data["serviced_item"]
                    )
                    new_inventory.save()
                    return HttpResponseRedirect(reverse('inventory:inventory_management',kwargs={'business_name':business_name}))
                except Exception as e:
                    # print("new inventory save failed", e)
                    error_messages.append(e)      
            else:
                print("errors in form", form.errors)
                for fields in form:
                    for error in fields.errors:
                        error_messages.append(error.capitalize())


        # If id was passed request was from edit inventory form
        else:
            print("alter inventory details")
            
            inventory_id = request.POST["id"]
            new_name = request.POST["name"]
            new_price = request.POST["price"]
            new_unit = request.POST["unit"]
            new_description = request.POST["description"]
            new_image = request.FILES.get('new_image',False)
            

            inventory = Inventory.objects.get(business = business, id = inventory_id)
            inventory.price = new_price
            inventory.unit = new_unit
            inventory.name = new_name
            inventory.description = new_description
            if new_image:
                        if inventory.image:
                            # Delete old logo
                            try:
                                os.remove(inventory.image.path)
                            except:
                                print("couldn't remove old image")
                        inventory.image = new_image
            inventory.save()
            return HttpResponse(status = 200)

    elif request.method == "DELETE":    
        try:
            data = json.loads(request.body)
            id = data['id']
            # Delete inventory
            inventory = Inventory.objects.get(business = business,id = id)
            inventory.delete()
            return HttpResponse(status = 200)
        except Exception as e:
            # print(e)
            return HttpResponse( status = 403)
    
    context = {
        "page":"inventory",
        "display":display,
        "business":business,
        "permissions":permissions,
        "form":InventoryForm(),
        "error_messages":error_messages
    }

    return render(request, "inventory/inventory_admin.html", context)

