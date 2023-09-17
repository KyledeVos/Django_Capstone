from django.urls import path
from . import views

app_name='user_management'
urlpatterns = [
    # user login
    path('user_login/', views.user_login, name='user_login'),
    # user signup
    path('create_user/', views.create_user, name='create_user')
]