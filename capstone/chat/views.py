from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import json
from business.models import Business, Employee
from business.views import get_user_permissions
from .models import Room, RoomMessage


@login_required(login_url = 'user:login')
def business_chat(request,business_name):
    business = Business.objects.get(name=business_name)
    context={
        "business":business,
    }
    return render(request,"chat/chat.html",context)

@login_required(login_url = 'user:login')
def admin_business_chat(request,business_name):
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
    except Business.DoesNotExist:
        raise Http404
        # Incase of javascript fetch 
        return HttpResponse(status=403)

    is_employee,permissions = get_user_permissions(request.user,business)

    if not is_employee:      
        raise Http404
        # Incase of javascript fetch 
        return HttpResponse(status=403)

    if "creator_access" in permissions:
        employee_id = "creator"
    else:
        employee = Employee.objects.get(business = business, employee = request.user)
        employee_id = employee.id
    
    business = Business.objects.get(name=business_name)
    context={
        "business":business,
        "page":"chat",
        "permissions":permissions,
        "employee_id":employee_id
    }
    return render(request,"chat/admin_chat.html",context)


@login_required(login_url = 'user:login')
def get_rooms(request,business_id):
    try:
        business = Business.objects.get(id = business_id)
    except Business.DoesNotExist:
        return HttpResponse(status=403)

    is_employee,permissions = get_user_permissions(request.user,business)

    if not is_employee:      
        return HttpResponse(status=403)
    rooms = Room.objects.filter(business_id = business_id).order_by("-pk")
    return JsonResponse([room.serialize() for room in rooms],safe=False) 


@login_required(login_url = 'user:login')
def get_messages(request,room_name):
    room = Room.objects.get(room_name = room_name)

    if room.customer == request.user:
        room_messages = RoomMessage.objects.filter(room = room).order_by("pk")
        return JsonResponse([message.serialize() for message in room_messages],safe=False)  

    business = room.business
    is_employee,permissions = get_user_permissions(request.user,business)

    if not is_employee:       
        return HttpResponse(status=403)

    room_messages = RoomMessage.objects.filter(room = room).order_by("-pk")
    return JsonResponse([message.serialize() for message in room_messages],safe=False)  

    


