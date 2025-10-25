from django import forms
from empleados.models import Empleado

class EmpleadoForm(forms.ModelForm):
    GAFETE_CHOICES = [
        ('cyber_robotics', 'Cyber robotics'),
        ('dreacht_strukchur', 'Dreacht & Strukchur'),
    ]

    area = forms.ChoiceField(
        choices=GAFETE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Área"
    )

    class Meta:
        model = Empleado
        exclude = ['gafete_pdf', 'fecha_alta', 'fecha_baja', 'nomina']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'puesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(default) Contratista'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional)'
            }),
            'nss': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional)'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional)'
            }),
            'tel_emg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional)'
            }),
        }
