import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Business, Employee, BusinessPermissions, BusinessPosition
from .forms import BusinessForm , BusinessEditForm
from user.models import User

# Returns a bool of whether user is an employee and also returns a list of permissions allowed that employee
def get_user_permissions(user,business):
    is_employee = False
    # Set permissions to none
    permissions = []
    
    # Check if creator
    if business.creator == user:
        # All access
        permissions.append("creator_access")
        is_employee = True
    else:
        # Get user permissions
        # Check if employee and find position
        try:
            employee = Employee.objects.get(business = business, employee = user)
            is_employee = True
            employee_position = employee.position
            employee_permissions = BusinessPermissions.objects.filter(position=employee_position)

            # Get all permissions assigned to the position
            permissions = [employee.allowed for employee in employee_permissions]
        except Exception as e:
            print(e)

    return (is_employee, permissions)

# View all business related to use; created or employed
@login_required(login_url = 'user:login')
def user_businesses(request):
    display = "body"
    error_messages = []

    # Trying to create new business
    if request.POST:
        display = "form"
        # Limit Businesses to 2
        user_businesses = Business.objects.filter(creator=request.user)
        # Business limit of 2 per user
        if len(user_businesses) < 2:
            form = BusinessForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    new_business = Business()
                    new_business.creator = request.user
                    new_business.name = form.cleaned_data['name'] 
                    new_business.logo = form.cleaned_data['logo']
                    new_business.country_code = form.cleaned_data['country_code']
                    new_business.phone = form.cleaned_data['phone']
                    new_business.email = form.cleaned_data['email']
                    new_business.location = form.cleaned_data['location']
                    new_business.description = form.cleaned_data['description']
                    new_business.save()

                    return HttpResponseRedirect(reverse('business:business_admin', kwargs={
                        'business_name':new_business.name ,
                        'page':'profile'
                    }))
                except Exception as e:
                    error_messages.append(e)
            else:
                for field in form:   
                    for error in field.errors:   
                        error_messages.append(error.capitalize())
        else:
            error_messages.append("2 businesses limit exceeded")

    context={
        "page":"business" ,  
        "error_messages":error_messages,  
        "display":display,  
        "form": BusinessForm(initial={
            "country_code":"233"
        }),
    }
    return render(request, "business/user_businesses.html", context)

# Direct to business profile page or employee management page
@login_required(login_url = 'user:login')
def business_admin(request, business_name, page):
    page = page.lower()
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
    except Business.DoesNotExist:
        raise Http404
        
    # Check if user is an employee and get permissions
    is_employee,permissions = get_user_permissions(request.user,business)

    if not is_employee:      
        message = "You do not have access to this business"
        return render(request,"theSP/error.html",context={"message":message})

    context = {
            "business":business, 
            "permissions": permissions,
            "page":page
    }

    if page == "profile": 
        context["display"] = "body"
        form = BusinessEditForm(initial={
            "name":business.name,
            "country_code":"233",
            "phone":business.phone,
            "email":business.email,
            "location":business.location,
            "description":business.location
        })  
        
        error_messages = []
        if request.POST:
            if not business.creator == request.user:
                raise Http404
            context["display"] = "form"
            form = BusinessEditForm(request.POST, request.FILES)
            # name = form['name'].errors
            if form.is_valid():
                try: 
                    business.name = form.cleaned_data['name']
                    new_logo = request.FILES.get('change_logo',False)
                    if new_logo:
                        if business.logo:
                            # Delete old logo
                            try:
                                os.remove(business.logo.path)
                            except:
                                print("couldn't remove old image")
                        business.logo = new_logo
                    business.country_code = form.cleaned_data['country_code']
                    business.phone = form.cleaned_data['phone']
                    business.email = form.cleaned_data['email']
                    business.location = form.cleaned_data['location']
                    business.description = form.cleaned_data['description']
                    business.save()

                    return HttpResponseRedirect(reverse('business:business_admin', kwargs={
                        'business_name': business.name,
                        'page': "profile"
                    }))
                except Exception as e:
                    print(e)
                    error_messages.append(e)
            else:
                print("invalid", form.errors)
                for field in form:   
                    for error in field.errors:   
                        error_messages.append(error.capitalize())

        context['form'] = form 
        context["error_messages"] = error_messages
        return render(request, "business/profile.html", context)

    elif page == "employee_management":
        if "creator_access" in permissions or "manage employees" in permissions:
            return render(request, "business/employee_management.html", context)
    raise Http404

# Returns Employee data in json and also saves new employee data and edits existing employee data
@login_required(login_url = 'user:login')
def employees(request,business_name,query,page_number):
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
        print("business exists")
    except Business.DoesNotExist:
        return HttpResponse(status=404)

    # Check if user is an employee and get permissions
    is_employee,permissions = get_user_permissions(request.user,business)

    if is_employee:
        if "creator_access" in permissions or "manage employees" in permissions:
            # Get all employees
            if request.method == "GET":
                query = query.lower()

                # Exclude user as employee
                if query == "all":
                    employees = Employee.objects.filter(business = business).exclude(employee = request.user)
                else:
                    employees = Employee.objects.filter(business=business).filter(
                        Q(employee__first_name__icontains = query) |
                        Q(employee__last_name__icontains = query) |
                        Q(employee__other_names__icontains = query) |
                        Q(name__icontains = query)
                    ).exclude(employee = request.user)
                    print(employees)            
                paginator = Paginator(employees, 10) # Show 10 items per page.
                all_employees = paginator.get_page(page_number)

                if all_employees.has_next():
                    next_page = all_employees.number + 1
                else:
                    next_page = 0
                if all_employees.has_previous():
                    prev_page = all_employees.number - 1
                else:
                    prev_page = 0
                return JsonResponse([[employee.serialize() for employee in all_employees],[{
                    "has_next": all_employees.has_next() ,
                    "has_previous":all_employees.has_previous(),
                    "number":all_employees.number, 
                    "num_pages":all_employees.paginator.num_pages,
                    "next_page_number":next_page,
                    "previous_page_number":prev_page,

                }]],safe=False) 

            # Add new employee
            elif request.method == "POST":
                try:
                    data = json.loads(request.body)
                    employee_username = data["employee_username"].lower()
                    username = employee_username
                    print("add",username)
                    user = User.objects.get(username=username)
                    new_employee = Employee(business=business,employee=user)
                    new_employee.save()
                    return HttpResponse(status=200)
                except IntegrityError:
                    print("user already exists")
                except User.DoesNotExist:
                    print("username does not exist")

            # Change employee position
            elif request.method == "PUT":
                try:
                    data = json.loads(request.body)
                    employee_id = data["employee_id"] 
                    position = data["position"].lower
                    employee = Employee.objects.get(business=business ,id = employee_id)

                    if position == "none":
                        employee.position = None
                    else:
                        new_position = BusinessPosition.objects.get(business=business, position=position)
                        employee.position = new_position
                    employee.save()
                    return HttpResponse(status=200)
                except Exception as e:
                    print(e)
            
            # Remove/delete employee
            elif request.method == "DELETE":
                print("deleting employee")
                try:
                    data = json.loads(request.body)
                    employee_id = data["employee_id"]
                    employee = Employee.objects.get(business=business,id=employee_id)
                    if employee.employee != business.creator:
                        employee.delete()
                        return HttpResponse(status=200)
                    else:
                        return HttpResponse(status=403)
                except Exception as e:
                    print(e)
               
    return HttpResponse(status=404)
                
# Returns company positions and manages positions and permissions(saves and edit)                    
@login_required(login_url = 'user:login')
def positions(request,business_name):
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
        print("business exists")
    except Business.DoesNotExist:
        return HttpResponse(status=404)

    # Check if user is an employee and get permissions
    is_employee,permissions = get_user_permissions(request.user,business)

    if is_employee:
        if "creator_access" in permissions or "manage employees" in permissions:
            print("access granted")
            if request.body:
                data = json.loads(request.body)

            if request.method == "GET":
                if "creator_access" in permissions:
                    positions = BusinessPosition.objects.filter(business = business)
                else:
                    # Exclude employees position
                    employee = Employee.objects.get(employee = request.user)
                    positions = BusinessPosition.objects.filter(business = business).exclude(position = employee.position)

                return JsonResponse([position.serialize() for position in positions],safe=False)
                
            elif request.method == "POST":
                try:   
                    position = data["position"].lower()
                    new_position = BusinessPosition(business=business,position=position)
                    new_position.save()
                    return HttpResponse(status=200)

                except Exception:
                    print("position already exists")

            elif request.method == "PUT":
                if data["action"] == "add":
                    try: 
                        position = data["position"]
                        permission = data["permission"]
                        position = BusinessPosition.objects.get(business = business, position=position) 
                        new_permission = BusinessPermissions(business=business, position=position, allowed=permission)
                        new_permission.save()  
                        return HttpResponse(status=200)

                    except Exception:
                        print("Could not add permission")

                elif data["action"] == "revoke":
                    try:
                        position = data["position"]
                        permission = data["permission"]
                        position = BusinessPosition.objects.get(business = business, position=position) 
                        permission = BusinessPermissions.objects.get(business=business, position=position, allowed=permission)
                        permission.delete()
                        return HttpResponse(status=200)
                    except Exception:
                        print("Could not delete permission")

            elif request.method == "DELETE":
                print(data)
                try:
                    position = data["position"]
                    print(position)
                    position = BusinessPosition.objects.get(business = business, position=position)  
                    position.delete()     
                    return HttpResponse(status=200)   
                except Exception:
                    print("Could not delete position")
    return HttpResponse(status=404)


