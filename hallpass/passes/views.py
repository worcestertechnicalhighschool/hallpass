from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import *
from .models import Student, HallPass, Destination
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
import datetime
import string
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, 'index.html', {})

@login_required
@require_http_methods(["POST"])
def time_in(request):
    form = LogForm(request.POST)
    if form.is_valid():
        log_id = form.cleaned_data['log_id']
        log = get_object_or_404(HallPass, pk = log_id)
        if log.time_in:
            return redirect("monitor")
        log.time_in = datetime.datetime.now()
        log.save()
    return redirect("monitor")

@login_required
@require_http_methods(["POST"])
def change_location(request):
    form = LocationForm(request.POST)
    if form.is_valid():
        log_id = form.cleaned_data['log_id']
        destination_id = form.cleaned_data['destination_id']

        log = get_object_or_404(HallPass, pk = log_id)
        destination = get_object_or_404(Destination, pk = destination_id)
        log.destination = destination
        log.save()
    return redirect("monitor")

@login_required
@require_http_methods(["POST"])
def time_out(request):
    form = LogForm(request.POST)
    if form.is_valid():
        log_id = form.cleaned_data['log_id']
        log = get_object_or_404(HallPass, pk = log_id)
        # check to makes sure they haven't been signed out at another computer
        if log.time_out == None:
            log.time_out = datetime.datetime.now()
            log.save()
        # Check to see if we can time_in the next person in queue
        destination = log.destination
        max = destination.max_people_allowed
        count_in = len(HallPass.objects.filter(destination = destination).exclude(time_in = None).filter(time_out = None))
        count_waiting = len(HallPass.objects.filter(destination = destination).filter(time_in = None).filter(time_out = None))
        if count_in < max and count_waiting > 0:
            next_in_line = HallPass.objects.filter(destination = destination).filter(time_in = None).filter(time_out = None)[0]
            next_in_line.time_in = datetime.datetime.now()
            next_in_line.save()
    
    return redirect("monitor")

@login_required
def monitor_destinations(request):
    # Users must have selected destinations 
    # in their profile. If not, redirect user
    user_profile = request.user.profile
    user_destinations = user_profile.destinations.filter(building = user_profile.building).order_by('room', 'category')
    if not user_destinations:
        return redirect(reverse('dashboard'))
    
    # Set form
    arrival_form = ArrivalForm()

    # Deal with submitted arrival form
    if request.method == "POST":
        arrival_form = ArrivalForm(request.POST)
        if arrival_form.is_valid():
            student_id = arrival_form.cleaned_data['student_id']

            # Retrieve the student from the database
            if (Student.objects.filter(student_id = student_id).exists()):
                student = get_object_or_404(Student, student_id = student_id)
                # check to see if student forgot to log out
                logs = HallPass.objects.filter(student_id = student).filter(time_out = None)
                for l in logs:
                    l.time_out = datetime.datetime.now() # logs student out 
                    l.forgot_time_out = True
                    l.save()
                # makes a new log
                destination_id = arrival_form.cleaned_data['destination_id']
                destination = get_object_or_404(Destination, pk = destination_id)
                log = HallPass(
                    student_id = student,
                    destination = destination,
                    building = destination.building,
                    arrival_time = datetime.datetime.now(),
                    user = request.user,
                )
                # I'VE TEMP DISABLED THIS FOR USER TESTING
                # Check if MAX_ALLOWED has been met yet. If not, time_in immediately
                queue = Profile.objects.filter(user = request.user)[0].queue
                
                if queue:
                    max = destination.max_people_allowed
                    count_in = len(HallPass.objects.filter(destination = destination).exclude(time_in = None).filter(time_out = None))
                    if count_in < max:
                        log.time_in = datetime.datetime.now()

                log.save()
                # Log created successfully. Reset the form
                arrival_form = ArrivalForm()
                
    # Prepare the data for the template
    destination_data = []
    for destination in user_destinations:
        logs = HallPass.objects.filter(destination = destination).filter(time_out = None)
        destination_data.append(
            {
                "destination": destination,
                "logs": logs,
            }
        )
    return render(
        request,
        'pages/monitor_destinations.html',
        {
            'arrival_form': arrival_form,
            'profile': user_profile,
            'destination_data': destination_data,
        }
    )


@login_required
def dashboard(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('monitor'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'pages/dashboard.html', { 'form': profile_form,})


def front_page(request):
    if request.method == 'POST':
        pass
    return render(request, 'pages/front_page.html', {})