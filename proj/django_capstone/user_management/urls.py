from django.urls import path
from . import views

app_name='user_management'
urlpatterns = [
    # user login
    path('<source>/<error>/user_login/', views.user_login, name='user_login'),
    # authenticate user - attempt login
    path('<source>/authenticate_user/', views.authenticate_user, name='authenticate_user'),
    # user logout
    path('user_logout', views.user_logout, name='user_logout'),
    # load html page to retrieve new use details
    path('<error>/create_user/', views.create_user, name='create_user'),
    # attempt to create and save new user
    path('add_user/', views.add_user, name='add_user')
]