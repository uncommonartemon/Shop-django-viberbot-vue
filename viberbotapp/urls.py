from django.urls import path
from . import viberbot, views

urlpatterns = [
    # Другие маршруты вашего приложения
    path('', views.webhook, name='webhook'),
]