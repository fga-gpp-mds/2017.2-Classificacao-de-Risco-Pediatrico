# Arquivo: /apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate

from .forms import RegistrationStaffForm
from .forms import RegistrationPatientForm

from .models import Patient, Staff


def login_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_admin:
                login(request, user)
                return redirect("/login/admin")

            if user.profile == 1:
                login(request, user)
                return redirect("/home/receptionist/")

            if user.profile == 2:
                login(request, user)
                return redirect("/risk_rating")
        else:

            kwargs['extra_context'] = {'next': reverse('users:login'),
                                       'errors': 'Usuário e/ou senha inválido.'
                                       }

            kwargs['template_name'] = 'users/login.html'
            return login(request, *args, **kwargs)

    kwargs['extra_context'] = {'next': reverse('users:login')}
    kwargs['template_name'] = 'users/login.html'
    return login(request, *args, **kwargs)


def logout_view(request, *args, **kwargs):
    """
    Define the logout page
    """
    kwargs['next_page'] = reverse('users:login')
    return logout(request, *args, **kwargs)


def sign_up_profile(request):
    if request.method == 'POST':
        form = RegistrationStaffForm(request.POST)
        form.is_valid()
        form.non_field_errors()
        # [print(field.label, field.name, field.errors) for field in form]
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            username = authenticate(username=username, password=raw_password)
            login(request, 'users:login')
            return redirect('users:login')
        else:
            status = 400
    else:
        form = RegistrationStaffForm()
        status = 200
    return render(request, 'users/registerProfile.html', {'form': form},
                  status=status)


def sign_up_patient(request):
    if request.method == 'POST':
        form = RegistrationPatientForm(request.POST)
        form.is_valid()
        form.non_field_errors()
        # [print(field.label, field.name, field.errors) for field in form]

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            username = authenticate(username=username, password=raw_password)
            login(request, 'users:login')
            return redirect('users:login')
        else:
            status = 400
    else:
        form = RegistrationPatientForm()
        status = 200
    return render(request, 'users/registerPatient.html', {'form': form},
                  status=status)


def register_patient(request):
    """
    Register a patient
    """
    return render(request, 'user/login', {})


def home_receptionist_view(request):
    """
    return rendered text from homeReceptionist
    """
    return render(request, 'users/homeReceptionist.html')


def admin_view(request):
    """
    return rendered text from homeReceptionist
    """
    return render(request, 'users/admin.html')


def home_attendant_view(request):
    """
    return rendered text from homeAttendant
    """
    return render(request, 'users/homeAttendant.html')


def manage_accounts_view(request):
    staffs = Staff.objects.all()
    return render(request, 'users/manageAccounts.html', {'staffs': staffs})


def edit_accounts_view(request, id_user):
    staffs = Staff.objects.filter(id_user=id_user)[0]
    return render(request, 'users/editAccounts.html', {'staffs': staffs})


def staff_remove(request, id_user):
    staff = Staff.objects.filter(id_user=id_user)
    staff.delete()
    return HttpResponseRedirect(reverse('users:manage_accounts'))


def show_pacient_view(request, cpf):
    """
    return rendered text from showPatient
    """
    patient = Patient.objects.filter(cpf=cpf)[0]
    return render(request, 'users/showPatient.html', {'patient': patient})
