from django.urls import path,include
from .import views


urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login/', views.all_login, name='login'),
    path('home',views.home,name='home'),
    path('register_college/', views.register_college, name='register_college'),
    path('register_student/', views.register_student, name='register_student'),
    path('register_mentor/', views.register_mentor, name='register_mentor'),
    path('', include('student.urls'),name='student_explore'),
    path('create_timeline',views.create_timeline,name='create_timeline'),
    path('create_task/', views.add_tasks_to_timeline, name='create_task'),
    path('projects-data/', views.projects_by_college, name='projects_by_college'),
    path('students-data/',views.filter_students,name='filter_students'),
    path('add_tasks/<int:timeline_id>/',views.add_tasks_to_timeline,name='add_tasks_to_timeline'),
    path('project-tasks-id/<int:project_id>/', views.project_tasks_id, name='project-tasks-id'),
    path('college-timelines/', views.college_timelines, name='college_timelines'),
    path('timeline_tasks/<int:timeline_id>/', views.timeline_tasks, name='timeline_tasks'),
    path('logout',views.logout_view,name='logout'),
    path('assign-mentors/', views.assign_mentors, name='assign_mentors'),
    # mentor urls
    path('mentor_projects/', views.mentor_projects, name='mentor_projects'),
    path('project/<int:project_id>/tasks_mentor/', views.project_tasks_mentor, name='project_tasks_mentor'),
    path('task-details-mentor/<int:task_id>/', views.task_details_mentor, name='task_details-mentor'),

 ]
