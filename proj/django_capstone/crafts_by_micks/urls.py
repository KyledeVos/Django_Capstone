from django.urls import path
from . import views

app_name = "crafts_by_micks"
urlpatterns = [
    path('', views.home_page, name = "home_page"),
    path('<source>/create_category/', views.create_category, name = "create_category"),
    path('<source>/add_category/', views.add_category, name = 'add_category'),
    path('<source>/create_label/', views.create_label, name='create_label'),
    path('<source>/add_label', views.add_label, name="add_label"),
    path('create_product/', views.create_product, name="create_product"),
    path('add_product/', views.add_product, name="add_product")
]