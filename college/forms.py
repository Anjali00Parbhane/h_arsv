from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['college_name', 'department', 'admission_year', 'current_year', 'university_no', 'name']


class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['title', 'admission_year', 'current_yr', 'dept']
        

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'notification_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notification_date': forms.DateInput(attrs={'type': 'date'}),
            # Add widgets for other fields as needed
        }
        
class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = [ 'remark']


class StudentFilterForm(forms.ModelForm):
    # admission_year = forms.IntegerField(choices=year_choices,default=current_year)
    # current_year = forms.IntegerField()
    # department = forms.CharField(max_length=100)
    class Meta:
        model=Student
        fields=['admission_year','current_year','department']

        # def filter_students(self):
        #     admission_year = self.cleaned_data['admission_year']
        #     current_year = self.cleaned_data['current_year']
        #     department = self.cleaned_data['department']
        #     students = Student.objects.filter(admission_year=admission_year, current_year=current_year, department=department)
        #     return students