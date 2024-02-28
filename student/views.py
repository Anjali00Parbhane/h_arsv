
# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from college.models import *
from student.forms import *
from django.shortcuts import render, redirect
from college.models import TechStack, Domain, Project

def student_explore(request):
    projects = Project.objects.all()
    return render(request, 'students/explore.html', {'projects': projects})

def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    print(project)
    return render(request, 'students/single_project.html', {'project': project})


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            student_obj=Student.objects.get(user=request.user)
            project.member_details_1=student_obj
            # Set the member_details_1 to the current user
            print(request)
            # project.member_details_1 = ''
            project.save()
            return redirect('project_list')  # Assuming you have a URL named 'project_list' for listing projects
    else:
        form = ProjectForm()
    return render(request, 'students/register_project.html', {'form': form})


def project_list(request):
    current_user = request.user
    print(request.user)
    try:
        student = Student.objects.get(user=current_user)

        projects = Project.objects.filter(member_details_1=student) | \
                   Project.objects.filter(member_details_2=student) | \
                   Project.objects.filter(member_details_3=student) | \
                   Project.objects.filter(member_details_4=student)
    except Student.DoesNotExist:
        return HttpResponse("No student found for the current user.")

    return render(request, 'students/personal_projects.html', {'projects': projects})



# def project_tasks(request, project_id):
#     try:
#         project = Project.objects.get(id=project_id)
#         print(project)
#         tasks=ProjectTask.objects.filter(project=project)
#         print(tasks)
#     except tasks.DoesNotExist:
#         return HttpResponse("Project does not exist")
#     return render(request, 'students/tasks.html', {'project': project, 'tasks': tasks})

def project_tasks(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        tasks = ProjectTask.objects.filter(project=project)
        if not tasks:
            return HttpResponse("No tasks found for this project.")
    except Project.DoesNotExist:
        return HttpResponse("Project does not exist")
    return render(request, 'students/tasks.html', {'project': project, 'tasks': tasks})


def task_details(request, task_id):
    task = ProjectTask.objects.get(id=task_id)
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status='Submitted'
            form.save()
            print(task.project)
            return redirect('project_tasks', project_id=task.project.id)
    else:
        form = ProjectTaskForm(instance=task)
    return render(request, 'students/task_submit.html', {'task': task, 'form': form})



def profile_dashboard(request):
    try:
        # Assuming request.user is the logged-in user
        student = get_object_or_404(Student, user=request.user)
        print(student)
        projects = Project.objects.filter(member_details_1=student) | \
                   Project.objects.filter(member_details_2=student) | \
                   Project.objects.filter(member_details_3=student) | \
                   Project.objects.filter(member_details_4=student)
    except Student.DoesNotExist:
        return HttpResponse("No student found for the current user.")

    return render(request, 'students/dashboard.html', {'projects': projects,'user':student})