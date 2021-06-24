# from django.test import TestCase, Client
# from django.core.files.uploadedfile import SimpleUploadedFile

# from user.models import User
# from business.models import Business
# from .models import Inventory

# HOST = "http://127.0.0.1:8000"
# SMALL_GIF =  (
#     b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
#     b'\x01\x0a\x00\x01\x00\x01\x00\x2c\x00\x00\x02\x00\x02\x00\x00\x02'
#     b'\x02\x4c\x01\x00\x3b'
# )
# # TEST_PICTURE = SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif')

# # Test Models
# class InventoryTest(TestCase):
#     def setUp(self):
#         self.client = Client()

#         #Create user
#         User.objects.create_user(
#             username ="user1",
#             password ="userpassword",
#             first_name = "Kofi",
#             last_name = "Aban",
#             other_names = "Wood" ,
#             email ="KofiAb@wood.com",
#             country_code ="233", 
#             phone_number ="123456789",
#             profile_picture="test_image.jpg",
#         )
#         user = User.objects.get(username = "user1")
        
#         # Create Business
#         business = Business()
#         business.creator = user
#         business.name = "Business One"
#         business .logo = "test_image.jpg"
#         business.country_code = "233"
#         business.phone = "125466789"
#         business.email = "thebus@thebus.com"
#         business.location =  "somewhere"
#         business.description = "a business"
#         business.save()

#         # Create Inventory
#         Inventory.objects.create(     
#             business = business,
#             type = "service",
#             name = "new inventory",
#             description = "some description",
#             price = 111.11,
#             unit = "hour",
#             image = "test_image.jpg",
#             serviced_item = True 
#         )
#         Inventory.objects.create(     
#             business = business,
#             type = "service",
#             name = "other inventory",
#             description = "some description",
#             price = 222.22,
#             unit = "day",
#             image = "test_image.jpg",
#             serviced_item = False 
#         )
    
#     def test_inventory_database(self):
#         '''Check if inventory exists in database'''
#         try:
#             inventory = Inventory.objects.all()
#         except Exception:
#             raise Exception("error in inventory database")

#         self.assertEqual(len(inventory),2)

#     def test_index_view(self):
#         response = self.client.get("")
#         self.assertEqual(response.status_code, 200)

#         # test business index
#         response = self.client.get("/index/Business One/")
#         self.assertEqual(response.status_code, 200)

#     def test_inventory_view(self):
#         response = self.client.get("/inventory/1/")
#         self.assertEqual(response.status_code, 200)


#     def test_inventory_management_view(self):
#         # Test logged in access
#         self.client.login(username ="user1",password ="userpassword")
#         self.assertTrue(self.client.login(username ="user1",password ="userpassword"))
#         response = self.client.get("/business/Business One/inventory_management/")
#         self.assertEqual(response.status_code, 200)



    




