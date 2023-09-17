from django.urls import path
from . import views

app_name='user_management'
urlpatterns = [
    # user login
    path('<error>/user_login/', views.user_login, name='user_login'),
    # authenticate user - attempt login
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    # user signup
    path('create_user/', views.create_user, name='create_user')
]