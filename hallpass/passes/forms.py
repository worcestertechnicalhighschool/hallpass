from django import forms
from django.forms import ModelForm
from .models import Student, HallPass, Destination, Category, Profile
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

class CreateHallPassForm(forms.Form):
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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('destinations',)

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            # I think this is redundant
            'color': TextInput(attrs={'type': 'color'}),
        }