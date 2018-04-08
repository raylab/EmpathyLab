from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/sensors', consumers.SensorsConsumer),
    path('ws/api', consumers.WebAPIConsumer),
]
