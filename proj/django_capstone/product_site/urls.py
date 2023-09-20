"""URL paths for app 'product-site' serving as django project site home and integrated with
    app 'crafts_by_micks' - admin control.
    """
from django.urls import path, include
from . import views

app_name='product_site'
urlpatterns = [
    # site home page
    path('', views.site_home, name='site_home'),
    # individual Product View
    path('<product_id>/product_view/', views.product_view, name='product_view')
]