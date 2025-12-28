from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from ..models import Request, Status, User, Project, File
from .auth import login_required


@login_required
def create_request(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, pk=user_id)
    
    # Solo estudiantes pueden crear solicitudes
    if user.roleId.name.lower() != 'estudiante':
        return HttpResponseForbidden("Solo los estudiantes pueden crear solicitudes")
    
    # Verificar que el estudiante tenga un proyecto asignado
    if not user.projectId:
        messages.error(request, "No tienes un proyecto asignado. Contacta al administrador.")
        return redirect('home')
    
    if request.method == 'POST':
        try:
            hours_requested = request.POST.get('hoursRequested', '').strip()
            description = request.POST.get('description', '').strip()
            date_str = request.POST.get('date', '').strip()
            
            if not all([hours_requested, description, date_str]):
                messages.error(request, "Todos los campos obligatorios deben ser completados")
                return redirect('create_request')
            
            # Convertir horas a entero
            try:
                hours = int(hours_requested)
                if hours <= 0:
                    messages.error(request, "Las horas deben ser un número positivo")
                    return redirect('create_request')
                if hours > 100:  # Límite razonable
                    messages.error(request, "Las horas no pueden exceder 100")
                    return redirect('create_request')
            except ValueError:
                messages.error(request, "Las horas deben ser un número válido")
                return redirect('create_request')
            
            # Convertir fecha
            try:
                request_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if request_date > timezone.now().date():
                    messages.error(request, "La fecha no puede ser futura")
                    return redirect('create_request')
            except ValueError:
                messages.error(request, "Formato de fecha inválido. Use YYYY-MM-DD")
                return redirect('create_request')
            
            # Obtener el status pendiente (ID 1)
            pending_status = get_object_or_404(Status, pk=1)
            
            # Crear la solicitud
            new_request = Request(
                userId_student=user,
                projectId=user.projectId,  # proyecto asignado al estudiante
                statusId=pending_status,   # Status pendiente
                hoursRequested=hours,
                description=description,
                date=request_date,
                professorComent='', 
                revisionDate=None 
            )
            new_request.save()
            
            # Manejar archivos subidos
            files = request.FILES.getlist('files')
            for uploaded_file in files:
                # Validar tamaño del archivo (máximo 10MB)
                if uploaded_file.size > 10 * 1024 * 1024:
                    messages.warning(request, f"El archivo {uploaded_file.name} excede el tamaño máximo de 10MB")
                    continue
                
                # Validar tipo de archivo
                allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.txt']
                if not any(uploaded_file.name.lower().endswith(ext) for ext in allowed_extensions):
                    messages.warning(request, f"El archivo {uploaded_file.name} tiene un tipo no permitido")
                    continue
                
                # Crear registro de archivo
                file_record = File(
                    requestId=new_request,
                    filePath=uploaded_file
                )
                file_record.save()
            
            messages.success(request, "Solicitud creada exitosamente")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f"Error al crear la solicitud: {str(e)}")
            return redirect('create_request')
    
    # GET request - mostrar formulario
    # Obtener la fecha actual para el campo de fecha
    today = timezone.now().date()
    
    context = {
        'current_user': user,
        'today': today,
        'user_role': user.roleId.name.lower(),
        'user_project': user.projectId
    }
    
    return render(request, 'tcu_system_app/requests/create_request.html', context)



@login_required
def list_requests(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(pk=user_id)
    user_role = user.roleId.name.lower()

    if user_role == 'estudiante':
        all_requests = Request.objects.filter(
            userId_student=user
        ).order_by('-date')
        
    elif user_role == 'profesor':
        professor_projects = Project.objects.filter(userId_professor=user)
        
        if professor_projects.exists():
            all_requests = Request.objects.filter(
                projectId__in=professor_projects
            ).order_by('-date')
        else:
            all_requests = Request.objects.none()
            
    else:
        all_requests = Request.objects.all().order_by('-date')

    context = {
        'all_requests': all_requests,
        'current_user': user,
        'user_role': user.roleId.name,
    }
    
    return render(request, 'tcu_system_app/requests/requests.html', context)



@login_required
def review_request(request, request_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, pk=user_id)
    if user.roleId.name.lower() == 'estudiante':
        return redirect('home')
    
    request_obj = get_object_or_404(Request, pk=request_id)
    files = File.objects.filter(requestId=request_obj)
    statuses = Status.objects.all()
    
    if request.method == 'POST':
        new_status_id = request.POST.get('status')
        comment = request.POST.get('professorComment', '')
        
        if new_status_id:
            new_status = get_object_or_404(Status, pk=new_status_id)
            request_obj.statusId = new_status
        
        if comment:
            request_obj.professorComent = comment
        
        request_obj.revisionDate = timezone.now().date()
        request_obj.save()
        
        return redirect('home')
    
    context = {
        'request': request_obj,
        'files': files,
        'statuses': statuses,
        'user_role': user.roleId.name,
    }
    
    return render(request, 'tcu_system_app/requests/review_request.html', context)


@login_required
def request_detail(request, request_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, pk=user_id)
    request_obj = get_object_or_404(Request, pk=request_id)
    files = File.objects.filter(requestId=request_obj)
    
    if user.roleId.name.lower() == 'estudiante' and request_obj.userId_student != user:
        return HttpResponseForbidden("No tienes permiso para ver esta solicitud")
    
    context = {
        'request': request_obj,
        'files': files,
        'user_role': user.roleId.name.lower(),
        'is_owner': request_obj.userId_student == user,
    }
    
    return render(request, 'tcu_system_app/requests/request_detail.html', context)
