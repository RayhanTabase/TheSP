# from django.test import TestCase, Client
# from django.core.files.uploadedfile import SimpleUploadedFile

# from user.models import User
# from .models import Business, Employee, BusinessPosition, BusinessPermissions
# from .views import get_user_permissions

# HOST = "http://127.0.0.1:8000"
# SMALL_GIF =  (
#     b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
#     b'\x01\x0a\x00\x01\x00\x01\x00\x2c\x00\x00\x02\x00\x02\x00\x00\x02'
#     b'\x02\x4c\x01\x00\x3b'
# )
# # TEST_PICTURE = SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif')

# # Test Models
# class BusinessTest(TestCase):
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
#         
#         user1 = User.objects.get(username = "user1")

#         user2 = User.objects.create(
#             username ="user2",
#             password ="userpassword",
#             first_name = "Ama",
#             last_name = "Aban",
#             other_names = "Wood" ,
#             email ="AmaAb@wood.com",
#             country_code ="233", 
#             phone_number ="335456783",
#             profile_picture="test_image.jpg",
#         )
#         user2.save()

#         # Create Business
#         business = Business()
#         business.creator = user1
#         business.name = "Business One"
#         business .logo = "test_image.jpg"
#         business.country_code = "233"
#         business.phone = "125466789"
#         business.email = "thebus@thebus.com"
#         business.location =  "somewhere"
#         business.description = "a business"
#         business.save()

#     def test_get__business(self):
#         '''Check if business was added to database'''
#         try:
#             business = Business.objects.get(name__icontains ='Business One')
#         except Exception as e:
#             raise Exception(e)

#     def test_get_permissions(self):
#         # Test Creator Permission '''
#         user_creator = User.objects.get(username__icontains = "user1")
#         business = Business.objects.get(name__icontains ='Business One')
#         is_employee, permissions = get_user_permissions(user_creator,business)
#         self.assertTrue(is_employee)
#         if not "creator_access" in permissions:
#             raise Exception("User not recognised as creator")

#         # Test Not Employee 
#         user = User.objects.get(username__icontains = "user2")
#         is_employee, permissions = get_user_permissions(user,business)
#         self.assertFalse(is_employee)
#         if permissions:
#             raise Exception("This user should have no permissions to this business")

#     def test_employee_creation_and_permissions(self):
#         business = Business.objects.get(name__icontains ='Business One')
#         user = User.objects.get(username__icontains = "user2")
#         new_employee = Employee.objects.create(
#             business = business,
#             employee = user
#         )
#         new_employee.save()
#         # Check if employee added
#         is_employee, permissions = get_user_permissions(user,business)
#         self.assertTrue(is_employee)
#         self.assertFalse(permissions)

#         # Add new position
#         new_position = BusinessPosition.objects.create(
#             business = business,
#             position = "Test Position"
#         )
#         new_position.save()
#         position = BusinessPosition.objects.get(position__icontains = "Test Position")
#         self.assertTrue(position)
#         new_employee.position = position
#         new_employee.save()

#         # Add permissions
#         permissions_available = ['Manage Inventory','Make Sales','Manage Sales','Access Accounts', 'Manage Accounts', 'Manage Employees']
        
#         for i in permissions_available:
#             new_permission = BusinessPermissions.objects.create(
#                 business = business,
#                 position = position,
#                 allowed = i
#             )
#             new_permission.save()

#         # Check permissions
#         is_employee, permissions = get_user_permissions(user,business)
#         self.assertEqual(len(permissions),6)

#     def test_businesses_page(self):
#         # Test get request
#         self.client.login(username ="user1",password ="userpassword")
#         response = self.client.get("/user/businesses/")
#         self.assertEqual(response.status_code, 200)

#         #Test post request
#         response = self.client.post("/user/businesses/",{
#             "name" : "New Name",
#             "logo" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif'),
#             "country_code" : "233",
#             "phone" : "98765432198",
#             "email" : "",
#             "location" : " somewhere new",
#             "description": " something new",
#         })
#         self.assertEqual(response.status_code,302)
        
#         # Error in form
#         response = self.client.post("/user/businesses/",{
#             "name" : "N",
#             "logo" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif'),
#             "country_code" : "233",
#             "phone" : "98",
#             "email" : "",
#             "location" : " somewhere new",
#             "description": " something new",
#         })
#         self.assertEqual(response.status_code,200) 
#         self.assertTrue(response.context['error_messages'])

#     def test_business_profile_page(self):
#         # Test get request
#         self.client.login(username ="user1",password ="userpassword")
#         response = self.client.get("/business/Business One/admin/profile/")
#         self.assertEqual(response.status_code, 200)

#         # Test post requests
#         response = self.client.post("/business/Business One/admin/profile/",{
#             "name" : "New Name",
#             "logo" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif'),
#             "country_code" : "233",
#             "phone" : "562293662",
#             "email" : " ",
#             "location" : "some where new",
#             "description" : "something new"
#         })
#         self.assertEqual(response.status_code, 302)

#         # Test invalid form
#         response = self.client.post("/business/New Name/admin/profile/",{
#             "name" : "u",
#             "logo" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif'),
#             "country_code" : "233",
#             "phone" : "5",
#             "email" : " ",
#             "location" : "some where new",
#             "description" : "something new"
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.context['error_messages'])

#     def test_business_employee_management_page(self):
#         # Test get request
#         self.client.login(username ="user1",password ="userpassword")
#         response = self.client.get("/business/Business One/admin/employee_management/")
#         self.assertEqual(response.status_code, 200)
        
        



    