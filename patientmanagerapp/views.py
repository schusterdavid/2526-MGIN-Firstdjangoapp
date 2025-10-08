from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from patientmanagerapp.models import Patient
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Create your views here.
def helloworld_view(request: HttpRequest):
    return HttpResponse("Hello World!")


def add_patient(request: HttpRequest):





    if (request.method == 'POST' and request.user.is_staff):
        Patient.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            date_of_birth = datetime.strptime(request.POST['birthday'], "%Y-%m-%dT%H:%M"),
            svnr = request.POST['svnr']
        )
        print(request.POST)

    return render(request, 'add_patient.html', context={'isValid': True})


def list_patients(request: HttpRequest):

    return render(request, 'listpatients.html', context={'patients': Patient.objects.all()})


def edit_patient(request: HttpRequest, id: int):

    patient = Patient.objects.get(id=id)
    
    if (request.method == 'POST' and request.user.is_staff):
        patient.first_name = request.POST['first_name']
        patient.last_name = request.POST['last_name']
        patient.date_of_birth = datetime.strptime(request.POST['birthday'], "%Y-%m-%dT%H:%M")
        patient.svnr = request.POST['svnr']
        patient.save()

    return render(request, 'add_patient.html', context={'patient': patient})
 



#Delete geht eigentlich
def delete_patient(request: HttpRequest):
    if request.method == 'POST':
        if request.POST.get('IdToDelete'):
            Patient.objects.filter(id=request.POST.get('IdToDelete')).delete()
    return render(request, 'listpatients.html', context={'patients': Patient.objects.all()})


def perform_login(request: HttpRequest):
    login_status = " "
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user: AbstractUser | None = authenticate(request, username=username, password=password)

        login_status = "successful" 

        if user is not None:
            login(request, user)
        else:
            login_status = "failed"

    return render(request, "login.html", context={"login_status": login_status})


def perform_logout(request: HttpRequest):
    logout(request)
    return redirect("/login/")


def perform_register(request: HttpRequest):
    registration_status = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not username or not password:
            registration_status = "Please fill in all required fields."
        else:
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                registration_status = "Username already exists."
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.is_active = False  # deactivate by default
                user.save()
                registration_status = "Registration successful. Your account must be activated by an admin."
    return render(request, "register.html", {"registration_status": registration_status, "username": request.POST.get('username', ''), "email": request.POST.get('email', '')})
 

def perform_assy(request: HttpRequest):

    return render(request, "assyn_practitioner.html")