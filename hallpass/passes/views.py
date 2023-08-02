from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CreateLogForm, ChooseBathroom
from .models import Student, Log, Bathroom
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import datetime
import string


@login_required
def bathroom(request, pk):   
    form = CreateLogForm()
    br = get_object_or_404(Bathroom, pk=pk)
    logs = Log.objects.filter(Time_out = None)

    if request.method == 'POST':
        if request.POST['action'] == 'Enter':
            form = CreateLogForm(request.POST)
            if len(logs.filter(bathroom = br)) < 4000:
                if form.is_valid():
                    student_id = form.cleaned_data['student']
                    student = Student.objects.filter(student_id=student_id)[0]
                    '''
                    for i in logs.filter(student_id = student):
                        i.Time_out = datetime.datetime.now()
                        i.save()
                    '''
                    log = Log(
                        student_id = student,
                        bathroom = br
                    )
                    log.save()
                    form = CreateLogForm()
            else:
                None
                # This should send a popup to the login page that say something like you have "4 students logged in already" but Im tired :(
        else:
            log_to_modify = get_object_or_404(Log, pk = request.POST['action'])        
            student_logout_id = log_to_modify.student_id.student_id

            logs.filter(student_id = Student.objects.filter(student_id = student_logout_id)[0]).update(Time_out = datetime.datetime.now())


    return render(request, 'pages/student_login.html', {'form': form, 'logs':logs.filter(bathroom = br), "room": br.room})


@login_required
def bathroom_selector(request):
    form = ChooseBathroom()
    if request.method == "POST":
        form = ChooseBathroom(request.POST)
        br_id = form['bathrooms'].value()
        url = reverse('bathroom', args=([br_id]))
        print(url)
        return redirect(reverse('bathroom', args=([br_id])))  
        
    return render(request, 'pages/bathroom.html',{'form': form})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy