from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timedelta, time
import pytz
from .models import Roles, Users, Accounts, Schedules, Meetings

def format_date(input_date):
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = month_names[input_date.month - 1]
    day = str(input_date.day).zfill(2)
    year = input_date.year
    hours = str(input_date.hour).zfill(2)
    minutes = str(input_date.minute).zfill(2)
    return f"{month} {day}, {year}, {hours}:{minutes}"

# Create your views here.
def get_page(request, patient_id):
    try:
        user = Users.objects.get(pk=patient_id)
        current_time = timezone.now()
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time.astimezone(tz)
        schedules = Schedules.objects.select_related('iduser').filter(status=1, startshift__gt=current_time_tz_vn)

        for schedule in schedules:
                # Định dạng trường startshift của mỗi phần tử trong schedules
                schedule.formatted_startshift = format_date(schedule.startshift)

        context = {"schedules": schedules, "idPatient": patient_id, "name": user.name}
        return render(request, 'BookAppointment.html', context)
    except ObjectDoesNotExist:
        print("Không tìm thấy role có id là 2")
    

def index(request):
    roles = Roles.objects.all()
    for role in roles:
        print('********', role.rolename, role.id)
    return HttpResponse('this is response')

def PostBookAppointment(request):
    try:
        idSchedule = request.POST["idSchedule"]
        idPatient = request.POST["idPatient"]
        symptom = request.POST["symptom"]
        current_time_tz = timezone.now()  + timedelta(hours=7)
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time_tz.astimezone(tz)

        # Retrieve instances of Schedules and Users
        schedule_instance = Schedules.objects.get(pk=idSchedule)
        patient_instance = Users.objects.get(pk=idPatient)

        if schedule_instance.status == 1 and schedule_instance.startshift > current_time_tz_vn:
            meeting = Meetings.objects.create(idschedule=schedule_instance, idpatient=patient_instance, symptom=symptom, status=1, createdby=idPatient, createddate=current_time_tz_vn)
            result = {"idSchedule": idSchedule, "idPatient": idPatient, "symptom": symptom}
            schedule_instance.status = 2
            schedule_instance.updateddate = current_time_tz_vn
            schedule_instance.updatedby = idPatient
            schedule_instance.save()
            return HttpResponse(str(current_time_tz_vn)) #str(result)
        
        return HttpResponse('Validation Failed.')
    except Exception as e:
        return HttpResponse(e)
    

def get_HistoryAppointment(request, patient_id):
    try:
        user = Users.objects.get(pk=patient_id)
        current_time = timezone.now()
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time.astimezone(tz)
        meetings = Meetings.objects.select_related('idschedule').filter(status=1, idpatient=patient_id)

        for meeting in meetings:
                # Định dạng trường startshift của mỗi phần tử trong schedules
                meeting.idschedule.formatted_startshift = format_date(meeting.idschedule.startshift)

        context = {"meetings": meetings, "idPatient": patient_id, "name": user.name}
        return render(request, 'HistoryAppointment.html', context)
    except ObjectDoesNotExist:
        print("Không tìm thấy role có id là 2")

def cancel_HistoryAppointment(request):
    try:
        idMeeting = request.POST["idMeeting"]
        
        current_time_tz = timezone.now()  + timedelta(hours=7)
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time_tz.astimezone(tz)

        meeting = Meetings.objects.get(pk=idMeeting)
        meeting.status = 0
        meeting.updateddate = current_time_tz_vn
        meeting.updatedby = meeting.idpatient.id
        patient_id = meeting.idpatient
        meeting.save()

        schedule_instance = Schedules.objects.get(pk=meeting.idschedule.id)
        schedule_instance.status = 0
        schedule_instance.updateddate = current_time_tz_vn
        schedule_instance.updatedby = patient_id
        schedule_instance.save()
        
        return HttpResponse(str(idMeeting))
    except Exception as e:
        return HttpResponse(e)