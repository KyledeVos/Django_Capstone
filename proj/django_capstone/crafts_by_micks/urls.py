from django.urls import path
from . import views

app_name = "crafts_by_micks"
urlpatterns = [
    path('', views.home_page, name = "home_page"),
    path('create_product/', views.create_product, name="create_product")
]