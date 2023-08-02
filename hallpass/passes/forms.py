from django import forms
from django.forms import ModelForm
from sign_in.models import Student, Log, Bathroom, BathroomGender
from django.forms.widgets import TextInput

from django.core.exceptions import ValidationError

class CreateLogForm(forms.Form):
    student = forms.CharField(max_length=6)

    def clean_student(self):
        input_id = self.cleaned_data["student"]
        id_length = len(input_id)
        validate = ''
        if id_length != 6:
            validate += "must be 6 numbers /b"
            
        if not input_id.isnumeric():
            validate += "Student Id's don't contain letters /b"
            
        if len(Student.objects.filter(student_id=input_id)) <= 0:
            validate += "Must be a valid student ID"
            
        if (validate != ''):
            raise ValidationError(validate.split("/b"))

        return input_id

#form to create choices of the bathrooms
class ChooseBathroom(forms.Form):
    bathrooms = Bathroom.objects.all()
    b_options = []
    for b in bathrooms:
        b_options.append( (b.id, b.room) )

    bathroom_choices = tuple(b_options)

    bathrooms = forms.ChoiceField(choices = bathroom_choices)

class BathroomGenderForm(ModelForm):
    class Meta:
        model = BathroomGender
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }