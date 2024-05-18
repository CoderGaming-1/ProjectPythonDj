from django.shortcuts import render
from django.http import HttpResponse
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
