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
from django.utils.dateparse import parse_date
import random
from django.contrib import messages
import string
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.defaultfilters import date
#import pycountry
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_account = Accounts.objects.filter(email=email).first()

        if user_account:
            rand_pass = generate_random_password()
            user_account.password = rand_pass
            user_account.save()

            email_subject = 'Reset your password'
            email_message = f"We have recovered your password. Your new password is {rand_pass}"

            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,  # Replace with your email
                [email],
                fail_silently=False,
            )
            msg = "A new password has been sent to your email."
        else:
            msg = "Your account does not exist."

        return render(request, 'password_reset_form.html', {'msg': msg})

    return render(request, 'password_reset_form.html')

# def index(request):
#     return render(request, 'login.html')

def get_login_view(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        msg = None
        
        if email and password:
            # Attempt to find the user with the provided email and password
            user = Accounts.objects.filter(email=email, password=password).first()

            if user:
                if user.status == 0:
                    msg = "Your account has been blocked. Sorry!"
                else:
                    user_real = user.iduser
                    if user_real:
                        user_role = Roles.objects.filter(id=user_real.idrole.id).first()
                        request.session['iduser'] = user_real.id
                        if user_role.rolename == 'admin':
                            admin_url = reverse('admin', args=[user_real.id])
                            return redirect(admin_url)
                        elif user_role.rolename == 'doctor':
                            schedule_url = reverse('schedule')
                            return redirect(schedule_url)
                        elif user_role.rolename == 'patient':
                            BookAppointment_url = reverse('BookAppointment')
                            return redirect(BookAppointment_url)
            else:
                # User not found or credentials are incorrect
                msg = "Incorrect email or password. Please try again."
        else:
            # Email or password not provided
            msg = "Both email and password are required."
        
        return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')

def get_register_view(request):
    return render(request, 'register.html')
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Oops! Confirm password didn't match with password.")
        elif Accounts.objects.filter(email=email).exists():
            messages.error(request, "This email has been used.")
        else:
            try:
                role = Roles.objects.get(rolename='patient')

                new_user = Users(
                    idrole=role,
                    name='',
                    birth=None,
                    gender=None,
                    phonenumber='',
                    nation='',
                    graduation='',
                    status=1,
                    description='',
                    createdby=0,
                    createddate=timezone.now(),
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
                    createddate=timezone.now()
                )
                new_account.save()

                new_medical_record = Medicalrecords(
                    iduser=new_user,
                    bloodtype='',
                    allergy='',
                    status=1,
                    description='',
                    creadtedby=0,
                    createddate=timezone.now()
                )
                new_medical_record.save()

                messages.success(request, "You have signed up a new account successfully!")
            except Roles.DoesNotExist:
                messages.error(request, "Role does not exist!")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'register.html')
def admin(request, idUser):
    return render(request,'admin.html',{'idUser': idUser})


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
               'user_email': account.email,
               'id_acc': account.iduser.id,
               }
    return render(request,'header.html', context)

def doctor_edit(request, idUser):
    if request.method != 'POST':
        user = Users.objects.get(id=idUser)
        account = Accounts.objects.filter(iduser=idUser, status=1).first()
        context = {'name': user.name,
                'phonenumber': user.phonenumber,
                'nation': user.nation,
                'graduation': user.graduation,
                'birth': user.birth,
                'gender': user.gender,
                'user_email': account.email,
                'idrole': user.idrole,
                'avatar' : user.avatar,
                'description' : user.description,
                }
        current_time = timezone.now()
        return render(request, 'edit_doctor.html', context)
        #Save into database
    elif ( request.method == 'POST'):
        name = request.POST.get('name')
        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        nation = request.POST.get('nation')
        graduation = request.POST.get('graduation')
        avatar = request.FILES.get('avatar')
        description = request.POST.get('description')
        email = request.POST.get('user_email')
        # Get current time
        current_time = timezone.now()
        
        # Update user instance and save it to the database
        user = Users.objects.get(id=idUser)
        account = Accounts.objects.filter(iduser=idUser, status=1).first()

        user.name = name
        user.birth = birth
        user.gender = True if gender == 'Female' else False
        user.phonenumber = phonenumber
        user.nation = nation
        user.graduation = graduation
        user.avatar = avatar
        user.description = description
        user.updateddate = current_time
        user.updatedby = idUser
        user.save()

        account.email = email
        account.updatedby = idUser
        account.updateddate = current_time
        account.save()
        return HttpResponse(f"{avatar}")
        context = {
               'name': user.name,
               'phonenumber': user.phonenumber,
               'nation': user.nation,
               'graduation': user.graduation,
               'birth': user.birth,
               'gender': user.gender,
               'avatar' : user.avatar,
               'description' : user.description,
               'user_email': account.email,
               'idrole': user.idrole,
               'id_acc': account.iduser.id,
               
               }
        return render(request, 'header.html', context)
        # Get current time
    return render(request, 'edit.html', context)

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from .models import Users, Accounts, Medicalrecords

def profile_patient(request):
    idUser = request.session.get('iduser')
    if idUser is None:
        return redirect(reverse('login'))

    user = Users.objects.get(id=idUser)
    account = Accounts.objects.filter(iduser=idUser, status=1).first()
    medical = Medicalrecords.objects.filter(iduser=idUser).first()
    birth_date = user.birth.strftime("%Y-%m-%d")
    
    if request.method == 'POST':
        if 'name' in request.POST:
            # Update profile
            name = request.POST.get('name')
            birth = request.POST.get('birth')
            gender = request.POST.get('gender')
            phonenumber = request.POST.get('phonenumber')
            nation = request.POST.get('nation')
            email = request.POST.get('email')
            bloodtype = request.POST.get('bloodtype')
            allergy = request.POST.get('allergy')

            user.name = name
            user.birth = birth
            user.gender = True if gender == 'Female' else False
            user.phonenumber = phonenumber
            user.nation = nation
            user.updateddate = timezone.now()
            user.updatedby = idUser
            user.save()

            if account:
                account.email = email
                account.updateddate = timezone.now()
                account.updatedby = idUser
                account.save()

            if medical:
                medical.bloodtype = bloodtype
                medical.allergy = allergy
                medical.updateddate = timezone.now()
                medical.updatedby = idUser
                medical.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('profile_patient')

        elif 'currentpassword' in request.POST:
            # Change password
            current_password = request.POST.get('currentpassword')
            new_password = request.POST.get('newpassword')
            confirm_password = request.POST.get('confirmpassword')

            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match')
                return redirect('profile_patient')

            if account.password != current_password:
                messages.error(request, 'Current password is incorrect')
                return redirect('profile_patient')

            account.password = new_password
            account.save()
            messages.success(request, 'Password changed successfully')
            return redirect('profile_patient')

    context = {
        'name': user.name,
        'phonenumber': user.phonenumber,
        'nation': user.nation,
        'birth': birth_date,
        'gender': user.gender,
        'email': account.email if account else '',
        'bloodtype': medical.bloodtype if medical else '',
        'allergy': medical.allergy if medical else '',
    }
    
    return render(request, 'edit_patient.html', context)


def admin_profile(request, idUser):

    return render(request, 'admin_profile.html',{'idUser': idUser})

def admin_task(request, idUser):
    return render(request, 'admin_task.html',{'idUser': idUser})
def admin_setting(request, idUser):
    if request.method != 'POST':
        acc = Accounts.objects.filter(iduser=idUser).first()
        email = acc.email
        password = acc.password
        context = {
            'email': email,
            'password': password,
            'idUser': idUser
        }
        return render(request, 'admin_setting.html', context)

    elif request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        acc = Accounts.objects.filter(iduser=idUser).first()
        if current_password == acc.password:
            if new_password == confirm_new_password:
                acc.password = new_password
                acc.save()
                context = {
                    'email': acc.email,
                    'password': acc.password,
                    'id': idUser
                }
                return render(request, 'admin_setting.html', context)  # Redirect to a success page after updating the password
            else:
                # Handle password mismatch error
                return render(request, 'admin_setting.html', {
                    'email': acc.email,
                    'password': acc.password,
                    'id': idUser,
                    'error': 'New password and confirmation do not match.'
                })
            
def admin_mda(request, idUser):
    # Fetch users with related account data
    users_list = Users.objects.filter(idrole=2).select_related('accounts').values(
        'id','name', 'birth', 'gender', 'phonenumber', 'nation', 'graduation', 'status', 'accounts__email'
    )
    active_users = [user for user in users_list if user['status'] == 1]
    inactive_users = [user for user in users_list if user['status'] == 0]
    # Create the context dictionary
    context = {
        'idUser': idUser,
        'users': users_list,
        'active_users': active_users,
        'inactive_users': inactive_users,
    }
    
    # Render the template with the context
    return render(request, 'admin_manage_mda.html', context)
def admin_mpa(request, idUser):
    users_list = Users.objects.filter(idrole=3).select_related('accounts').values(
        'id','name', 'birth', 'gender', 'phonenumber', 'nation', 'status', 'accounts__email'
    )
    context = {
        'idUser': idUser,
        'users': users_list
    }
    # Render the template with the context
    return render(request, 'admin_manage_mpa.html', context)

def update_user_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        new_status = int(request.POST.get('newStatus'))

        try:
            user = Users.objects.get(id=user_id)
            user.status = new_status
            user.save()

            # Update the associated account status
            account = Accounts.objects.get(iduser=user)
            account.status = new_status
            account.save()

            return JsonResponse({'status': 'success'})
        except Users.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        except Accounts.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def update_doctor_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        new_status = int(request.POST.get('newStatus'))

        try:
            user = Users.objects.get(id=user_id)
            user.status = new_status
            user.save()
            account = Accounts.objects.get(iduser=user)
            account.status = new_status
            account.save()

            return JsonResponse({'status': 'success'})
        except Users.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        except Accounts.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Account not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def admin_eda(request, idUser,idd):
    if request.method != 'POST':
        user = Users.objects.select_related('accounts').filter(id=idd).values(
            'id','name', 'birth', 'gender','graduation', 'phonenumber', 'nation', 'status', 'description','accounts__email'
        )
        context = {
            'idUser': idUser,
            'idd': idd,
            'user': user,
        }
        return render(request,'admin_eda.html' ,context)
    elif (request.method == 'POST'):
        # Get the form data from the POST request
        email = request.POST.get('email')
        name = request.POST.get('name')
        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        #description = request.POST.get('description')
        graduation = request.POST.get('graduation')
        nation = request.POST.get('nation')

        # Update the user object with the new data
        user = Users.objects.get(id=idd)
        acc = Accounts()
        user.accounts_set.update(email=email)
        user.name = name
        user.birth = birth
        if gender == 'Female':
            user.gender = True
        elif gender == 'Male':
            user.gender = False
        user.phonenumber = phonenumber
        #user.description = description
        user.graduation = graduation
        user.nation = nation
        user.updatedby = idUser
        user.updateddate = timezone.now()
        user.save()

        acc.iduser = user
        acc.email = email
        acc.updatedby = idd
        acc.updateddate = timezone.now()
        acc.save()

        # Redirect to the admin_eda page
        return HttpResponseRedirect(reverse('admin_eda', args=(idUser, idd)))
    
def admin_ada(request,idUser):
    # context = {
    #     'idUser':idUser,
    # }
    # return render(request, 'admin_ada.html',context)
    if request.method == 'POST':
        # Get the form data from the request
        email = request.POST.get('email')
        name = request.POST.get('name')
        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        description = request.POST.get('description')
        graduation = request.POST.get('graduation')
        nation = request.POST.get('nation')

        # Convert birth to date format
        birth_date = parse_date(birth)

        # Convert gender to boolean
        gender_bool = True if gender.lower() == 'Female' else False

        # Create or update the user and account
        user = Users(idrole_id=2)  # Set default role
        account = Accounts()

        user.name = name
        user.birth = birth_date
        user.gender = gender_bool
        user.phonenumber = phonenumber
        user.nation = nation
        user.graduation = graduation
        user.description = description
        user.status = 1
        user.save()

        account.iduser = user
        account.email = email
        account.save()

        return redirect('admin_mda', idUser=idUser)
    elif(request.method != 'POST') :
        context = {
        'idUser':idUser,
        }
        return render(request, 'admin_ada.html',context)
    
def log_out(request):
    if 'iduser' in request.session:
        del request.session['iduser']
    return redirect('login')