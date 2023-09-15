"""
URL configuration for django_capstone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    # admin site control for admin user
    path('admin_control/', include('crafts_by_micks.urls'))
]

# url path allowing for upload and access of stored site images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
