from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('BookAppointment/<int:patient_id>', views.get_page, name="BookAppointment"),
    path('PostBookAppointment/', views.PostBookAppointment, name="PostBookAppointment"),
    path('HistoryAppointment/<int:patient_id>', views.get_HistoryAppointment, name="HistoryAppointment"),
    path('CancelHistoryAppointment/', views.cancel_HistoryAppointment, name="CancelHistoryAppointment"),
]