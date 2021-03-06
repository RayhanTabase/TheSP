from django.urls import path, re_path
from . import views


app_name = "user"

urlpatterns = [
    # SignIn and Registration
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name="login" ),
    path('logout/',views.logout_view,name="logout" ),
    path('activate/<str:username>/', views.activate_user, name="activate_user"),
    
    # Navigation
    path('user/profile/', views.user_profile, name="user_profile"),
    path('user/invoices/', views.user_purchases, name="user_invoices"),

    # Edits
    path('user/edit/', views.edit_profile, name="edit_profile"),
    path('reset_password/<int:user_id>/' ,views.reset_password_page, name = "reset_password_page"),
    path('send_reset_email/' ,views.reset_password_email, name = "reset_password_email"),
    path('user/change_password/', views.change_password, name = "change_password"),

    # API get user name,contact, profile_picture_url
    path("check_username/<str:username>/", views.check_username, name="check_username")
]