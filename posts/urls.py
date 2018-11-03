from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<slug:post_name>/', views.post, name='post'),
    path('tags/<slug:tag_name>/', views.tag, name='tag'),
]
