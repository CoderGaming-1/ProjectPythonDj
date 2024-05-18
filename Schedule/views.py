from django.shortcuts import render
from .models import Roles, Users, Accounts, Schedules
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login
# Create your views here.
def index(request):
    # response = HttpResponse()
    # response.writelines("<h1>Xin chao </h1>")
    # response.writelines("Day la schedule")
    context = {
        'nav_links': ['Home', 'Schedule', 'Appointment']
    }
    return render(request, 'pages/doctorScheduleMonth.html', context)
    # return render(request, 'pages/doctorScheduleMonth.html')
def doctor_info(request):
    first_user = Users.objects.first()
    user_account = Accounts.objects.filter(iduser=first_user.id).first()
    user_email = user_account.email if user_account else None
    return render(request,'base/header.html', {'first_user': first_user,'user_email': user_email})