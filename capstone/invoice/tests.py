from django.test import TestCase, Client
# from django.core.files.uploadedfile import SimpleUploadedFile

from user.models import User
from business.models import Business, Employee
from inventory.models import Inventory
from .models import Invoice, InvoiceItem

HOST = "http://127.0.0.1:8000"
# SMALL_GIF =  (
#     b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
#     b'\x01\x0a\x00\x01\x00\x01\x00\x2c\x00\x00\x02\x00\x02\x00\x00\x02'
#     b'\x02\x4c\x01\x00\x3b'
# )
# # TEST_PICTURE = SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif')

# Test Models
class InvoiceTest(TestCase):
    def setUp(self):
        self.client = Client()

        #Create user
        User.objects.create_user(
            username ="user1",
            password ="userpassword",
            first_name = "Kofi",
            last_name = "Aban",
            other_names = "Wood" ,
            email ="KofiAb@wood.com",
            country_code ="233", 
            phone_number ="123456789",
            profile_picture="test_image.jpg",
        )
        user = User.objects.get(username = "user1")
        
        # Create Business
        Business.objects.create(
            creator = user,
            name = "Business One",
            logo = "test_image.jpg",
            country_code = "233",
            phone = "125466789",
            email = "thebus@thebus.com",
            location =  "somewhere",
            description = "a business"
        )
        business = Business.objects.all().first()

        # Create Inventory
        Inventory.objects.create(     
            business = business,
            type = "service",
            name = "inventory 1",
            description = "some description",
            price = 111.11,
            unit = "hour",
            image = "test_image.jpg",
            serviced_item = True 
        )
        Inventory.objects.create(     
            business = business,
            type = "service",
            name = "inventory 2",
            description = "some description",
            price = 222.22,
            unit = "day",
            image = "test_image.jpg",
            serviced_item = False 
        )

        # Create Invoice
        employee = Employee.objects.get(employee = user)
        sales_agent = employee
        invoice = Invoice.objects.create(
            business = business,
            sales_agent = sales_agent,
            customer_name = "Customer",
            customer_contact = "026544435677",
            employee_created = True
        )
        
        items = Inventory.objects.all()
        item1 = items[0]
        item2 = items[1]
        InvoiceItem.objects.create(
            invoice = invoice,
            inventory = item1,
            quantity = 3,
        )
        InvoiceItem.objects.create(
            invoice = invoice,
            inventory = item2,
            quantity = 3,
        )

      
    def test_invoice_database(self):
        '''Check if inventory exists in database'''
        try:
            invoice = Invoice.objects.get(id=1)
        except Invoice.DoesNotExist:
            raise Exception("error in inventory database")
        self.assertEqual(len(invoice.items.all()),2)
        self.assertEqual(float(invoice.total_cost), 999.99)
        self.assertFalse(invoice.paid)
        self.assertTrue(invoice.customer_name == "Customer")
        self.assertTrue(invoice.customer_contact == "026544435677")
        self.assertTrue(invoice.employee_created)

    # Test urls
    def test_create_page(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/business/business one/invoices/create/")
        self.assertEqual(response.status_code, 200)

    def test_manage_invoice_page(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/business/Business One/manage_invoice/1/")
        self.assertEqual(response.status_code, 200)

    def test_index_invoice_page(self):
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/business/Business One/index_invoices/")
        self.assertEqual(response.status_code, 200)
    
    def test_user_estimate_page(self):
        response = self.client.get("/business/Business One/user_estimate/")
        self.assertEqual(response.status_code, 200)
        
 