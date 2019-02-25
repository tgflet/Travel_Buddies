from django.urls import path, include
from . import views
urlpatterns = [
    path('main',views.index),
    path('join',views.join),
    path('travels',views.dash),
    path('login',views.verify),
    path('travels/add',views.plan),
    path('logout',views.logout),
    path('travels/add_trip',views.add),
    path('travels/join/<num>',views.join_trip),
    path('travels/destinations/<num>',views.trip),
]