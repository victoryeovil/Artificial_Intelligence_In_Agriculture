from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.farmer_dashboard, name='dashboard'),
    path('weather/', views.get_weather_data, name='weather'),
    path('search/', views.search_plant, name='search'),
    path('plant/', views.plant_search, name='plant'),
    path('current/',views. current, name='current'),
    path('focus/', views.focus, name='focus'),
    path('landing/', views.landing, name='landing'),
    path('detect/', views.plant_disease_detection, name='detection'),

]
