
from django.urls import path, include
from rest_framework import routers
from . import views, apis

# Viesets
api_routs = routers.DefaultRouter()
api_routs.register(r'chat_users', apis.ChatUserViewSet)
api_routs.register(r'entries', apis.EntrieViewSet)
api_routs.register(r'sensors', apis.SensorViewSet)
api_routs.register(r'rooms', apis.RoomViewSet)
api_routs.register(r'places', apis.PlaceViewSet)
# api_routs.register(r'places/options', apis.roomtype_options)


# Views as methods
urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('settings/create/sensor/', views.create_sensor, name='create_sensor'),
    path('settings/create/place/', views.create_place, name='create_place'),
    path('settings/create/room/', views.create_room, name='create_room'),
    path('settings/create/chat_user/', views.create_chat_user, name='create_bot'),
    path('settings/update/place/', views.update_place, name='update_place'),
    path('settings/update/room/', views.update_room, name='update_room'),
    path('settings/update/chat_user/',
         views.update_chat_user, name='update_bot'),
    path('settings/update/settings/',
         views.update_settings, name='update_settings'),

    path('init_sensor/', views.init_sensor, name='init_sensor'),
    path('init_db/', views.init_db, name='init_db'),
    path('api/', include(api_routs.urls)),
    path('api/places/options', apis.roomtype_options, name='places_options'),
]
