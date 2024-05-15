from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('BookAppointment/<int:patient_id>', views.get_page, name="BookAppointment"),
    path('PostBookAppointment/', views.PostBookAppointment, name="PostBookAppointment"),
]