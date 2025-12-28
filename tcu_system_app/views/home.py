from django.shortcuts import render, redirect
from ..models import Request, User, Project
from .auth import login_required


@login_required
def home(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    user_role_name = user.roleId.name
    user_role_lower = user_role_name.lower()

    if user_role_lower == 'estudiante': 
        # Para estudiantes solo sus propias solicitudes
        approved_count = Request.objects.filter(
            userId_student=user, 
            statusId__name__icontains='Aceptada'
        ).count()
        
        pending_count = Request.objects.filter(
            userId_student=user, 
            statusId__name__icontains='Pendiente'
        ).count()
        
        rejected_count = Request.objects.filter(
            userId_student=user, 
            statusId__name__icontains='Rechazada'
        ).count()
        
        recent_requests = Request.objects.filter(
            userId_student=user
        ).order_by('-date')[:10]
        
    elif user_role_lower == 'profesor':
        # Para profesores solicitudes de proyectos donde son encargados
        professor_projects = Project.objects.filter(userId_professor=user)
        
        if professor_projects.exists():
            approved_count = Request.objects.filter(
                projectId__in=professor_projects,
                statusId__name__icontains='Aceptada'
            ).count()
            
            pending_count = Request.objects.filter(
                projectId__in=professor_projects,
                statusId__name__icontains='Pendiente'
            ).count()
            
            rejected_count = Request.objects.filter(
                projectId__in=professor_projects,
                statusId__name__icontains='Rechazada'
            ).count()
            
            recent_requests = Request.objects.filter(
                projectId__in=professor_projects
            ).order_by('-date')[:10]
        else:
            # Si el profesor no tiene proyectos asignados
            approved_count = 0
            pending_count = 0
            rejected_count = 0
            recent_requests = Request.objects.none()
            
    else: 
        # Para otros roles (como administrador) todas las solicitudes
        approved_count = Request.objects.filter(
            statusId__name__icontains='Aceptada'
        ).count()
        
        pending_count = Request.objects.filter(
            statusId__name__icontains='Pendiente'
        ).count()
        
        rejected_count = Request.objects.filter(
            statusId__name__icontains='Rechazada'
        ).count()
        
        recent_requests = Request.objects.all().order_by('-date')[:10]
    
    total_count = approved_count + pending_count + rejected_count

    context = {
        'user_role': user_role_name,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'total_count': total_count,
        'recent_requests': recent_requests,
        'current_user': user,
        'user_full_name': f"{user.firstName} {user.lastName}",
    }
    
    return render(request, 'tcu_system_app/dashboard.html', context)