from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/sensors', consumers.SensorsConsumer),
    path('ws/api', consumers.WebAPIConsumer),
    path('ws/tnes/<str:sensor>', consumers.TNESConsumer),
    path('ws/public/<str:sensor>', consumers.PublicConsumer),
    path('ws/analyzers/<str:sensor>', consumers.AnalyzersConsumer),
]
