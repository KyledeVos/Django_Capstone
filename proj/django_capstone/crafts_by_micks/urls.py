"""URL paths for app: 'crafts_by_micks' within Django project 'django_capstone.
    Includes Path for site admin control and user usage.'"""

from django.urls import path
from . import views

app_name = "crafts_by_micks"
urlpatterns = [
    # Home Page of App showing user signup, login, product catalog and orders
    path('', views.home_page, name = "home_page"),
    # admin control - create a new Product Category
    path('<source>/create_category/', views.create_category, name = "create_category"),
    # admin control - add newly created Product Category to Database
    path('<source>/add_category/', views.add_category, name = 'add_category'),
    # admin control - create a new Product Label
    path('<source>/create_label/', views.create_label, name='create_label'),
    # admin control - add newly created label to database
    path('<source>/add_label', views.add_label, name="add_label"),
    # admin control - Create a New Product
    path('create_product/', views.create_product, name="create_product"),
    # admin control - add newly created product to database
    path('add_product/', views.add_product, name="add_product")
]
