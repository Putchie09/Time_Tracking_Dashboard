from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import re
from ..models import User, Role, Project
from .auth import login_required  

@login_required
def list_users(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, pk=user_id)
    user_role = user.roleId.name
    
    # solo admin
    if user.roleId.name.lower() not in ['admin']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    # Obtener todos los usuarios
    users = User.objects.all().order_by('lastName', 'firstName')

    return render(request, 'tcu_system_app/users/users.html', {
        'users': users, 
        'current_user': user, 
        'user_role': user_role,
        'roles': Role.objects.all(),
        'projects': Project.objects.all()
    })


@login_required
def create_user(request):
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
            first_name = request.POST.get('firstName', '').strip()
            last_name = request.POST.get('lastName', '').strip()
            email = request.POST.get('email', '').strip().lower()
            role_id = request.POST.get('roleId')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')
            project_id = request.POST.get('projectId')
            
            # Validaciones básicas
            if not all([first_name, last_name, email, role_id, password]):
                messages.error(request, "Todos los campos obligatorios deben ser completados")
                return redirect('create_user')
            
            # Validar formato de email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                messages.error(request, "El formato del email no es válido")
                return redirect('create_user')
            
            # Validar contraseña
            if password != confirm_password:
                messages.error(request, "Las contraseñas no coinciden")
                return redirect('create_user')
            
            if len(password) < 6:
                messages.error(request, "La contraseña debe tener al menos 6 caracteres")
                return redirect('create_user')
            
            # Obtener rol
            role = get_object_or_404(Role, pk=role_id)
            
            # Si es estudiante, validar proyecto
            project = None
            if role.name.lower() == 'estudiante':
                if project_id:
                    project = get_object_or_404(Project, pk=project_id)
            elif project_id:
                messages.warning(request, "Solo los estudiantes pueden tener proyectos asignados")
            
            # Crear usuario
            user = User(
                firstName=first_name,
                lastName=last_name,
                email=email,
                roleId=role,
                projectId=project
            )
            user.set_password(password)
            user.save()
            
            messages.success(request, f"Usuario {first_name} {last_name} creado exitosamente")
            return redirect('list_users')
            
        except IntegrityError:
            messages.error(request, "El email ya está registrado")
            return redirect('create_user')
        except Exception as e:
            messages.error(request, f"Error al crear usuario: {str(e)}")
            return redirect('create_user')
    
    # GET request
    roles = Role.objects.all()
    projects = Project.objects.all()
    
    return render(request, 'tcu_system_app/users/create_user.html', {
        'roles': roles,
        'projects': projects,
        'current_user': current_user
    })


@login_required
def edit_user(request, user_id):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return redirect('login')
    
    current_user = get_object_or_404(User, pk=current_user_id)
    
    # solo admin
    if current_user.roleId.name.lower() not in ['admin']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    user_to_edit = get_object_or_404(User, pk=user_id)
    
    # Prevenir edición de administradores
    if user_to_edit.roleId.name.lower() == 'admin':
        messages.error(request, "No se pueden editar los administradores desde esta vista")
        return redirect('list_users')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            first_name = request.POST.get('firstName', '').strip()
            last_name = request.POST.get('lastName', '').strip()
            email = request.POST.get('email', '').strip().lower()
            role_id = request.POST.get('roleId')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')
            project_id = request.POST.get('projectId')
            
            # Validaciones básicas
            if not all([first_name, last_name, email, role_id]):
                messages.error(request, "Todos los campos obligatorios deben ser completados")
                return redirect('edit_user', user_id=user_id)
            
            # Validar formato de email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                messages.error(request, "El formato del email no es válido")
                return redirect('edit_user', user_id=user_id)
            
            # Verificar si el email ya existe (excluyendo al usuario actual)
            if User.objects.filter(email=email).exclude(pk=user_id).exists():
                messages.error(request, "El email ya está registrado por otro usuario")
                return redirect('edit_user', user_id=user_id)
            
            # Obtener rol
            role = get_object_or_404(Role, pk=role_id)
            
            # Manejar proyecto según el rol
            project = None
            if role.name.lower() == 'estudiante':
                if project_id:
                    project = get_object_or_404(Project, pk=project_id)
            else:
                # Si no es estudiante, limpiar el proyecto
                project = None
            
            # Actualizar usuario
            user_to_edit.firstName = first_name
            user_to_edit.lastName = last_name
            user_to_edit.email = email
            user_to_edit.roleId = role
            user_to_edit.projectId = project
            
            # Actualizar contraseña si se proporcionó una nueva
            if password and password.strip():
                if password != confirm_password:
                    messages.error(request, "Las contraseñas no coinciden")
                    return redirect('edit_user', user_id=user_id)
                
                if len(password) < 6:
                    messages.error(request, "La contraseña debe tener al menos 6 caracteres")
                    return redirect('edit_user', user_id=user_id)
                
                user_to_edit.set_password(password)
            
            user_to_edit.save()
            
            messages.success(request, f"Usuario {first_name} {last_name} actualizado exitosamente")
            return redirect('list_users')
            
        except Exception as e:
            messages.error(request, f"Error al actualizar usuario: {str(e)}")
            return redirect('edit_user', user_id=user_id)
    
    # GET request
    roles = Role.objects.all()
    projects = Project.objects.all()
    
    return render(request, 'tcu_system_app/users/edit_user.html', {
        'user': user_to_edit,
        'roles': roles,
        'projects': projects,
        'current_user': current_user
    })


@require_POST
@csrf_exempt
@login_required
def delete_user(request, user_id):
    try:
        current_user_id = request.session.get('user_id')
        if not current_user_id:
            return JsonResponse({'success': False, 'error': 'No autenticado'}, status=401)
        
        current_user = get_object_or_404(User, pk=current_user_id)
        
        # solo admin
        if current_user.roleId.name.lower() not in ['admin']:
            return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)
        
        user_to_delete = get_object_or_404(User, pk=user_id)
        
        # No permitir eliminar administradores
        if user_to_delete.roleId.name.lower() == 'admin':
            return JsonResponse({
                'success': False, 
                'error': 'No se puede eliminar a un administrador'
            }, status=400)
        
        # No permitir eliminar al propio usuario
        if int(user_id) == int(current_user_id):
            return JsonResponse({
                'success': False, 
                'error': 'No puedes eliminar tu propia cuenta'
            }, status=400)
        
        # Verificar si el usuario tiene solicitudes asociadas
        from ..models import Request
        has_requests = Request.objects.filter(userId_student=user_to_delete).exists()
        
        if has_requests:
            return JsonResponse({
                'success': False, 
                'error': 'No se puede eliminar el usuario porque tiene solicitudes asociadas'
            }, status=400)
        
        # Guardar información para el mensaje
        user_name = f"{user_to_delete.firstName} {user_to_delete.lastName}"
        user_to_delete.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Usuario {user_name} eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)