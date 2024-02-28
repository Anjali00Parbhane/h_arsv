import random
from django.shortcuts import render, redirect, HttpResponse
from django.db import IntegrityError
# from django.contrib.auth.models import User
from college.EmailBackend import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from college.models import *
from .forms import *
from .middlewares import auth
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password



def all_login(request):
    if request.method == "POST":
        user = EmailBackend.authenticate(request,
                                           username=request.POST.get('email'),
                                           password=request.POST.get('password'),)
        if user!=None:
          login(request,user)
          user_type = user.user_type
          print(user_type)
          if user_type == '1':
               return redirect('home')
          elif user_type == '2':
               return redirect('student_explore')
          elif user_type == '3':
               return redirect('mentor_projects')
          else:
               messages.error(request,'Email and password are invalid')
               # return redirect('login')
               return redirect('login')
     
    else:
        messages.error(request,'Email and password are invalid')
        return render(request,'welcome/login.html')

@login_required
# @auth
def home(request):
    return render(request,'Coordinator/index.html')

def welcome_page(request):
     return render(request,'welcome/welcome_page.html')

def logout_view(request):
     logout(request)
     return redirect('login')

# def allow_to_college(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             user = request.user
#             if user.user_type == '1':
#                 try:
#                     # Retrieve the college associated with the admin user
#                     current_college = College.objects.get(admin=user)
#                     if current_college.verify:
#                         return view_func(request, *args, **kwargs)
#                     else:
#                         messages.error(request, "Your account is not verified yet. Please contact the coordinator for verification.")
#                         return redirect('login')
#                 except College.DoesNotExist:
#                     messages.error(request, "No college associated with the logged-in user.")
#                     return redirect('login')
#             else:
#                 messages.error(request, "You are logged in with a different account. Please login with the correct account.")
#                 return redirect('login')
#         else:
#             messages.error(request, "You need to login first.")
#             return redirect('login')

#     return wrapper_func


def register_college(request):
     if request.method == "POST":
        first_name = request.POST.get('first_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        request.session['first_name'] = first_name
        request.session['address'] = address
        request.session['email'] = email
        request.session['username'] = username
        request.session['password'] = password1
        request.session['user_type'] = 1

        if password1 == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exist') 
                return redirect('register_college')
            
            elif CustomUser.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exist')
                return redirect('register_college')
            else:
                sent_otp(request)
                return render(request,'otp.html', {'email':email})
            
        else:
        # else:
        #   user = CustomUser(
        #      first_name = first_name,
        #      email = email,
        #      username = username,
        #      password = password,
        #      user_type = 1,
        #   )

        #   user.set_password(password)
        #   user.save()

        #   college = College(
        #       admin = user,
        #       address = address,
        #   ) 
        #   college.save()
        #   messages.success(request, 'College registered successfully')
        #   return redirect('login')
            messages.info(request,"password mismatch")
            return render(request,'welcome/register_college.html') 
     
     

def send_otp(request):
    s=""
    for x in range(0,4):
      s+=str(random.randint(0,9))
        
    request.session["otp"]=s
        
    send_mail("otp for sign up", s, 'hireziarsv@gmail.com', [request.session['email']],fail_silently=False)
        
    return render(request, "otp.html")

def otp_verification(request):
    if request.method=='POST':
        otp_=request.POST.get("otp")

    if otp_==request.POST.get("otp"):
        encryptedpassword=make_password(request.session['password'])

        nameuser=CustomUser(first_name = request.session['first_name'],email=request.session['email'],username=request.session['username'],password=encryptedpassword,user_type = request.session['user_type'])
        
        nameuser.save()
        college = College(admin = nameuser,address=request.session['address'])
        college.save()
        
        messages.info(request, 'signed in successfully...')
        
        CustomUser.is_active=True
        
        return redirect('login')
    else:
        messages.error(request, "otp doesn't match")

        return render(request, 'otp.html')


@login_required
#@allow_to_college
def register_student(request):
     if request.method == "POST":
        first_name = request.POST.get('name')
        department = request.POST.get('department')
        current_year = request.POST.get('current_year')
        admission_year = request.POST.get('admission_year')
        university_no = request.POST.get('university_no')
        email = request.POST.get('email')
     #    username = request.POST.get('username')
        password = request.POST.get('password')

     #    college_name = request.user.first_name
        college_obj = College.objects.filter(admin=request.user)[0]
   
        
        if CustomUser.objects.filter(email=email).exists():
          print('email',email)
          messages.warning(request, 'Email already exist') 
          return redirect('register_student')
        
        else:
          user = CustomUser(
             first_name = first_name,
             email = email,
             username = email,
             password = password,
             user_type = 2,
          )

          user.set_password(password)
          user.save()

          student = Student(
              user = user,
              college_name = college_obj,
              department = department,
              current_year = current_year,
              university_no = university_no,
              admission_year=int(admission_year),
              name=first_name
          ) 
          student.save()
          print(student.id)
          print("student regi succ")
          messages.success(request, 'College registered successfully')
          return redirect('register_student')
     
     return render(request,'Coordinator/register_student.html') 



# def register_mentor(request):
#     from django.contrib import messages
@login_required
#@allow_to_college
def register_mentor(request):
    domain=Domain.objects.all()
    if request.method == "POST":
        first_name = request.POST.get('name')
        department = request.POST.get('department')
        domain_id = request.POST.get('domain_id')
        email = request.POST.get('email')
        password = request.POST.get('password')

        college_obj = College.objects.filter(admin=request.user).first()

        if college_obj is None:
            messages.error(request, 'No college associated with the logged-in user')
            return redirect('register_mentor')

        elif CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('register_mentor')
        
    #     else:
    #         user = CustomUser.objects.create( 
    #             # change
    #             first_name=first_name,
    #             email=email,
    #             username=email,
    #             password=password,
    #             user_type=3,  # Assuming mentor user type is 3
    #         )

    #         mentor = Mentor.objects.create(
    #             user=user,
    #             college_name=college_obj,
    #             department=department,
    #             domain_id=Domain.objects.get(id=domain_id),
    #             name=first_name
    #         )
    #         messages.success(request, 'Mentor registered successfully')
    #         return redirect('register_mentor')
    # print(domain)
    # return render(request, 'Coordinator/register_mentor.html',{'domains':domain})
        else:
            try:
                user = CustomUser.objects.create( 
                    first_name=first_name,
                    email=email,
                    username=email,
                    password=password,
                    user_type=3,  # Assuming mentor user type is 3
                )
                user.save()
                mentor = Mentor.objects.create(
                    user=user,
                    college_name=college_obj,
                    department=department,
                    domain_id=Domain.objects.get(id=domain_id),
                    name=first_name
                )
                mentor.save()
                messages.success(request, 'Mentor registered successfully')
                return redirect('register_mentor')
            except IntegrityError:
                messages.error(request, 'An error occurred while registering the mentor')
                return redirect('register_mentor')

    return render(request, 'Coordinator/register_mentor.html',{'domains':domain})

@login_required
#@allow_to_college
def create_timeline(request):
    if request.method == 'POST':
        form = TimelineForm(request.POST)
        print(form)
        if form.is_valid():
            # timeline = form.save()
            try:
                projects_to_update = Project.objects.get(
                    # timeline_id__isnull=True,
                    member_details_1__admission_year=form.cleaned_data['admission_year'],
                    member_details_1__current_year=form.cleaned_data['current_yr'],
                    member_details_1__department=form.cleaned_data['dept']
               )
                projects_to_update.timeline_id=timeline 
                timeline = form.save()
                print('hello')          
                return redirect('add_tasks_to_timeline', timeline_id=timeline.id)
            except:
                pass
    else:
        form = TimelineForm()
        print(form)
    return render(request, 'Coordinator/create_timeline.html', {'form': form})

@login_required
def add_tasks_to_timeline(request, timeline_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task=form.save()
            task_name = form.cleaned_data['name']
            task = Task.objects.get(name=task_name)
            timeline_task = TimelineTasks.objects.create(
                task_name=task,
                timeline_title_id=timeline_id
            )

            return redirect('add_tasks_to_timeline', timeline_id=timeline_id)
    else:
        form = TaskForm()
    return render(request, 'Coordinator/add_tasks.html', {'form': form})


@login_required
def projects_by_college(request):
    username = request.user
    college=College.objects.filter(admin=username)
    projects = Project.objects.filter(College__in=college)
    return render(request, 'Coordinator/project_data.html', {'projects': projects})

@login_required
def project_tasks_id(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        print(project)
        tasks=ProjectTask.objects.filter(project=project)
        print(tasks)
    except tasks.DoesNotExist:
        return HttpResponse("Project does not exist")
    return render(request, 'Coordinator/project_status.html', {'project': project, 'tasks': tasks})

@login_required
def college_timelines(request):
    # Assuming the logged-in user's college is stored in request.user.college
    username = request.user
    college=College.objects.get(admin=username)
    timelines = Timeline.objects.filter(college=college)
    return render(request, 'Coordinator/college_timelines.html', {'timelines': timelines})

@login_required
def timeline_tasks(request, timeline_id):
    timeline_tasks = TimelineTasks.objects.filter(timeline_title_id=timeline_id)
    print(timeline_tasks)
    task_names = [task.task_name for task in timeline_tasks]
    print(task_names)
    return render(request, 'Coordinator/timeline_tasks.html', {'timeline_tasks': task_names})

@login_required
def filter_students(request):
    if request.method == 'POST':
        form = StudentFilterForm(request.POST)
        if form.is_valid():
            admission_year = form.cleaned_data['admission_year']
            current_year = form.cleaned_data['current_year']
            department = form.cleaned_data['department']
            students = Student.objects.filter(admission_year=admission_year, current_year=current_year, department=department)
            print(students)
            return render(request,'Coordinator/students_data.html', {'students':students,'form':form})
    else:
        form=StudentFilterForm()
    return render(request, 'Coordinator/students_data.html', {'form': form})


# def assign_mentors(request):
#     if request.method == 'POST':
#         for key, value in request.POST.items():
#             print("k",key,"v",value)
#             if key.startswith('mentor_'):
#                 project_id = key.split('_')[-1]
#                 mentor_id = value
#                 project = Project.objects.get(id=project_id)
#                 mentor = Mentor.objects.get(id=mentor_id)
#                 print(project,mentor)
#                 project.mentor = mentor
#                 project.save()
#                 print(project.mentor)
#         return redirect('assign_mentors')  # Redirect back to the same page after assigning mentors
#         return HttpResponse("Success")
    
#     # username = request.user
#     college=College.objects.filter(admin=request.user).first()
#     projects = Project.objects.filter(College=college)
#     mentors_by_domain = {}
#     for project in projects:
#         domain_mentors = Mentor.objects.filter(domain_id=project.project_domain)
#         mentors_by_domain[project] = domain_mentors
#     # print(college,mentors_by_domain)
#     return render(request, 'Coordinator/assign_mentors.html', {'projects': projects, 'mentors_by_domain': mentors_by_domain})

@login_required
#@allow_to_college
def assign_mentors(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('mentor_'):
                project_id = key.split('_')[-1]
                mentor_id = value
                project = Project.objects.get(id=project_id)
                mentor = Mentor.objects.get(id=mentor_id)
                project.mentor_id = mentor
                project.save()
        return redirect('assign_mentors')
    
    college = College.objects.filter(admin=request.user).first()
    projects = Project.objects.filter(College=college)
    mentors_by_domain = {}
    for project in projects:
        domain_mentors = Mentor.objects.filter(domain_id=project.project_domain)
        mentors_by_domain[project] = domain_mentors

    return render(request, 'Coordinator/assign_mentors.html', {'projects': projects, 'mentors_by_domain': mentors_by_domain})

@login_required
def mentor_projects(request):
    username = request.user    
    mentor_id = Mentor.objects.get(user=username)
    
    # Retrieve all projects where the mentor is assigned as a mentor
    projects = Project.objects.filter(mentor_id=mentor_id)
    
    return render(request, 'mentors/mentor_project.html', {'projects': projects})

@login_required
def project_tasks_mentor(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        print(project)
        tasks=ProjectTask.objects.filter(project=project)
        print(tasks)
    except tasks.DoesNotExist:
        return HttpResponse("Project does not exist")
    return render(request, 'mentors/tasks.html', {'project': project, 'tasks': tasks})

# def task_details_mentor(request, task_id):
#     task = ProjectTask.objects.get(id=task_id)
#     if request.method == 'POST':
#         form = ProjectTaskForm(request.POST, request.FILES, instance=task)
#         if form.is_valid():
#             task.status='Submitted'
#             form.save()
#             print(task.project)
#             return redirect('project_tasks', project_id=task.project.id)
#     else:
#         form = ProjectTaskForm(instance=task)
#     return render(request, 'mentors/task_verify.html', {'task': task, 'form': form})

# def task_details_mentor(request, task_id):
#     task = ProjectTask.objects.get(id=task_id)
#     if request.method == 'POST':
#         form = ProjectTaskForm(request.POST, request.FILES, instance=task)
#         if form.is_valid():
#             form.save()
#             project_id = task.project.id
#             print(project_id)
#             return redirect('project_tasks', project_id=project_id)
#         print(request.POST)
#         if 'verify' in request.POST:
#             task.status = 'Verified'
#             task.save()
#             return redirect('project_tasks_mentor', project_id=task.project.id)  
            
#         elif 'reassign' in request.POST:
#             return redirect('mentors/tasks.html', project_id=task.project.id)  
#     else:
#         form = ProjectTaskForm(instance=task)

#     return render(request, 'mentors/task_verify.html', {'task': task, 'form': form})

@login_required
def task_details_mentor(request, task_id):
    task = ProjectTask.objects.get(id=task_id)
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            project_id = task.project.id
            print(project_id)
            return redirect('project_tasks', project_id=project_id)
        print(request.POST)
        if 'verify' in request.POST:
            task.status = 'Verified'
            task.save()
            return redirect('project_tasks_mentor', project_id=task.project.id)  
            
        elif 'reassign' in request.POST:
            return redirect('mentors/tasks.html', project_id=task.project.id)  
    else:
        form = ProjectTaskForm(instance=task)

    return render(request, 'mentors/task_verify.html', {'task': task, 'form': form})

