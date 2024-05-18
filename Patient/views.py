from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Roles, Users, Accounts, Schedules, Meetings

# Create your views here.
def get_page(request, patient_id):
    try:
        current_time = timezone.now()
        schedules = Schedules.objects.select_related('iduser').filter(status=1, startshift__gt=current_time)
        context = {"schedules": schedules, "idPatient": patient_id}
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
        current_time = timezone.now()

        # Retrieve instances of Schedules and Users
        schedule_instance = Schedules.objects.get(pk=idSchedule)
        patient_instance = Users.objects.get(pk=idPatient)

        if schedule_instance.status == 1 and schedule_instance.startshift > current_time:
            meeting = Meetings.objects.create(idschedule=schedule_instance, idpatient=patient_instance, symptom=symptom, status=1, createdby=idPatient, createddate=current_time)
            result = {"idSchedule": idSchedule, "idPatient": idPatient, "symptom": symptom}
            schedule_instance.status = 2
            schedule_instance.save()
            return HttpResponse(str(meeting)) #str(result)
        
        return HttpResponse('Validation Failed.')
    except Exception as e:
        return HttpResponse(e)