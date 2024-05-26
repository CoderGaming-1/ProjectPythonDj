from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timedelta, time
import pytz
from .models import Roles, Users, Accounts, Schedules, Meetings
from django.urls import reverse
from django.core.paginator import Paginator
from urllib.parse import urlencode

meeting_status_desc = ['Inactive', 'Pending', 'Active', 'Rejected']

def format_date(input_date):
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = month_names[input_date.month - 1]
    day = str(input_date.day).zfill(2)
    year = input_date.year
    hours = str(input_date.hour).zfill(2)
    minutes = str(input_date.minute).zfill(2)
    return f"{month} {day}, {year}, {hours}:{minutes}"

# Create your views here.
def get_page(request):
    try:
        patient_id = request.session.get('iduser')
        if patient_id is None:
            login_url = reverse('login')
            return redirect(login_url)
        
        user = Users.objects.get(pk=patient_id)
        current_time = timezone.now()
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time.astimezone(tz)
        schedules = Schedules.objects.select_related('iduser').filter(status=1, startshift__gt=current_time_tz_vn).order_by('-startshift')

        for schedule in schedules:
                # Định dạng trường startshift của mỗi phần tử trong schedules
                schedule.formatted_startshift = format_date(schedule.startshift)

        # Sử dụng Paginator để phân trang
        paginator = Paginator(schedules, 12)  # 10 schedules mỗi trang
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        #context = {"schedules": schedules, "idPatient": patient_id, "name": user.name}
        context = {"page_obj": page_obj, "idPatient": patient_id, "name": user.name}
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
            HistoryAppointment_url = reverse('HistoryAppointment')
            return redirect(HistoryAppointment_url)
        
        return HttpResponse('Validation Failed.')
    except Exception as e:
        return HttpResponse(e)
    

def get_HistoryAppointment(request):
    try:
        errormsg = request.GET.get('errormsg', None)
        patient_id = request.session.get('iduser')
        if patient_id is None:
            login_url = reverse('login')
            return redirect(login_url)

        user = Users.objects.get(pk=patient_id)
        current_time = timezone.now()
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time.astimezone(tz)
        meetings = Meetings.objects.select_related('idschedule', 'idschedule__iduser').filter(idpatient=patient_id).order_by('-idschedule__startshift')

        for meeting in meetings:
            # Định dạng trường startshift của mỗi phần tử trong schedules
            meeting.idschedule.formatted_startshift = format_date(meeting.idschedule.startshift)
            meeting.idschedule.startshift_tz = meeting.idschedule.startshift.astimezone(tz)
            meeting.statusDesc = meeting_status_desc[meeting.status]

        context = {
            "meetings": meetings, 
            "idPatient": patient_id, 
            "name": user.name, 
            'current_time': current_time_tz_vn, 
            'errormsg': errormsg}
        return render(request, 'HistoryAppointment.html', context)
    except ObjectDoesNotExist:
        print("Không tìm thấy role có id là 2")

def cancel_HistoryAppointment(request):
    try:
        patient_id = request.session.get('iduser')
        if patient_id is None:
            login_url = reverse('login')
            return redirect(login_url)

        idMeeting = request.POST["idMeeting"]
        
        current_time_tz = timezone.now()  + timedelta(hours=7)
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time_tz_vn = current_time_tz.astimezone(tz)
        
        meeting = Meetings.objects.get(pk=idMeeting)
        schedule_instance = Schedules.objects.get(pk=meeting.idschedule.id)
        if schedule_instance.startshift > current_time_tz_vn:
            meeting.status = 0
            meeting.updateddate = current_time_tz_vn
            meeting.updatedby = patient_id #meeting.idpatient.id
            meeting.reason = 'Cancelled By Patient'
            meeting.save()

            
            schedule_instance.status = 0
            schedule_instance.updateddate = current_time_tz_vn
            schedule_instance.updatedby = patient_id
            schedule_instance.save()
            HistoryAppointment_url = reverse('HistoryAppointment')
            return redirect(HistoryAppointment_url)
        
        else:
            params = {'errormsg': 'Expired Appointment cannot be cancelled.'}
            HistoryAppointment_url = f"{reverse('HistoryAppointment')}?{urlencode(params)}"
            return redirect(HistoryAppointment_url)
    except Exception as e:
        return HttpResponse(e)