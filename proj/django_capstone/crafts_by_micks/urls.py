"""URL paths for app: 'crafts_by_micks' within Django project 'django_capstone.
    Includes Path for site admin control and user usage.'"""

from django.urls import path
from . import views

app_name = "crafts_by_micks"
urlpatterns = [
    # Admin Home Page of App showing user signup, login, product catalog and orders
    path('', views.home_page, name = "home_page"),

    #----------------------------- Admin Control -------------------------------------------------
    # 1) Creation
    # Create a new Product Category
    path('<source>/<error>/create_category/', views.create_category, name = "create_category"),
    # Add newly created Product Category to Database
    path('<source>/add_category/', views.add_category, name = 'add_category'),
    # New Product Label
    path('<source>/<error>create_label/', views.create_label, name='create_label'),
    # Add newly created label to database
    path('<source>/add_label', views.add_label, name="add_label"),
    # Create a New Product
    path('<error>/create_product/', views.create_product, name="create_product"),
    # Add newly created product to database
    path('add_product/', views.add_product, name="add_product"),

    # 2) Read
    # Return All Products in Database to Admin
    path('view_all_products/', views.view_all_products, name = "view_all_products")

    # 3) Update

    # 4) Deletion

    # Delete Category


    #----------------------------- Client Usage -------------------------------------------------
]
