# Arquivo: /apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from datetime import date
from apps.risk_rating.ml_classifier import MachineLearning
from apps.users.forms import RegistrationStaffForm
from apps.users.forms import RegistrationPatientForm
from apps.users.forms import EditPatientForm
from .models import Patient, Staff
from apps.risk_rating.forms import ClinicalState_28dForm
from apps.risk_rating.forms import ClinicalState_29d_2mForm
from apps.risk_rating.forms import ClinicalState_2m_3yForm
from apps.risk_rating.models import ClinicalState_28d
from apps.risk_rating.models import ClinicalState_29d_2m
from apps.risk_rating.models import ClinicalState_2m_3y


ml1 = MachineLearning('apps/risk_rating/class_menos_28.csv')
ml2 = MachineLearning('apps/risk_rating/class_29d_2m.csv')
ml3 = MachineLearning('apps/risk_rating/class_2m_3y.csv')
ml5 = MachineLearning('apps/risk_rating/class_10y+.csv')


def landing_page(request):
    return render(request, 'landing_page/landingPage.html', {})


def login_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home")
        else:

            kwargs['extra_context'] = {'next': reverse('users:login'),
                                       'errors': 'Usuário e/ou senha inválido.'
                                       }

            kwargs['template_name'] = 'users/user_login/login.html'
            return login(request, *args, **kwargs)

    kwargs['extra_context'] = {'next': reverse('users:login')}
    kwargs['template_name'] = 'users/user_login/login.html'
    return login(request, *args, **kwargs)


@login_required(redirect_field_name='', login_url='users:login')
def home(request):
    """
    define home page behaviour
    """
    form1 = ClinicalState_28dForm()
    form2 = ClinicalState_29d_2mForm()
    form3 = ClinicalState_2m_3yForm()
    patients = Patient.objects.all()
    classification = None

    if request.method == "POST" and "form1" in request.POST:
        # this 'if' with the form1' runs when you submit the form of
        # patients under 28 days
        form = ClinicalState_28dForm(request.POST)
        form.save()

        p_id = request.POST.get("patient_id1")
        subject_patient = Patient.objects.filter(id=p_id)[0]
        p_c_states_l = ClinicalState_28d.objects.filter(patient_id1=p_id)
        clinical_state = p_c_states_l.order_by('-id')[0]
        trigger_ml(subject_patient, clinical_state)

    elif request.method == "POST" and "form2" in request.POST:
        form = ClinicalState_29d_2mForm(request.POST)
        form.save()

        p_id = request.POST.get("patient_id2")
        subject_patient = Patient.objects.filter(id=p_id)[0]
        p_c_states_l = ClinicalState_29d_2m.objects.filter(patient_id2=p_id)
        clinical_state = p_c_states_l.order_by('-id')[0]
        trigger_ml(subject_patient, clinical_state)

    elif request.method == "POST" and "form3" in request.POST:
        form = ClinicalState_2m_3yForm(request.POST)
        form.save()

        p_id = request.POST.get("patient_id3")
        subject_patient = Patient.objects.filter(id=p_id)[0]
        p_c_states_l = ClinicalState_2m_3y.objects.filter(patient_id3=p_id)
        clinical_state = p_c_states_l.order_by('-id')[0]
        trigger_ml(subject_patient, clinical_state)

    return render(request, 'users/user_home/main_home.html',
                           {'patients': patients,
                            'classification': classification,
                            'form1': form1,
                            'form2': form2,
                            'form3': form3})


def trigger_ml(subject_patient, clinical_state):
    """
    triggers the machine learning based on patient's age range
    """
    if subject_patient.age_range == 1:
        patient = get_under_28_symptoms(clinical_state)
        probability = ml1.calc_probabilities(patient)
        classification = ml1.classify_patient(patient)
        impact_list = ml1.feature_importance()
    elif subject_patient.age_range == 2:
        patient = get_29d_2m_symptoms(clinical_state)
        probability = ml2.calc_probabilities(patient)
        classification = ml2.classify_patient(patient)
        impact_list = ml2.feature_importance()
        # due to the lack of data, this classification is
        # always being "AmbulatorialGeral"
    elif subject_patient.age_range == 3:
        patient = get_2m_3y_symptoms(clinical_state)
        probability = ml3.calc_probabilities(patient)
        classification = ml3.classify_patient(patient)
        impact_list = ml3.feature_importance()
    # to add another age range, use another elif

    # printing results:
    print(probability)
    print(impact_list)
    print(classification)
    define_patient_classification(subject_patient, classification)


def define_patient_classification(subject_patient, classification):
    """
    edit patient's classification attribute
    """
    if classification == 'AtendimentoImediato':
        subject_patient.classification = 1
    elif classification == 'AmbulatorialGeral':
        subject_patient.classification = 2
    elif classification == 'AtendimentoHospitalar':
        subject_patient.classification = 3
    else:
        pass

    subject_patient.save()


def check_patient_problem(problem):
    if problem is not None and problem is True:
        problem = 1
    else:
        problem = 0

    return problem


def logout_view(request, *args, **kwargs):
    """
    Define the logout page
    """
    kwargs['next_page'] = reverse('users:landing_page')
    return logout(request, *args, **kwargs)


def sign_up_profile(request):
    form = RegistrationStaffForm()
    if request.method == 'POST':
        form = RegistrationStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')

    return render(request, 'users/user_login/registerUser.html',
                  {'form': form})


def specify_age_range(age_range, aux_age_range, form):
    if age_range >= 0 and age_range <= 28:
        aux_age_range = form.cleaned_data['age_range'] = 1
    elif age_range > 28 and age_range <= 90:
        aux_age_range = form.cleaned_data['age_range'] = 2
    elif age_range > 90 and age_range <= 730:
        aux_age_range = form.cleaned_data['age_range'] = 3
    elif age_range > 730 and age_range <= 3650:
        aux_age_range = form.cleaned_data['age_range'] = 4
    elif age_range > 3650:
        aux_age_range = form.cleaned_data['age_range'] = 5
    else:
        aux_age_range = form.cleaned_data['age_range'] = 0
    instance = form.save(commit=False)
    instance.age_range = aux_age_range
    instance.save()


def calculate_age_range(form):
    birth_date = form.cleaned_data['birth_date']
    age_range = (date.today() - birth_date).days
    int(age_range)
    aux_age_range = 0
    specify_age_range(age_range, aux_age_range, form)


@login_required(redirect_field_name='', login_url='users:login')
def register_patient(request):
    form = RegistrationPatientForm()
    if request.method == 'POST':
        form = RegistrationPatientForm(request.POST)
        if form.is_valid():
            if ['birth_date'] in form.changed_data:
                calculate_age_range(form)
            else:
                pass    
            form.save()
            return redirect('users:home')

    return render(request, 'users/user_home/registerPatient.html',
                  {'form': form})


@login_required(redirect_field_name='', login_url='users:login')
def queue_patient(request, cpf_patient):
    patients = Patient.objects.filter(cpf=cpf_patient)
    patient = Patient.objects.get(cpf=cpf_patient)
    patientsInQueue = Patient.objects.all()
    patientList = list()
    for patient0 in patientsInQueue:
        patientList.append(patient0.patient)
    if patient in patientList:
        return render(request, 'users/queuePatient.html',
                               {'patientList': patientList})
    else:
        queuedPatient = Patient.objects.create(patient=patient)
        queuedPatient.save()
        patientList.append(patient)
        return render(request, 'users/queuePatient.html',
                               {'patients': patients})
    return render(request, 'users/queuePatient.html', {'patients': patients})


@login_required(redirect_field_name='', login_url='users:login')
def manage_accounts_view(request):
    staffs = Staff.objects.all()
    return render(request, 'users/manageAccounts.html', {'staffs': staffs})


@login_required(redirect_field_name='', login_url='users:login')
def edit_accounts_view(request, id_user):
    staff = Staff.objects.filter(id_user=id_user)
    if len(staff) == 1:
        return render(request, 'users/editAccounts.html', {'staff': staff[0]})
    return render(request, 'users/editAccounts.html', status=404)


@login_required(redirect_field_name='', login_url='users:login')
def staff_remove(request, id_user):
    staff = Staff.objects.filter(id_user=id_user)
    staff.delete()
    return HttpResponseRedirect(reverse('users:manage_accounts'))


@login_required(redirect_field_name='', login_url='users:login')
def patient_remove(request, id):
    patient = Patient.objects.filter(id=id)
    patient.delete()
    return HttpResponseRedirect(reverse('users:home'))


@login_required(redirect_field_name='', login_url='users:login')
def edit_patient(request, id):
    """
    edit an existing patient with post method
    """
    patient = Patient.objects.filter(id=id)[0]
    form = EditPatientForm()

    status = 200

    if request.method == 'POST':
        form = EditPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('users:home')
        else:
            status = 400
    return render(request, 'users/editPatient.html',
                  {'patient': patient, 'form': form}, status=status)


@login_required(redirect_field_name='', login_url='users:login')
def show_patient_view(request, cpf):
    """
    return rendered text from showPatient
    """
    patient = Patient.objects.filter(cpf=cpf)
    if len(patient) == 1:
        return render(request, 'users/showPatient.html', {'patient': patient})
    return render(request, 'users/showPatient.html', status=404)


def get_under_28_symptoms(clinical_state):
    """
    building patient (28d) to use on ml based on patient's clinical condition
    """
    patient = [[
        check_patient_problem(clinical_state.dispineia),
        check_patient_problem(clinical_state.ictericia),
        check_patient_problem(clinical_state.perdada_consciencia),
        check_patient_problem(clinical_state.cianose),
        check_patient_problem(clinical_state.febre),
        check_patient_problem(clinical_state.solucos),
        check_patient_problem(clinical_state.prostracao),
        check_patient_problem(clinical_state.vomitos),
        check_patient_problem(clinical_state.tosse),
        check_patient_problem(clinical_state.coriza),
        check_patient_problem(clinical_state.obstrucao_nasal),
        check_patient_problem(clinical_state.convulcao_no_momento),
        check_patient_problem(clinical_state.diarreia),
        check_patient_problem(clinical_state.choro_inconsolavel),
        check_patient_problem(clinical_state.dificuldade_evacuar),
        check_patient_problem(clinical_state.nao_suga_seio),
        check_patient_problem(clinical_state.manchas_na_pele),
        check_patient_problem(clinical_state.salivacao),
        check_patient_problem(clinical_state.queda),
        check_patient_problem(clinical_state.chiado_no_peito),
        check_patient_problem(clinical_state.diminuicao_da_diurese),
        check_patient_problem(clinical_state.dor_abdominal),
        check_patient_problem(clinical_state.dor_de_ouvido),
        check_patient_problem(clinical_state.fontanela_abaulada),
        check_patient_problem(clinical_state.secrecao_no_umbigo),
        check_patient_problem(clinical_state.secrecao_ocular),
        check_patient_problem(clinical_state.sangue_nas_fezes),
        check_patient_problem(clinical_state.convulsao_hoje)
    ]]
    return patient


def get_29d_2m_symptoms(clinical_state):
    """
    building patient (29d-2m) to use on ml based on
    patient's clinical condition
    """
    patient = [[
        check_patient_problem(clinical_state.dispineia),
        check_patient_problem(clinical_state.ictericia),
        check_patient_problem(clinical_state.perdada_consciencia),
        check_patient_problem(clinical_state.cianose),
        check_patient_problem(clinical_state.febre),
        check_patient_problem(clinical_state.solucos),
        check_patient_problem(clinical_state.prostracao),
        check_patient_problem(clinical_state.vomitos),
        check_patient_problem(clinical_state.tosse),
        check_patient_problem(clinical_state.coriza),
        check_patient_problem(clinical_state.obstrucao_nasal),
        check_patient_problem(clinical_state.convulcao_no_momento),
        check_patient_problem(clinical_state.diarreia),
        check_patient_problem(clinical_state.dificuldade_evacuar),
        check_patient_problem(clinical_state.nao_suga_seio),
        check_patient_problem(clinical_state.manchas_na_pele),
        check_patient_problem(clinical_state.salivacao),
        check_patient_problem(clinical_state.queda),
        check_patient_problem(clinical_state.chiado_no_peito),
        check_patient_problem(clinical_state.diminuicao_da_diurese),
        check_patient_problem(clinical_state.dor_abdominal),
        check_patient_problem(clinical_state.dor_de_ouvido),
        check_patient_problem(clinical_state.fontanela_abaulada),
        check_patient_problem(clinical_state.secrecao_no_umbigo),
        check_patient_problem(clinical_state.secrecao_ocular),
        check_patient_problem(clinical_state.sangue_nas_fezes),
        check_patient_problem(clinical_state.convulsao_hoje)
    ]]
    return patient


def get_2m_3y_symptoms(clinical_state):
    """
    building patient (2m-3y) to use on ml based on
    patient's clinical condition
    """
    patient = [[
        check_patient_problem(clinical_state.dispineia),
        check_patient_problem(clinical_state.ictericia),
        check_patient_problem(clinical_state.perdada_consciencia),
        check_patient_problem(clinical_state.cianose),
        check_patient_problem(clinical_state.febre),
        check_patient_problem(clinical_state.solucos),
        check_patient_problem(clinical_state.prostracao),
        check_patient_problem(clinical_state.vomitos),
        check_patient_problem(clinical_state.tosse),
        check_patient_problem(clinical_state.coriza),
        check_patient_problem(clinical_state.obstrucao_nasal),
        check_patient_problem(clinical_state.convulcao_no_momento),
        check_patient_problem(clinical_state.diarreia),
        check_patient_problem(clinical_state.dificuldade_evacuar),
        check_patient_problem(clinical_state.nao_suga_seio),
        check_patient_problem(clinical_state.manchas_na_pele),
        check_patient_problem(clinical_state.salivacao),
        check_patient_problem(clinical_state.queda),
        check_patient_problem(clinical_state.chiado_no_peito),
        check_patient_problem(clinical_state.diminuicao_da_diurese),
        check_patient_problem(clinical_state.dor_abdominal),
        check_patient_problem(clinical_state.dor_de_ouvido),
        check_patient_problem(clinical_state.fontanela_abaulada),
        check_patient_problem(clinical_state.secrecao_no_umbigo),
        check_patient_problem(clinical_state.secrecao_ocular)
    ]]
    return patient


def get_10y_more(form):
    """
    get symptoms from form to build patient's clinical condition
    """
    mais72hFebre = check_patient_problem(form.get("mais72hrFebre"))
    menos72hrFebre = check_patient_problem(form.get("menos72hrFebre"))
    tontura = check_patient_problem(form.get("tontura"))
    corpoEstranho = check_patient_problem(form.get("corpoEstranho"))
    dorDeDente = check_patient_problem(form.get("dorDeDente"))
    disuria = check_patient_problem(form.get("disuria"))
    urinaConcentrada = check_patient_problem(form.get("urinaConcentrada"))
    dispineia = check_patient_problem(form.get("dispineia"))
    dorToracica = check_patient_problem(form.get("dorToracica"))
    choqueEletrico = check_patient_problem(form.get("choqueEletrico"))
    quaseAfogamento = check_patient_problem(form.get("quaseAfogamento"))
    artralgia = check_patient_problem(form.get("artralgia"))
    ictericia = check_patient_problem(form.get("ictericia"))
    perdaDaConsciencia = check_patient_problem(form.get("perdaDaConsciencia"))
    palidez = check_patient_problem(form.get("palidez"))
    cianose = check_patient_problem(form.get("cianose"))
    solucos = check_patient_problem(form.get("solucos"))
    prostracao = check_patient_problem(form.get("prostracao"))
    febre = check_patient_problem(form.get("febre"))
    vomitos = check_patient_problem(form.get("vomitos"))
    tosse = check_patient_problem(form.get("tosse"))
    coriza = check_patient_problem(form.get("coriza"))
    espirros = check_patient_problem(form.get("espirros"))
    hiperemiaConjuntival = check_patient_problem(form.get("hiperemiaConjuntival"))
    secrecaoOcular = check_patient_problem(form.get("secrecaoOcular"))
    obstrucaoNasal = check_patient_problem(form.get("obstrucaoNasal"))
    convulsao = check_patient_problem(form.get("convulsao"))
    diarreia = check_patient_problem(form.get("diarreia"))
    dificuldadeEvacuar = check_patient_problem(form.get("dificuldadeEvacuar"))
    cefaleia = check_patient_problem(form.get("cefaleia"))
    manchasNaPele = check_patient_problem(form.get("manchasNaPele"))
    salivacao = check_patient_problem(form.get("salivacao"))
    queda = check_patient_problem(form.get("queda"))
    hiporexia = check_patient_problem(form.get("hiporexia"))
    salivacao = check_patient_problem(form.get("salivacao"))
    hiporexia = check_patient_problem(form.get("hiporexia"))
    constipacao = check_patient_problem(form.get("constipacao"))
    chiadoNoPeito = check_patient_problem(form.get("chiadoNoPeito"))
    diminuicaoDaDiurese = check_patient_problem(form.get("diminuicaoDaDiurese"))
    dorAbdominal = check_patient_problem(form.get("dorAbdominal"))
    otalgia = check_patient_problem(form.get("otalgia"))
    epistaxe = check_patient_problem(form.get("epistaxe"))
    otorreia = check_patient_problem(form.get("otorreia"))
    edema = check_patient_problem(form.get("edema"))
    adenomegalias = check_patient_problem(form.get("adenomegalias"))
    dorArticular = check_patient_problem(form.get("dorArticular"))
    dificuldadesDeMarcha = check_patient_problem(form.get("dificuldadesDeMarcha"))
    sonolencia = check_patient_problem(form.get("sonolencia"))
    secrecaoOcular = check_patient_problem(form.get("secrecaoOcular"))
    dorMuscular = check_patient_problem(form.get("dorMuscular"))
    dorRetroobitaria = check_patient_problem(form.get("dorRetroobitaria"))

    patient = [[
        mais72hFebre,
        menos72hrFebre,
        tontura,
        corpoEstranho,
        dorDeDente,
        disuria,
        urinaConcentrada,
        dispineia,
        dorToracica,
        choqueEletrico,
        quaseAfogamento,
        artralgia,
        ictericia,
        perdaDaConsciencia,
        palidez,
        cianose,
        solucos,
        prostracao,
        febre,
        vomitos,
        tosse,
        coriza,
        espirros,
        hiperemiaConjuntival,
        secrecaoOcular,
        obstrucaoNasal,
        convulsao,
        diarreia,
        dificuldadeEvacuar,
        cefaleia,
        manchasNaPele,
        salivacao,
        queda,
        hiporexia,
        salivacao,
        hiporexia,
        constipacao,
        chiadoNoPeito,
        diminuicaoDaDiurese,
        dorAbdominal,
        otalgia,
        epistaxe,
        otorreia,
        edema,
        adenomegalias,
        dorArticular,
        dificuldadesDeMarcha,
        sonolencia,
        secrecaoOcular,
        dorMuscular,
        dorRetroobitaria,
    ]]

    return patient
