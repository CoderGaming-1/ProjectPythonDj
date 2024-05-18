from django.shortcuts import render
from .models import Roles, Users, Accounts, Medicalrecords
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Accounts
from django.conf import settings
import random
import string


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def forget_password(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        user_e = Accounts.objects.filter(email=email).first().email
        user_account = Accounts.objects.filter(email=email).first()
        if user_account:
            rand_pass = generate_random_password()
            user_account.password = rand_pass
            user_account.save()
        email_subject = 'Reset your password'
        email_message = f"We have recover your password. Your password is {rand_pass}"
        recipients = [email, user_e] #Receiver
        recipients_tuple = tuple(recipients)
        send_mail(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,  # Replace with your email
            [email],
            fail_silently=False,
        )
        return render(request, 'login.html')
    return render(request, 'password_reset_form.html')

def index(request):
    first_user = Users.objects.first()
    return render(request, {'first_user': first_user})

def get_login_view(request):
    return render(request, 'login.html')

def login_view(request):
    email = request.POST["email"]
    password = request.POST["password"]
    msg = None

    if request.method == 'POST':     
        try:
            user = Accounts.objects.get(email=email)
            
            # Verify the password
            if password == user.password: 
                user_real = user.iduser
                if user_real:
                    user_role = Roles.objects.filter(id=user_real.idrole.id).first()
                    if user_role.rolename == 'admin':
                        return render(request,'admin.html',{'id': user.iduser.id} )
                    elif user_role.rolename == 'doctor':
                        return render(request,'doctor.html', {'id': user.iduser.id})
                    elif user_role.rolename == 'patient':
                        return render(request,'patient.html',{'id': user.iduser.id})
            else:
                msg = "Fail"
                return render(request, 'login.html', {'msg': msg})
        except Accounts.DoesNotExist:
            msg="Didn't exist"
            return render(request, 'login.html', {'msg': msg})
    else:
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
            role = Roles.objects.get(rolename='patient')

            new_user = Users(
                idrole=role,
                name='hongngan',
                birth=None,
                gender=None,
                phonenumber='123456789',
                nation='',
                graduation='Truong DHBK DaNang',
                status=1, 
                description='',
                createdby=0,  
                createddate=timezone.now(),
                updatedby=0, 
                updateddate=timezone.now(),
                avatar=None
            )
            new_user.save()

            new_account = Accounts(
                iduser=new_user,
                email=email,
                password=password,  
                status=1,
                description='',
                createdby=0, 
                createddate=timezone.now(),
                updatedby=0, 
                updateddate=timezone.now()
            )
            new_account.save()

            new_medical_record = Medicalrecords(
                iduser=new_user,
                bloodtype='O',  
                allergy='Mentally', 
                status=1,  
                description='',
                creadtedby=0, 
                createddate=timezone.now(),
                updatedby=0,  
                updateddate=timezone.now()
            )
            new_medical_record.save()
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