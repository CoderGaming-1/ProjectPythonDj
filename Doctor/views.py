from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Roles, Users, Accounts, Schedules, Meetings

def index(request):
    return render(request, 'pages/home.html')

def schedule(request):
    schedules = Schedules.objects.select_related('iduser').all()
    context = {"schedules": schedules}
    return render(request, 'pages/schedule.html', context)

def appointment(request):
    return render(request, 'pages/appointment.html')

