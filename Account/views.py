from django.shortcuts import render
from .models import Roles, Users, Accounts, Schedules

# Create your views here.
def index(request):
    roles = Roles.objects.all()
    context = {"roles": roles}
    return render(request,'homepage.html', context)