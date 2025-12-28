from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from ..models import User


def logout(request):
    """
    View para cerrar sesión del usuario
    """
    # Limpiar la sesión
    if 'user_id' in request.session:
        del request.session['user_id']

    # borrar datos de la sesión
    request.session.flush()
    return redirect('login')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'tcu_system_app/login.html')
        
        if check_password(password, user.password):
            request.session['user_id'] = user.userId
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'tcu_system_app/login.html')
        
    return render(request, 'tcu_system_app/login.html')



def is_authenticated(request):
    '''
    Función para verificar si el usuario está autenticado
    ''' 
    return request.session.get('user_id') is not None


def login_required(view_func):
    '''
    Decorador para proteger vistas que requieren autorización
    ''' 
    def wrapper(request, *args, **kwargs):
        # si el usuario no está autenticado, lo redirige al login
        if not is_authenticated(request):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper