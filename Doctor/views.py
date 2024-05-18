from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Roles, Users, Accounts, Schedules, Meetings
import json
import logging
import datetime as dt
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'pages/home.html')

class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return obj.isoformat()
        return super().default(obj)

def schedule(request):
    iduser = 4
    schedules = Schedules.objects.filter(iduser__id=iduser).select_related('iduser')
    schedules_list = list(schedules.values('status', 'startshift'))
    schedules_json = json.dumps(schedules_list, cls=DateTimeEncoder)
    context = { "iduser": iduser,
                "schedules": schedules, 
                "schedules_json": schedules_json,
               }
    return render(request, 'pages/schedule.html', context)

# def createSchedule(request):
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
            if current_time.time() >= time(19, 0):
                current_time = current_time.replace(hour=7, minute=0) + timedelta(days=1)
        return redirect('/Doctor/schedule')
        # return HttpResponse('Created successfully')
        # return JsonResponse({'status': 'success'})
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
logger = logging.getLogger(__name__)

def createSchedule(request):
    try:
        iduser = 4
        startShift = request.POST["startShift"]
        endShift = request.POST["endShift"]
        createdDate = datetime.now()
        
        try:
            starttime = timezone.make_aware(datetime.strptime(startShift, '%Y-%m-%dT%H:%M'))
            endtime = timezone.make_aware(datetime.strptime(endShift, '%Y-%m-%dT%H:%M'))
        except ValueError as ve:
            logger.error(f"Date parsing error: {ve}")
            return HttpResponse(f"Date parsing error: {ve}")
        
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
            if current_time.time() >= time(19, 0):
                current_time = current_time.replace(hour=7, minute=0) + timedelta(days=1)
        
        return redirect('/Doctor/schedule')
    
    except Users.DoesNotExist:
        logger.error(f"User with id {iduser} does not exist.")
        return HttpResponse(f"User with id {iduser} does not exist.")
    
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        return HttpResponse(f"Error: {str(e)}")
    
def getScheduleByStatusTime(idDoctor, status, schedule_time_str):
    try:
        schedule_time = datetime.strptime(schedule_time_str, '%Y-%m-%d %H:%M:%S.%f')
        
        if schedule_time.tzinfo is None or schedule_time.tzinfo.utcoffset(schedule_time) is None:
            schedule_time = timezone.make_aware(schedule_time)

        # return HttpResponse(str(idDoctor) + ' ' + str(status) + ' ' + str(schedule_time))
        schedule = Schedules.objects.filter(iduser__id=idDoctor, status=status, startshift=schedule_time).order_by('-id').first()
        
        if schedule:
            return schedule.id
        else:
            return HttpResponse("No schedule found with the given status and time.")
    
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
def deleteSchedule(request):
    try:
        idDoctor = request.POST["idDoctor"]
        statusStr = request.POST["status"]
        shift = request.POST["shift"]
        status = 0
        if(statusStr == 'Active'):
            status = 1
        elif(statusStr == 'Booked'):
            status = 2
        
        print(f"Received idDoctor: {idDoctor}, status: {status}, shift: {shift}")

        try:
            # Parse the incoming shift string to a datetime object
            schedule_time = datetime.strptime(shift, '%a %b %d %Y %H:%M:%S')
            formatted_time = schedule_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        except ValueError as e:
            return HttpResponse(f"Error parsing date: {str(e)}")
        
        idSchedule = getScheduleByStatusTime(idDoctor, status, formatted_time)
        
        if isinstance(idSchedule, HttpResponse):
            return idSchedule 
        
        print(f"Obtained idSchedule: {idSchedule}")
        if idSchedule:
            schedule_id = int(idSchedule)
            schedule = Schedules.objects.filter(id=schedule_id).first()
            
            if schedule:
                schedule.status = 0
                schedule.save()
                return redirect('/Doctor/schedule')   
            else:
                return HttpResponse(f"No schedule found with id {idSchedule}.")
        else:
            return HttpResponse("No schedule id found for the given status and shift.") 
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    

def getMeetingByIdSchedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idDoctor = data.get('idDoctor')
            shift = data.get('time')
            status = data.get('status')

            try:
                schedule_time = datetime.strptime(shift, '%a %b %d %Y %H:%M:%S')
                formatted_time = schedule_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            except ValueError as e:
                return HttpResponse(f"Error parsing date: {str(e)}")
        
            idSchedule = getScheduleByStatusTime(idDoctor, status, formatted_time)
            # Thực hiện xử lý hoặc truy vấn cơ sở dữ liệu tại đây
            # Ví dụ: 
            meeting_info = getMeetingByIdSchedule(request, time, status)

            # Trả về phản hồi JSON
            return JsonResponse({'meeting_info': meeting_info})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def appointment(request):
    iduser = 4
    meetings = Meetings.objects.filter(idschedule__iduser=iduser).select_related('idschedule', 'idpatient').order_by('-idschedule__startshift')

    STATUS_MAP = {
        1: 'Pending',
        2: 'Active',
        3: 'Rejected',
        0: 'Inactive',
    }

    meetings_list = list(meetings.values(
        'id',
        'idpatient__name',
        'idpatient__phonenumber',
        'idschedule__startshift',
        'status', 
        'symptom',
        'reason',
        ))
    
    now = timezone.localtime(timezone.now())
    for meeting in meetings_list:
        meeting['idschedule__startshift'] = timezone.localtime(meeting['idschedule__startshift'])
        meeting['status'] = STATUS_MAP.get(meeting['status'], 'Unknown')
    context = {
        "iduser": iduser,
        "meetings": meetings_list,
        "nowTime": now,
    }
    return render(request, 'pages/appointment.html', context)
def approveMeeting(idMeeting):
    try:
        meeting = Meetings.objects.select_related('idschedule').get(id=idMeeting)
        meeting.status = 2
        meeting.updatedby = meeting.idschedule.iduser.id
        meeting.updateddate = datetime.now()
        meeting.save()
        return True
    except Meetings.DoesNotExist:
        return False

def rejectMeeting(idMeeting):
    try:
        meeting = Meetings.objects.select_related('idschedule').get(id=idMeeting)
        meeting.status = 3
        meeting.updatedby = meeting.idschedule.iduser.id
        meeting.updateddate = datetime.now()
        meeting.save()
        return True
    except Meetings.DoesNotExist:
        return False
    
def cancelMeeting(idMeeting, reasonCancel):
    try:
        print(idMeeting)
        print(reasonCancel)
        meeting = Meetings.objects.select_related('idschedule').get(id=idMeeting)
        meeting.status = 0
        meeting.reason = reasonCancel
        meeting.updatedby = meeting.idschedule.iduser.id
        meeting.updateddate = datetime.now()
        meeting.save()
        return True
    except Meetings.DoesNotExist:
        return False

def appointmentDetail(request, idMeeting):
    try:
        meeting = Meetings.objects.select_related('idschedule').get(id=idMeeting)
        context = {
            "meeting": meeting
        }
        return render(request, 'pages/appointmentDetail.html', context)  # Trả lại template và dữ liệu cuộc họp
    except Meetings.DoesNotExist:
        return HttpResponse("Meeting not found")

def proccessMeeting(request, meeting_id):
    try:
        action = request.POST["action-form-btn"]
        reasonCancel = request.POST["reasonCancel"]
        idMeeting = request.POST["idMeeting"]
        if action: 
            if action == 'Approve':
                approveMeeting(meeting_id)
                return redirect('/Doctor/appointment') 
            elif action == 'Reject':
                rejectMeeting(meeting_id)
                return redirect('/Doctor/appointment') 
            elif action == 'Cancel':
                # print('cancel zo ne')
                cancelMeeting(idMeeting, reasonCancel)
                return redirect('/Doctor/appointment')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


