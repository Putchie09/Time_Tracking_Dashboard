from django.urls import path
from .views.requests import list_requests, review_request, request_detail, create_request
from .views.projects import list_projects, create_project, edit_project, delete_project
from .views.users import list_users, create_user, edit_user, delete_user
from .views.auth import login, logout
from .views.home import home

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', home, name='home'),
    path('home/', home, name='home'),
    
    path('requests/', list_requests, name='requests'),
    path('requests/create/', create_request, name='create_request'),
    path('review/<int:request_id>/', review_request, name='review_request'),
    path('request/<int:request_id>/', request_detail, name='request_detail'),
    
    
    path('projects/', list_projects, name='list_projects'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/edit/<int:project_id>/', edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    
    
    path('users/', list_users, name='list_users'),
    path('users/create/', create_user, name='create_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
