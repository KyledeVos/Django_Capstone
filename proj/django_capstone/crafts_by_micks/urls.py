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
    # Return All Labels
    path('view_all_labels', views.view_all_labels, name='view_all_labels'),
    # Return All Products in Database to Admin
    path('view_all_products/', views.view_all_products, name = "view_all_products"),

    # 3) Update (and Deletion Combined)
    # Return Categories for Title Update
    path('<error>/view_all_categories/', views.view_all_categories, name = 'view_all_categories'),
    # Update or Delete a Category
    path('<int:category_id>/update_delete_category', views.update_delete_category, name = 'update_delete_category'),
    # Retrieve user inputs for label update
    path('<int:label_id>/<error>/update_label', views.update_label, name = 'update_label'),
    # Perform Label Update
    path('<int:label_id>/save_label_update', views.save_label_update, name = 'save_label_update' ),
    # Return Single Product info using Primary Key ID for update
    path('<int:product_id>/<error>/update_product/', views.update_product, name='update_product'),
    # Perform Update of a Product
    path('<int:product_id>/save_update', views.save_update, name = 'save_update'),

    # 4) Deletion - Only
    # Delete a Label
    path("<int:label_id>/delete_label", views.delete_label, name='delete_label'),
    # Product - Initial Deletion
    path("<int:product_id>/initial_product_deletion", views.initial_product_deletion, name='initial_product_deletion'),
    # Product Confirmed Deletion Deletion
    path('<int:product_id>/confirmed_product_deletion', views.confirmed_product_deletion, name='confirmed_product_deletion'),

    # 5) Customers and Orders - Details
    # View all Customers
    path('all_customers/', views.all_customers, name='all_customers'),
    # View All Orders for a Client
    path('<customer_id>/customer_orders/', views.customer_orders, name='customer_orders'),
    # view specific client order
    path('<order_id>/<customer_id>/<type>/view_order/', views.view_order, name='view_order'),
    # View all Orders
    path('all_orders/', views.all_orders, name='all_orders'),


]
