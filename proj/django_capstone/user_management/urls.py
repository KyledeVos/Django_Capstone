"""URL paths for user_management app designated to app 'product_site' and
    'crafts_by_micks' - admin control. App handles user creation, login and logout.
    
NOTE:
current implementation has one admin user with no functionality to create other staff users as
was requested by site admin. All created users with the use of this app are designated as 'Active'
Only.
Use of the 'crafts_by_micks' - admin control is limited to the admin user only    
'"""
from django.urls import path
from . import views

app_name='user_management'
urlpatterns = [
    # user login - source = page of call to user login
    path('<source>/<error>/user_login/', views.user_login, name='user_login'),
    # authenticate user - attempt login. source = page of call to user login
    path('<source>/authenticate_user/', views.authenticate_user, name='authenticate_user'),
    # user logout - user logout will return user to product home page
    path('user_logout', views.user_logout, name='user_logout'),
    # load html page to retrieve new use details. source = page of call for user creation
    path('<source>/<error>/create_user/', views.create_user, name='create_user'),
    # attempt to create and save new user. source = page of call for user creation
    path('<source>/add_user/', views.add_user, name='add_user')
]