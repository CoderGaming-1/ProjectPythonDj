from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('createSchedule/', views.createSchedule, name="createSchedule"),
    path('appointment/', views.appointment, name='appointment')
]