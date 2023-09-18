"""URL paths for app 'product-site' serving as django project site home and integrated with
    app 'crafts_by_micks' - admin control.
    """
from django.urls import path, include
from . import views

app_name='product_site'
urlpatterns = [
    # site home page
    path('', views.site_home, name='site_home')
]