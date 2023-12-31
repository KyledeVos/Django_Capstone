"""URL paths for app 'product-site' serving as django project site home and integrated with
    app 'crafts_by_micks' - admin control.
"""
from django.urls import path
from . import views

app_name='product_site'
urlpatterns = [
    # site home page
    path('', views.site_home, name='site_home'),
    # individual Product View
    path('<product_id>/<error>/product_view/', views.product_view, name='product_view'),
    # Retrieve product specifications to create an item to be added to an order
    path('<product_id>/create_order_item', views.create_order_item, name='create_order_item'),
    # display customer orders and details menu
    path('<message>/customer_orders', views.customer_orders, name='customer_orders'),
    # allow customer to remove an item from an order
    path('<item_id>/<order_id>/remove_item/', views.remove_item, name='remove_item'),
    # allow customer to submit an open order
    path('<order_id>/submit_order', views.submit_order, name='submit_order'),
    # allow customer to view processing and completed orders
    path('<order_id>/<message>/view_order', views.view_order, name='view_order'),
    # allow a customer to leave a review
    path('<order_item_id>/<order_id>/product_review', views.product_review, name='product_review'),
    # save review to a product
    path('<product_id>/<order_id>/save_review', views.save_review, name='save_review')
]
