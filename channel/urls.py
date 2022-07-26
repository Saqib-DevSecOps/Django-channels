from django.urls import path

from channel import views

urlpatterns = [
    path('<str:channel_name>/',views.index)
]