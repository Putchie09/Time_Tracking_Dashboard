from django.contrib import admin
from .models import Role, Status, Project, User, Request, File


# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('roleId', 'name')
    search_fields = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('statusId', 'name')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('projectId', 'code', 'name', 'userId_professor')
    search_fields = ('name', 'code')
    list_filter = ('userId_professor',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userId', 'firstName', 'lastName', 'email', 'roleId', 'projectId')
    search_fields = ('firstName', 'lastName', 'email')
    list_filter = ('roleId', 'projectId')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestId', 'userId_student', 'projectId', 'statusId', 'hoursRequested', 'date', 'revisionDate')
    search_fields = ('description',)
    list_filter = ('statusId', 'projectId')
    autocomplete_fields = ('userId_student', 'projectId', 'statusId')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('fileId', 'requestId', 'filePath')
    list_filter = ('requestId',)
