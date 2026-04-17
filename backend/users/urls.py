from django.urls import path
from .views import register_user, login_user,users_list

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('',users_list),
]