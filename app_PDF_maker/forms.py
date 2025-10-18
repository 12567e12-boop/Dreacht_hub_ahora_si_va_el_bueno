from django import forms
from empleados.models import Empleado

class EmpleadoForm(forms.ModelForm):
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
                'placeholder': '(Opcional) Dirección'
            }),
            'nss': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional) Número de Seguro Social'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional) Teléfono'
            }),
            'tel_emg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(Opcional) Teléfono de emergencia'
            }),
        }
