from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from ..models import Project, User, Role
from .auth import login_required
from ..models import Request


@login_required
def list_projects(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, pk=user_id)
    user_role = user.roleId.name
    
    # Verificar permisos
    if user.roleId.name.lower() not in ['admin']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    # Obtener todos los proyectos
    projects = Project.objects.all().order_by('name')
    
    context = {
        'all_projects': projects,
        'user_role': user.roleId.name.lower(),
        'current_user': user,
        'user_role': user_role,
    }
    
    return render(request, 'tcu_system_app/projects/projects.html', context)


@login_required
def create_project(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    current_user = get_object_or_404(User, pk=user_id)
    
    # solo admin
    if current_user.roleId.name.lower() not in ['admin']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            code = request.POST.get('code', '').strip().upper()
            name = request.POST.get('name', '').strip()
            professor_id = request.POST.get('professorId')
            
            # Validaciones básicas
            if not all([code, name]):
                messages.error(request, "Código y nombre son campos obligatorios")
                return redirect('create_project')
            
            # Validar formato del código
            if len(code) < 2:
                messages.error(request, "El código debe tener al menos 2 caracteres")
                return redirect('create_project')
            
            # Obtener profesor si se seleccionó uno
            professor = None
            if professor_id:
                professor = get_object_or_404(User, pk=professor_id)
                # Verificar que sea un profesor
                if professor.roleId.name.lower() not in ['profesor', 'professor', 'coordinador', 'coordinator']:
                    messages.error(request, "Solo se pueden asignar profesores a los proyectos")
                    return redirect('create_project')
            
            # Crear proyecto
            project = Project(
                code=code,
                name=name,
                userId_professor=professor
            )
            project.save()
            
            messages.success(request, f"Proyecto {name} creado exitosamente")
            return redirect('list_projects')
            
        except IntegrityError:
            # Manejar error de unicidad
            if Project.objects.filter(code=code).exists():
                messages.error(request, f"El código {code} ya está registrado")
            elif Project.objects.filter(name=name).exists():
                messages.error(request, f"El nombre {name} ya está registrado")
            else:
                messages.error(request, "Error al crear el proyecto")
            return redirect('create_project')
        except Exception as e:
            messages.error(request, f"Error al crear proyecto: {str(e)}")
            return redirect('create_project')
    
    # GET request - obtener profesores disponibles
    professors = User.objects.filter(
        roleId__name__in=['Profesor', 'Professor', 'Coordinador', 'Coordinator']
    ).order_by('lastName', 'firstName')
    
    return render(request, 'tcu_system_app/projects/create_project.html', {
        'professors': professors,
        'current_user': current_user
    })


@login_required
def edit_project(request, project_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    current_user = get_object_or_404(User, pk=user_id)
    
    # solo admin
    if current_user.roleId.name.lower() not in ['admin']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            code = request.POST.get('code', '').strip().upper()
            name = request.POST.get('name', '').strip()
            professor_id = request.POST.get('professorId')
            
            # Validaciones básicas
            if not all([code, name]):
                messages.error(request, "Código y nombre son campos obligatorios")
                return redirect('edit_project', project_id=project_id)
            
            # Validar formato del código
            if len(code) < 2:
                messages.error(request, "El código debe tener al menos 2 caracteres")
                return redirect('edit_project', project_id=project_id)
            
            # Verificar si el código ya existe
            if Project.objects.filter(code=code).exclude(pk=project_id).exists():
                messages.error(request, f"El código {code} ya está registrado")
                return redirect('edit_project', project_id=project_id)
            
            # Verificar si el nombre ya existe
            if Project.objects.filter(name=name).exclude(pk=project_id).exists():
                messages.error(request, f"El nombre {name} ya está registrado")
                return redirect('edit_project', project_id=project_id)
            
            # Obtener profesor si se seleccionó uno
            professor = None
            if professor_id:
                professor = get_object_or_404(User, pk=professor_id)
                # Verificar que sea un profesor
                if professor.roleId.name.lower() not in ['profesor', 'professor', 'coordinador', 'coordinator']:
                    messages.error(request, "Solo se pueden asignar profesores a los proyectos")
                    return redirect('edit_project', project_id=project_id)
            
            # Actualizar proyecto
            project.code = code
            project.name = name
            project.userId_professor = professor
            project.save()
            
            messages.success(request, f"Proyecto {name} actualizado exitosamente")
            return redirect('list_projects')
            
        except Exception as e:
            messages.error(request, f"Error al actualizar proyecto: {str(e)}")
            return redirect('edit_project', project_id=project_id)
    
    # GET request - obtener profesores disponibles
    professors = User.objects.filter(
        roleId__name__in=['Profesor', 'Professor', 'Coordinador', 'Coordinator']
    ).order_by('lastName', 'firstName')
    
    return render(request, 'tcu_system_app/projects/edit_project.html', {
        'project': project,
        'professors': professors,
        'current_user': current_user
    })


@require_POST
@csrf_exempt
@login_required
def delete_project(request, project_id):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
        
        current_user = get_object_or_404(User, pk=user_id)
        
        # solo admin
        if current_user.roleId.name.lower() not in ['admin']:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
        
        project_to_delete = get_object_or_404(Project, pk=project_id)
        
        # Verificar si el proyecto tiene estudiantes asignados
        has_students = User.objects.filter(projectId=project_to_delete).exists()
        
        if has_students:
            return JsonResponse({
                'success': False, 
                'error': 'No se puede eliminar el proyecto porque tiene estudiantes asignados'
            }, status=400)
        
        # Verificar si el proyecto tiene solicitudes asociadas
        
        has_requests = Request.objects.filter(projectId=project_to_delete).exists()
        
        if has_requests:
            return JsonResponse({
                'success': False, 
                'error': 'No se puede eliminar el proyecto porque tiene solicitudes asociadas'
            }, status=400)
        
        # Guardar información para el mensaje
        project_name = project_to_delete.name
        project_to_delete.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Proyecto {project_name} eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)