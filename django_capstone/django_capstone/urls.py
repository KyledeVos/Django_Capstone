"""URL configuration for django_capstone project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # django admin site
    path('admin/', admin.site.urls),
    # site home page
    path('', include('product_site.urls')),
    # user management
    path('user_management/', include('user_management.urls')),
    # admin site control for admin user
    path('admin_control/', include('crafts_by_micks.urls'))
]

# url path allowing for upload and access of stored site images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
