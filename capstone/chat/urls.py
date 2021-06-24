from django.urls import path

from . import views

app_name = "chat"
urlpatterns =[
    path("chat/<str:business_name>/", views.business_chat, name="chat"),
    path("<str:business_name>/chats/", views.admin_business_chat, name="admin_chat"),
    path("chat/get_rooms/<int:business_id>/",views.get_rooms,name="get_rooms"),
    path("chat/get_messages/<str:room_name>/",views.get_messages,name="get_chats"),
]