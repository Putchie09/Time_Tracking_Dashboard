# tcu_system_app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Role, Project

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mínimo 8 caracteres',
            'class': 'form-control'
        }),
        min_length=8
    )
    
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita la contraseña',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'roleId', 'projectId']
        widgets = {
            'firstName': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre',
                'class': 'form-control'
            }),
            'lastName': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'ejemplo@correo.com',
                'class': 'form-control'
            }),
            'roleId': forms.Select(attrs={
                'class': 'form-select'
            }),
            'projectId': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'firstName': 'Nombre',
            'lastName': 'Apellido',
            'email': 'Email',
            'roleId': 'Rol',
            'projectId': 'Proyecto',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar queryset para proyectos
        self.fields['projectId'].queryset = Project.objects.all()
        self.fields['projectId'].required = False
        self.fields['projectId'].empty_label = "Sin proyecto asignado"
        
        # Personalizar queryset para roles
        self.fields['roleId'].queryset = Role.objects.all()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user