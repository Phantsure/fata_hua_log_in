from django.urls import path

from . import views

app_name = 'log'
urlpatterns = [
    path('', views.index, name='index'),
    path('cat/', views.cat, name='cat'),
    path('blog/', views.blog, name='blog'),
    path('blog/<str:given_title>/', views.saved_blog, name='saved_blog'),
    path('blog/<str:given_title>/delete/', views.delete_saved_blog, name='delete_saved_blog'),
]