from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CreateHallPassForm, ChooseDestination
from .models import Student, HallPass, Destination
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import datetime
import string


@login_required
def destination(request, pk):   
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
                    '''
                    for i in logs.filter(student_id = student):
                        i.Time_out = datetime.datetime.now()
                        i.save()
                    '''
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


    return render(request, 'pages/student_login.html', {'form': form, 'hallpasses':hallpasses.filter(destination = d), "room": d.room})


@login_required
def destination_selector(request):
    form = ChooseDestination()
    if request.method == "POST":
        form = ChooseDestination(request.POST)
        br_id = form['destinations'].value()
        url = reverse('destination', args=([br_id]))
        print(url)
        return redirect(reverse('destination', args=([br_id])))  
        
    return render(request, 'pages/destination.html',{'form': form})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy