from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CreateHallPassForm, ProfileForm
from .models import Student, HallPass, Destination
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import datetime
import string
from django.views.decorators.http import require_http_methods

@login_required
def monitor_destinations(request):
    user_profile = request.user.profile
    user_destinations = user_profile.destinations.filter(building = user_profile.building)
    form = CreateHallPassForm(request = request)

    if not user_destinations:
        return redirect(reverse('select'))

    hallpasses = HallPass.objects.filter(Time_out = None)

    if request.method == 'POST':
        if 'Enter' in request.POST['action']:
            form = CreateHallPassForm(request.POST, request = request)
            if form.is_valid(): 
                student_id = form.cleaned_data['student']
                student = Student.objects.filter(student_id=student_id)[0]
                d = Destination.objects.get(id = request.POST['action'].split(" ")[1])
                
                hallpass = HallPass(
                    student_id = student,
                    destination = d,
                    building = d.building
                )

                hallpass.save()
                form = CreateHallPassForm(request=request)

        elif 'Out' in request.POST['action']:
            log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'].split(" ")[1])    
            student_logout_id = log_to_modify.student_id.student_id

            hallpasses.filter(student_id = Student.objects.filter(student_id = student_logout_id)[0]).update(Time_out = datetime.datetime.now())

    return render(request, 'pages/student_login.html', {'form': form, 'profile': user_profile, 'destinations': user_destinations })

@login_required
def dashboard(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()

            form = CreateHallPassForm(request = request)
            user_profile = request.user.profile
            user_destinations = user_profile.destinations.all()

            return redirect(reverse('monitor'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'pages/dashboard.html', { 'form': profile_form, })
