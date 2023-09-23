"""URL paths for app 'product-site' serving as django project site home and integrated with
    app 'crafts_by_micks' - admin control.
    """
from django.urls import path, include
from . import views

app_name='product_site'
urlpatterns = [
    # site home page
    path('', views.site_home, name='site_home'),
    # customer orders and details menu
    path('customer_orders', views.customer_orders, name='customer_orders'),
    # individual Product View
    path('<product_id>/<error>/product_view/', views.product_view, name='product_view'),
    # Retrieve product specifications to create an item to be added to an order
    path('<product_id>/create_order_item', views.create_order_item, name='create_order_item')
]