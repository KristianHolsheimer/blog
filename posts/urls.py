from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/new/', views.edit, name='new'),
    path('posts/<slug:post_name>/edit/', views.edit, name='edit'),
    path('posts/<slug:post_name>/', views.post, name='post'),
    path('tags/<slug:tag_name>/', views.tag, name='tag'),
]
