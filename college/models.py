from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from datetime import datetime

class CustomUser(AbstractUser):
    USER = (
        (1,'COORDINATOR'),
        (2,'STUDENT'),
        (3,'MENTOR'),
    ) 
    user_type = models.CharField(choices=USER, max_length=50,default=1)




class College(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
    
import datetime
def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year


class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    college_name = models.ForeignKey(College, on_delete=models.CASCADE,default=1)
    department = models.CharField(max_length=100)
    admission_year = models.IntegerField(choices=year_choices,default=current_year)
    current_year = models.IntegerField()
    university_no=models.IntegerField()
    name=models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        current_year = datetime.datetime.now().year
        if self.admission_year:
            self.current_year = current_year - self.admission_year
        super().save(*args, **kwargs)
            
    def __str__(self):
        print(self.__dict__)
        return self.name
    
class Domain(models.Model):
    domain_name = models.CharField(max_length=100)
    def __str__(self):
        return self.domain_name
class TechStack(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Timeline(models.Model):
    title = models.CharField(max_length=200)
    admission_year = models.IntegerField(choices=year_choices,default=current_year)
    current_yr = models.IntegerField()
    dept = models.CharField(max_length=100)
    college=models.ForeignKey(College,on_delete=models.CASCADE,default='1')
    def __str__(self):
        return (str(self.title)) 
    
class Mentor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    college_name = models.ForeignKey(College, on_delete=models.CASCADE,default=1)
    department = models.CharField(max_length=100)
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name=models.CharField(max_length=100, default='')
    def __str__(self):
        return self.name
    
class Project(models.Model):
    project_title = models.CharField(max_length=200)
    project_domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)
    College=models.ForeignKey(College,on_delete=models.DO_NOTHING,default=1)
    tech_stack=models.ForeignKey(TechStack, on_delete=models.DO_NOTHING)
    support_doc = models.FileField(upload_to='documents/', blank=True, null=True)
    member_details_1 = models.ForeignKey(Student,related_name='member_1', on_delete=models.CASCADE)
    member_details_2 = models.ForeignKey(Student,related_name='member_2' ,on_delete=models.CASCADE)
    member_details_3 = models.ForeignKey(Student,related_name='member_3', on_delete=models.CASCADE)
    member_details_4 = models.ForeignKey(Student,related_name='member_4', on_delete=models.CASCADE)
    mentor_id=models.ForeignKey(Mentor,on_delete=models.CASCADE,null=True, blank=True)
    timeline_id=models.ForeignKey(Timeline,on_delete=models.CASCADE,null=True, blank=True)
    abstract=models.CharField(max_length=500,blank=True, null=True)
    # image_1 = models.ImageField(upload_to='images/')
    # image_2 = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.project_title
    

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    notification_date = models.DateField()

    def __str__(self):
        return self.name

class TimelineTasks(models.Model):
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
    timeline_title = models.ForeignKey(Timeline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timeline_title.title} - {self.task_name.name}"

class ProjectTask(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('InProgress', 'In Progress'),
        ('Submitted','Submitted'),
        ('Reassigned','Re Assigned')
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    response = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return f"{self.project} - {self.task_name}"
