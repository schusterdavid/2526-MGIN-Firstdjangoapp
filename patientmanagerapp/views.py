from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from patientmanagerapp.models import Patient
from datetime import datetime

# Create your views here.
def helloworld_view(request: HttpRequest):
    return HttpResponse("Hello World!")


def add_patient(request: HttpRequest):

    if (request.method == 'POST'):
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

    if (request.method == 'POST'):
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

