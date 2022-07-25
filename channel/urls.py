from django.urls import path

from channel import views

urlpatterns = [
    path('',views.index)
]