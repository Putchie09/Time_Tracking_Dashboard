from django.core.management.base import BaseCommand
from tcu_system_app.models import User, Role, Project, Status
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Crea datos iniciales para el sistema TCU'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Contraseña para el usuario administrador'
        )
    
    def handle(self, *args, **options):
        self.stdout.write("Iniciando creación de datos iniciales...")
        
        # 1. Crear roles
        roles = ['Estudiante', 'Profesor', 'Admin']
        role_objects = {}
        
        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            role_objects[role_name] = role
            if created:
                self.stdout.write(self.style.SUCCESS(f'Rol creado: {role_name}'))
            else:
                self.stdout.write(f'Rol ya existía: {role_name}')
        
        # 2. Crear estados
        statuses = ['Pendiente', 'Aceptada', 'Rechazada']
        
        for status_name in statuses:
            status, created = Status.objects.get_or_create(name=status_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Estado creado: {status_name}'))
            else:
                self.stdout.write(f'✓ Estado ya existía: {status_name}')
        
        # 3. Crear usuario administrador
        admin_email = 'admin@gmail.com'
        admin_password = options['password']
        
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create(
                roleId=role_objects['Admin'],
                firstName='Admin',
                lastName='System',
                email=admin_email,
                password=make_password(admin_password),
                projectId=None
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario administrador creado: {admin_email}'))
        else:
            self.stdout.write(f'Usuario administrador ya existe: {admin_email}')
        
        # 4. Crear profesor de ejemplo
        prof_email = 'profesor@example.com'
        if not User.objects.filter(email=prof_email).exists():
            User.objects.create(
                roleId=role_objects['Profesor'],
                firstName='Carlos',
                lastName='Rodríguez',
                email=prof_email,
                password=make_password('prof123'),
                projectId=None
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario profesor creado: {prof_email}'))
        
        # 5. Crear estudiante de ejemplo
        student_email = 'estudiante@example.com'
        if not User.objects.filter(email=student_email).exists():
            User.objects.create(
                roleId=role_objects['Estudiante'],
                firstName='Ana',
                lastName='Martínez',
                email=student_email,
                password=make_password('estu123'),
                projectId=None
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario estudiante creado: {student_email}'))
        
        # 6. Crear proyecto de ejemplo
        if not Project.objects.filter(code='TCU001').exists():
            # Obtener el profesor creado
            professor = User.objects.get(email=prof_email)
            
            project = Project.objects.create(
                code='TCU001',
                name='Proyecto de Reforestación',
                userId_professor=professor
            )
            self.stdout.write(self.style.SUCCESS(f'Proyecto creado: {project.name}'))
            
            # Asignar proyecto al estudiante
            student = User.objects.get(email=student_email)
            student.projectId = project
            student.save()
            self.stdout.write(self.style.SUCCESS(f'Proyecto asignado al estudiante: {student.email}'))
        
        self.stdout.write(self.style.SUCCESS('\n¡Datos iniciales creados exitosamente!'))
        self.stdout.write(f"\nCredenciales de acceso:")
        self.stdout.write(f"  Administrador: admin@gmail.com / {admin_password}")
        self.stdout.write(f"  Profesor: profesor@example.com / prof123")
        self.stdout.write(f"  Estudiante: estudiante@example.com / estu123")