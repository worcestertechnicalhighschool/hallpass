from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CreateHallPassForm, ProfileForm
from .models import Student, HallPass, Destination
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import datetime
import string
from django.views.decorators.http import require_http_methods

'''
@login_required
def monitor_destinations_old(request, pk):   
    form = CreateHallPassForm()
    d = get_object_or_404(Destination, pk=pk)
    hallpasses = HallPass.objects.filter(Time_out = None)

    if request.method == 'POST':
        if request.POST['action'] == 'Enter':
            form = CreateHallPassForm(request.POST)
            if len(hallpasses.filter(destination = d)) < 4000:
                if form.is_valid():
                    student_id = form.cleaned_data['student']
                    student = Student.objects.filter(student_id=student_id)[0]
                    
                    for i in logs.filter(student_id = student):
                        i.Time_out = datetime.datetime.now()
                        i.save()
                    
                    hallpass = HallPass(
                        student_id = student,
                        destination = d
                    )
                    hallpass.save()
                    form = CreateHallPassForm()
            else:
                None
                # This should send a popup to the login page that say something like you have "4 students logged in already" but Im tired :(
        else:
            log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'])        
            student_logout_id = log_to_modify.student_id.student_id

            hallpasses.filter(student_id = Student.objects.filter(student_id = student_logout_id)[0]).update(Time_out = datetime.datetime.now())


    return render(request, 'pages/student_login_old.html', {'form': form, 'hallpasses':hallpasses.filter(destination = d), "room": d.room})
'''

@login_required
def monitor_destinations(request):
    form = CreateHallPassForm()
    user_profile = request.user.profile
    user_destinations = user_profile.destinations.all()
    hallpasses = HallPass.objects.filter(Time_out = None)

    if request.method == 'POST':
        if 'Enter' in request.POST['action']:
            form = CreateHallPassForm(request.POST)
            if form.is_valid(): 
                student_id = form.cleaned_data['student']
                student = Student.objects.filter(student_id=student_id)[0]
                d = Destination.objects.get(id = request.POST['action'].split(" ")[1])
                
                hallpass = HallPass(
                    student_id = student,
                    destination = d
                )

                hallpass.save()
                form = CreateHallPassForm()
        elif 'Out' in request.POST['action']:
            log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'].split(" ")[1])    
            student_logout_id = log_to_modify.student_id.student_id

            hallpasses.filter(student_id = Student.objects.filter(student_id = student_logout_id)[0]).update(Time_out = datetime.datetime.now())

    return render(request, 'pages/student_login.html', {'form': form, 'profile': user_profile, 'destinations': user_destinations })

@login_required
def select_destinations(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()

            form = CreateHallPassForm()
            user_profile = request.user.profile
            user_destinations = user_profile.destinations.all()

            return redirect(reverse('monitor'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'pages/dashboard.html', { 'form': profile_form, })