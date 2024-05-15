from django.shortcuts import render
from .models import Roles, Users, Accounts, Schedules
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate ,login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.
# def index(request):
#     roles = Roles.objects.all()
#     context = {"roles": roles}
#     return render(request,'index.html', context)
def index(request):
    first_user = Users.objects.first()
    return render(request, {'first_user': first_user})

def get_login_view(request):
    return render(request, 'login.html')

def login_view(request):
    #role=...
    # user = Users.objects.create(idschedule=schedule_instance, idpatient=patient_instance, symptom=symptom, status=1, createdby=idPatient, createddate=current_time)
    # acc = Accounts.objects.create(iduser=user,...)
    # form = LoginForm(request.POST or None)
    email = request.POST["email"]
    password = request.POST["password"]
    msg = None

    if request.method == 'POST':     
        try:
            # Check if a user with the provided email exists
            user = Accounts.objects.get(email=email)
            
            # Verify the password
            if password == user.password: 
                # Retrieve the user's role from the Roles table based on their ID
                user_real = user.iduser
                if user_real:
                    user_role = Roles.objects.filter(id=user_real.idrole.id).first()
                    if user_role.rolename == 'admin':
                        return HttpResponse(user_role.rolename)
                        return render(request,'admin.html',{'id': user.iduser.id} )
                    elif user_role.rolename == 'doctor':
                        return render(request,'doctor.html', {'id': user.iduser.id})
                    elif user_role.rolename == 'patient':
                        return render(request,'patient.html',{'id': user.iduser.id})
            else:
                # Authentication failed, handle error
                msg = "Fail"
                return render(request, 'login.html', {'msg': msg})
        except Accounts.DoesNotExist:
            # No user with that email exists
            msg="Didn't exist"
            return render(request, 'login.html', {'msg': msg})
    else:
        #return render(request,"login.html")
        return HttpResponse('this is response')



def get_register_view(request):
    return render(request, 'register.html')
def register_view(request):
    msg = None
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            msg = "Passwords do not match!"
            return render(request, 'register.html', {'msg': msg})

        if Accounts.objects.filter(email=email).exists():
            msg = "Email already exists!"
            return render(request, 'register.html', {'msg': msg})

        try:
            # Get the role, assuming it exists
            role = Roles.objects.get(rolename='patient')

            # Create a new user
            new_user = Users(
                idrole=role,
                name='phanbahoang',
                birth=None,
                gender=None,
                phonenumber='',
                nation='',
                graduation='Truong DHBK DaNang',
                status=1,  # Set default status
                description='',
                createdby=0,  # Or use request.user.id if logged in
                createddate=timezone.now(),
                updatedby=0,  # Or use request.user.id if logged in
                updateddate=timezone.now(),
                avatar=None
            )
            new_user.save()

            # Create a new account linked to the new user
            new_account = Accounts(
                iduser=new_user,
                email=email,
                password=password,  # Hash the password
                status=1,  # Set default status
                description='',
                createdby=0,  # Or use request.user.id if logged in
                createddate=timezone.now(),
                updatedby=0,  # Or use request.user.id if logged in
                updateddate=timezone.now()
            )
            new_account.save()

            return redirect('/Account/login')
        except Roles.DoesNotExist:
            msg = "Role does not exist!"
            return render(request, 'register.html', {'msg': msg})
        except Exception as e:
            msg = str(e)
            return render(request, 'register.html', {'msg': msg})
    else:
        return render(request, 'register.html', {'msg': msg})
    
def admin(request):
    return render(request,'admin.html')


def patient(request):
    return render(request,'patient.html')


def doctor(request, idUser):
    user = Users.objects.get(id=idUser)
    account = Accounts.objects.filter(iduser=idUser, status=1).first()
    context = {'name': user.name,
               'phonenumber': user.phonenumber,
               'idrole': user.idrole,
               'nation': user.nation,
               'graduation': user.graduation,
               'birth': user.birth,
               'gender': user.gender,
               'user_email': account.email}
    return render(request,'header.html', context)