from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/list/', views.favorites_list, name='favorites_list'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
]