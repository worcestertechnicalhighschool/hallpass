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
        log.Time_in = datetime.datetime.now()
        log.save()
    return redirect("monitor")

@login_required
@require_http_methods(["POST"])
def time_out(request):
    form = LogForm(request.POST)
    if form.is_valid():
        log_id = form.cleaned_data['log_id']
        log = get_object_or_404(HallPass, pk = log_id)
        # check to makes sure they havent been signed out at another computer
        if log.Time_out == None:
            log.Time_out = datetime.datetime.now()
            log.save()
        destination = log.destination
        max = destination.max_people_allowed
        count_in = len(HallPass.objects.filter(destination = destination).exclude(Time_in = None).filter(Time_out = None))
        count_waiting = len(HallPass.objects.filter(destination = destination).filter(Time_in = None).filter(Time_out = None))
    return redirect("monitor")

@login_required
@require_http_methods(["POST"])
def arrival(request):
    form = ArrivalForm(request.POST)
    if form.is_valid():
        student_id = form.cleaned_data['student_id']
        student = get_object_or_404(Student, student_id = student_id)
        # checks to see if student forgot to log out
        logs = HallPass.objects.filter(student_id = student).filter(Time_out = None)
        for l in logs:
            l.Time_out = datetime.datetime.now()# logs student out 
            l.forgot_time_out = True
            l.save()
        # makes a new log
        destination_id = form.cleaned_data['destination_id']
        destination = get_object_or_404(Destination, pk = destination_id)
        max = destination.max_people_allowed
        log = HallPass(
            student_id = student,
            destination = destination,
            building = destination.building,
            Arrival_time = datetime.datetime.now()
        )
        
        count_in = len(HallPass.objects.filter(destination = destination).exclude(Time_in = None).filter(Time_out = None))
        if count_in < max:
            log.Time_in = datetime.datetime.now()
        log.save()
        
    return redirect("monitor")

@login_required
def monitor_destinations(request):
    user_profile = request.user.profile
    user_destinations = user_profile.destinations.filter(building = user_profile.building)
    
    if not user_destinations:
        return redirect(reverse('dashboard'))
    arrival_form = ArrivalForm()
    destination_data = []
    for destination in user_destinations:
        logs = HallPass.objects.filter(destination = destination).filter(Time_out = None)
        destination_data.append(
            {
                "destination":destination,
                "logs":logs,
            }
        )
        print(destination_data)
    return render(
        request,
        'pages/student_login.html',
        {
            'arrival_form': arrival_form,
            'profile': user_profile,
            # 'destinations': user_destinations,
            'destination_data':destination_data,
        }
    )
    # if count_in < max and count_waiting > 0:
    #     log = HallPass.objects.filter(destination = destination).filter(Time_in = None).filter(Time_out = None)[0]
    #     log.Time_in = datetime.datetime.now()
    #     log.save()
    
    # form = CreateHallPassForm(user_destinations = user_destinations)
    # form = CreateHallPassForm()

    # if request.method == 'POST':
    #     form = CreateHallPassForm(request.POST)
    #     hallpasses = HallPass.objects.filter(Time_out = None)

        # This form has several "action" elements that postback here.
        # if 'enter' in request.POST['action']: # Should we create a hidden input for this? 
        #     if form.is_valid(): 
        #         # print(form.cleaned_data) # See the cleaned data!
        #         destination_id = form.cleaned_data['action']
        #         print(destination_id) # This contains the action and the DestID. Maybe we separate these?
        #         d = Destination.objects.get(id = request.POST['action'].split(" ")[1])
        #         count = len(HallPass.objects.filter(destination = d).exclude(Time_in = None).filter(Time_out = None))
        #         student_id = form.cleaned_data['student']   
        #         student = Student.objects.filter(student_id=student_id)[0]
           
                # def queueCheck(bathroomCount, destination):
                #     previous_destination = None
                #     if len(HallPass.objects.filter(student_id = student).filter(Time_out = None)) > 0:
                #         previous_destination = HallPass.objects.filter(student_id = student).filter(Time_out = None)[0].destination
                #     current_destination = destination
                #     if len(HallPass.objects.filter(student_id = student).filter(Time_out = None)) >= 1:
                #         HallPass.objects.filter(student_id = student).filter(Time_out = None).update(Time_out = datetime.datetime.now())
                #         if len(HallPass.objects.filter(destination = previous_destination).filter(Time_in = None).filter(Time_out = None)) > 0:
                #             log = HallPass.objects.filter(destination = previous_destination).filter(Time_in = None).filter(Time_out = None)[0]
                #             log.Time_in = datetime.datetime.now()
                #             log.save()
                #         bathroomCount = len(HallPass.objects.filter(destination = d).exclude(Time_in = None).filter(Time_out = None))
                            
                #     if current_destination.max_people_allowed > bathroomCount:
                #         return datetime.datetime.now()

                # hallpass = HallPass(
                #     student_id = student,
                #     destination = d,
                #     building = d.building,
                #     Time_in = queueCheck(count, d)
                # )

                # hallpass.save()

                # # resets the form for another student
                # form = CreateHallPassForm()
                
            
        # elif 'out' in request.POST['action']:
        #     log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'].split(" ")[1])    
        #     student_logout_id = log_to_modify.student_id.student_id
        #     count = len(HallPass.objects.filter(destination = log_to_modify.destination).exclude(Time_in = None).filter(Time_out = None))
        #     hallpasses.filter(student_id = Student.objects.filter(student_id = student_logout_id)[0]).update(Time_out = datetime.datetime.now())
        #     if log_to_modify.destination.max_people_allowed >= count and len(HallPass.objects.filter(destination = log_to_modify.destination).filter(Time_in = None).filter(Time_out = None)) > 0:
        #         log = HallPass.objects.filter(destination = log_to_modify.destination).filter(Time_in = None).filter(Time_out = None)[0]
        #         log.Time_in = datetime.datetime.now()
        #         log.save()

       

        # elif 'in' in request.POST['action']:
        #     log_to_modify = get_object_or_404(HallPass, pk = request.POST['action'].split(" ")[1])    
        #     log_to_modify.Time_in = datetime.datetime.now()
        #     log_to_modify.save()



@login_required
def dashboard(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()

            form = ArrivalForm()
            user_profile = request.user.profile
            user_destinations = user_profile.destinations.all()

            return redirect(reverse('monitor'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'pages/dashboard.html', { 'form': profile_form, })


