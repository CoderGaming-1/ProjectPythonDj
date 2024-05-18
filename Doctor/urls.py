from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('createSchedule/', views.createSchedule, name="createSchedule"),
    path('deleteSchedule/', views.deleteSchedule, name="deleteSchedule"),
    path('appointment/', views.appointment, name='appointment'),
    path('appointmentDetail/<int:idMeeting>/', views.appointmentDetail, name='appointmentDetail'),
    path('proccessMeeting/<int:meeting_id>/', views.proccessMeeting, name='proccessMeeting'),
]