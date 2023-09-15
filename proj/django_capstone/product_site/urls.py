from django.urls import path, include
from . import views

app_name='product_site'
urlpatterns = [
    path('', views.site_home, name='site_home')
]