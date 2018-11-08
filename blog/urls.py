"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.views.generic import RedirectView
from .settings import DEBUG, MEDIA_ROOT, STATIC_URL

urlpatterns = [
    path('', include('posts.urls')),
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=os.path.join(STATIC_URL, 'img/K_black.svg'))),
]

# in production, we'll serve '/media/' directly from nginx
if DEBUG:
    urlpatterns.append(
        re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}))
