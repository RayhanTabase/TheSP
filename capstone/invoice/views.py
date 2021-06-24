from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from datetime import date
from django.core.paginator import Paginator

from business.models import Business,Employee
from business.views import get_user_permissions
from inventory.models import Inventory
from user.models import User
from .models import Invoice, InvoiceItem

from .resources import InvoiceResource, InvoiceItemsResource


@login_required(login_url = 'user:login')
def create_invoice(request,business_name):
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

    if not "creator_access" in permissions and not "make sales" in permissions:
        raise Http404
        # Incase of javascript fetch 
        return HttpResponse(status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        items = data['invoice_items']
        customer_username = data['customer_username']
        customer_name = data['customer_name']
        customer_contact = data['customer_contact']
        discount = data['discount']
        
        if data['employee_created']:
            try:
                new_invoice = Invoice()
                new_invoice.business = business
                new_invoice.employee_created = True
                try:
                    new_invoice.sales_agent = Employee.objects.get(business=business, employee=request.user)
                except Exception:
                    if business.creator == request.user:
                        new_employee = Employee()
                        new_employee.business = business
                        new_employee.employee = request.user
                        new_employee.save()
                        new_invoice.sales_agent = new_employee
                    else:
                        raise Exception("Permission not granted")
                if customer_username:
                    user = User.objects.get(username=customer_username)
                    new_invoice.customer = user
                else:
                    new_invoice.customer_name = customer_name
                new_invoice.customer_contact = customer_contact

                new_invoice.invoice_discount = discount #this should be changed to handle decimals
                new_invoice.save()
            
                for item in items:
                    new_invoice_item = InvoiceItem() 
                    new_invoice_item.invoice = new_invoice
                    new_invoice_item.inventory = Inventory.objects.get(id = item['id'] )
                    new_invoice_item.quantity = item['quantity']
                    new_invoice_item.save()

                return JsonResponse({"invoice_id":new_invoice.id},safe=False)
            except Exception as e:
                print("error",e)
        else:
            invoice = Invoice()
            invoice.business = business
            invoice.username = customer_username
            invoice.employee_created = False
            invoice.save()

            for item in items:
                    new_invoice_item = InvoiceItem() 
                    new_invoice_item.invoice = invoice
                    new_invoice_item.inventory = Inventory.objects.get(id = item['id'] )
                    new_invoice_item.quantity = item['units']
                    new_invoice_item.save()
            return HttpResponse(status=200)

        return HttpResponse(status=404)

    context = {
        "business":business,
        "permissions":permissions,
        "page":"sales"
    }
    return render(request, "invoice/create.html",context)

 


@login_required(login_url = 'user:login')
def manage_invoice(request,business_name,invoice_id):
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
    except Business.DoesNotExist:
        raise Http404
        # Incase of javascript fetch 
        return HttpResponse(status=403)
        
    # Check employee permission
    is_employee,permissions = get_user_permissions(request.user,business)

    if is_employee:
        if "creator_access" in permissions or "make_sales" in permissions:
            invoice = Invoice.objects.get(business__name = business_name, id = invoice_id)

            if request.method == "POST":
                invoice.paid = True
                invoice.sales_agent = Employee.objects.get(business=business, employee=request.user)
                invoice.save()
                return HttpResponse(status = 200)
            
            if request.method == "DELETE":
                invoice.delete()
                return HttpResponse(status = 200)
            
            elif request.method == "GET":
                extract = False
                try:
                    print(request.GET["extract_csv"] )
                    if int(request.GET["extract_csv"]) == 1:
                        extract = True
                except:
                    pass
            
                if extract:
                    filename = f"invoice-{invoice.customer_name}.csv"
                    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
                    invoice_items_resource = InvoiceItemsResource()
                    dataset = invoice_items_resource.export(invoice_items)
                    response =  HttpResponse(dataset.csv, content_type = 'text/csv')
                    response['Content-Disposition'] = f'attachment; filename={filename}'
                    return response
                context ={
                    "invoice":invoice,
                    "business":business
                }
                return render(request,'invoice/manage_invoice.html',context)
    raise Http404

@login_required(login_url = 'user:login')
def index_invoices(request,business_name,my_page=False):
    business_name = business_name.lower()
    try:
        business = Business.objects.get(name = business_name)
    except Business.DoesNotExist:
        raise Http404

    is_employee,permissions = get_user_permissions(request.user,business)

    if not is_employee:      
        raise Http404

    if not "creator_access" in permissions and not "manage accounts" in permissions:
        raise Http404

    category = "all"
    date_from=""
    date_to=date.today()
    try:
        category = request.GET["category"].lower()
    except Exception as e:
        print("error",e)
    try: 
        print(request.GET["date-from"])
        # date_from = date(request.GET["date-from"])
        date_from = request.GET["date-from"]
    except Exception as e:
        print("error",e)
    try:
        date_to = request.GET["date-to"]
    except Exception as e:
        print("error",e)
    if category == "all":
        if date_from:
            invoices = Invoice.objects.filter(business = business, timestamp__date__range=(date_from, date_to))
        else:
            invoices = Invoice.objects.filter(business = business, timestamp__date__lte = date_to)
    elif  category == "paid":
        if date_from:
            invoices = Invoice.objects.filter(business = business, paid = True, timestamp__date__range=(date_from, date_to))
        else:
            invoices = Invoice.objects.filter(business = business, paid = True, timestamp__date__lte = date_to)
    elif  category == "unpaid":
        if date_from:
            invoices = Invoice.objects.filter(business = business, paid = False, timestamp__date__range=(date_from, date_to))
        else:
            invoices = Invoice.objects.filter(business = business, paid = False, timestamp__date__lte = date_to)
   
    extract = False
    try:
        print(request.GET["extract_csv"] )
        if int(request.GET["extract_csv"]) == 1:
            extract = True
    except:
        pass
  
    if extract:
        filename = f"invoices-{category}-{date_from}-{date_to}.csv"
        print(request.GET["extract_csv"])
        invoice_resource = InvoiceResource()
        dataset = invoice_resource.export(invoices)
        response =  HttpResponse(dataset.csv, content_type = 'text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename} '
        return response

    paginator = Paginator(invoices, 10) # Show 10 items per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context ={
        # "invoices":invoices,
        "page":"invoices",
        'page_obj': page_obj,
        "business":business,
        "category": category,
        "permissions":permissions,
        "date_to": date_to,
        "date_from": date_from
    }
    return render(request, 'invoice/index_invoices.html',context)

def user_estimate(request,business_name):
    business_name = business_name.lower()
    return render(request, 'invoice/user_estimate.html')