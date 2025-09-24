"""
URL configuration for patientmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from patientmanagerapp import views as pmapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', pmapp_views.helloworld_view),
    path('add_patient/', pmapp_views.add_patient),
    path('listpatients/', pmapp_views.list_patients),
    path('patients/edit/<int:id>/', pmapp_views.edit_patient),
    path('patients/delete/', pmapp_views.delete_patient, name='delete_patient'),
    path('login/', pmapp_views.perform_login),
    path('logout/', pmapp_views.perform_logout)
]

