from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Roles, Users, Accounts, Schedules, Meetings
import json
import datetime as dt
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder


def index(request):
    return render(request, 'pages/home.html')

class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return obj.isoformat()
        return super().default(obj)

def schedule(request):
    schedules = Schedules.objects.filter(iduser__id=4).select_related('iduser')
    schedules_list = list(schedules.values('status', 'startshift', ))
    schedules_json = json.dumps(schedules_list, cls=DateTimeEncoder)
    context = {"schedules": schedules, "schedules_json": schedules_json}
    return render(request, 'pages/schedule.html', context)

def createSchedule(request):
    try:
        iduser = 4
        startShift = request.POST["startShift"]
        endShift = request.POST["endShift"]
        createdDate = datetime.now()
        starttime = timezone.make_aware(datetime.strptime(startShift, '%Y-%m-%dT%H:%M'))
        endtime = timezone.make_aware(datetime.strptime(endShift, '%Y-%m-%dT%H:%M'))
        doctor_instance = Users.objects.get(pk=iduser)
        
        current_time = starttime
        while current_time < endtime:
            if time(7, 0) <= current_time.time() <= time(19, 0):
                if not Schedules.objects.filter(iduser=doctor_instance, startshift=current_time, status=1).exists():
                    Schedules.objects.create(
                        iduser=doctor_instance, 
                        startshift=current_time, 
                        status=1, 
                        createdby=iduser, 
                        createddate=createdDate
                    )
            current_time += timedelta(minutes=30)
        # return redirect('/')
        return HttpResponse('Created successfully')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
    
def appointment(request):
    return render(request, 'pages/appointment.html')

