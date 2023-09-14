from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CreateHallPassForm, ProfileForm
from .models import Student, HallPass, Destination
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import datetime
import string
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, 'index.html', {})

@login_required
def monitor_destinations(request):
    user_profile = request.user.profile
    user_destinations = user_profile.destinations.filter(building = user_profile.building)
    # form = CreateHallPassForm(request = request)
    form = CreateHallPassForm(request.POST, request = request)

    if not user_destinations:
        return redirect(reverse('dashboard'))

    hallpasses = HallPass.objects.filter(Time_out = None)
    if request.method == 'POST':
        if 'Enter' in request.POST['action']: 
            if form.is_valid(): 
                d = Destination.objects.get(id = request.POST['action'].split(" ")[1])
                count = len(HallPass.objects.filter(destination = d).exclude(Time_in = None).filter(Time_out = None))
                student_id = form.cleaned_data['student']   
                student = Student.objects.filter(student_id=student_id)[0]
           
                def queueCheck():
                    if len(HallPass.objects.filter(student_id = student)) >= 1:
                        HallPass.objects.filter(student_id = student).update(Time_out = datetime.datetime.now())
                    count = len(HallPass.objects.filter(destination = d).exclude(Time_in = None).filter(Time_out = None))
                    if d.max_people_allowed > count :
                        return datetime.datetime.now()

                hallpass = HallPass(
                    student_id = student,
                    destination = d,
                    building = d.building,
                    Time_in = queueCheck()
                )

                hallpass.save()
                form = CreateHallPassForm(request=request)
                
            
        elif 'Out' in request.POST['action']:
            log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'].split(" ")[1])    
            student_logout_id = log_to_modify.student_id.student_id
            count = len(HallPass.objects.filter(destination = log_to_modify.destination).exclude(Time_in = None).filter(Time_out = None))
            hallpasses.filter(student_id = Student.objects.filter(student_id = student_logout_id)[0]).update(Time_out = datetime.datetime.now())
            if log_to_modify.destination.max_people_allowed >= count and len(HallPass.objects.filter(destination = log_to_modify.destination).filter(Time_in = None).filter(Time_out = None)) > 0:
                log = HallPass.objects.filter(destination = log_to_modify.destination).filter(Time_in = None).filter(Time_out = None)[0]
                log.Time_in = datetime.datetime.now()
                log.save()

        elif 'In' in request.POST['action']:
            log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'].split(" ")[1])    
            log_to_modify.Time_in = datetime.datetime.now()
            log_to_modify.save()


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


