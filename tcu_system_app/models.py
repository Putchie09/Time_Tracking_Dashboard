from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils import timezone

# Create your models here.
class Role(models.Model):
    roleId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class Status(models.Model):
    statusId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Statuses"
    
    
class Project(models.Model):
    projectId = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True, default='NA')
    name = models.CharField(max_length=200, unique=True)
    userId_professor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
    
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    roleId = models.ForeignKey(Role, on_delete=models.PROTECT)
    firstName = models.CharField(max_length=100, unique=False)
    lastName = models.CharField(max_length=100, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, unique=False)
    projectId = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    
class Request(models.Model):
    requestId = models.AutoField(primary_key=True)
    userId_student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='student_requests')
    projectId = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    statusId = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    hoursRequested = models.IntegerField()
    description = models.TextField()
    date = models.DateField(auto_now_add=False)
    professorComent = models.TextField(null=True, blank=True)
    revisionDate = models.DateField(null=True, blank=True, default=timezone.now)
    
    
class File(models.Model):
    fileId = models.AutoField(primary_key=True)
    requestId = models.ForeignKey(Request, on_delete=models.CASCADE)
    filePath = models.FileField(upload_to='uploads/')