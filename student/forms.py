# forms.py
from django import forms
from college.models import Project,ProjectTask

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'project_domain', 'tech_stack', 'member_details_2', 'member_details_3', 'member_details_4']


# class TaskDetailsForm(forms.Form):
#     response = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
#     document = forms.FileField(label='Upload Document', required=False)

class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = [ 'response', 'document']
