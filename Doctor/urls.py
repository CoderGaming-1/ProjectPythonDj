from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('scheduleMonth/', views.schedule, name='schedule'),
    path('appointment/', views.appointment, name='appointment')
]