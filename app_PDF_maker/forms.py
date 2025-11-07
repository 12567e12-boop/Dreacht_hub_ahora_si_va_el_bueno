from django import forms
from django.core.exceptions import ValidationError
from empleados.models import Empleado, Requisicion


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
        error_messages = {
            'nombre': {
                'required': 'Este campo es obligatorio.',
            },
            'foto': {
                'required': 'Este campo es obligatorio.',
            },
            'puesto': {
                'required': 'Este campo es obligatorio.',
            },
            'area': {
                'required': 'Este campo es obligatorio.',
            },
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'puesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contratista'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección (Opcional)'
            }),
            'nss': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NSS (Opcional)'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono (Opcional)'
            }),
            'tel_emg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de Emergencia (Opcional)'
            }),
        }


class RequisicionForm(forms.Form):
    obra = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'id': 'campo-obra',
            'placeholder': 'obra'
        }),
        error_messages={
            'required': 'El campo obra es obligatorio.',
            'max_length': 'La obra no puede exceder 200 caracteres.'
        }
    )
    ubicacion = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'id': 'campo-ubicacion',
            'placeholder': 'ubicacion'
        }),
        error_messages={
            'required': 'El campo ubicación es obligatorio.',
            'max_length': 'La ubicación no puede exceder 200 caracteres.'
        }
    )
    numero_de_articulos = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'campo',
            'id': 'campo-numero_de_articulos',
            'placeholder': 'numero de articulos'
        }),
        error_messages={
            'min_value': 'El número de artículos debe ser positivo.',
            'invalid': 'El número de artículos debe ser un entero.'
        }
    )
    fecha_soli = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'campo',
            'id': 'campo-fecha_soli',
            'type': 'date'
        }),
        error_messages={
            'required': 'La fecha de solicitud es obligatoria.',
            'invalid': 'Formato de fecha inválido.'
        }
    )
    fecha_util = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'campo',
            'id': 'campo-fecha_util',
            'type': 'date'
        }),
        error_messages={
            'invalid': 'Formato de fecha inválido.'
        }
    )
    fecha_surt = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'campo',
            'id': 'campo-fecha_surt',
            'type': 'date'
        }),
        error_messages={
            'invalid': 'Formato de fecha inválido.'
        }
    )
    contratista_soli = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'id': 'campo-contratista_soli',
            'placeholder': 'Nombre completo'
        }),
        error_messages={
            'required': 'El contratista solicitante es obligatorio.',
            'max_length': 'El nombre no puede exceder 200 caracteres.'
        }
    )
    contratista_auto = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'id': 'campo-contratista_auto',
            'placeholder': 'Nombre completo'
        }),
        error_messages={
            'required': 'El contratista autorizante es obligatorio.',
            'max_length': 'El nombre no puede exceder 200 caracteres.'
        }
    )
    area_util = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'id': 'campo-area_util',
            'placeholder': 'Ej. traumatologia'
        }),
        error_messages={
            'required': 'El área de utilidad es obligatoria.',
            'max_length': 'El área no puede exceder 200 caracteres.'
        }
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'campo',
            'id': 'campo-observaciones',
            'placeholder': 'Observaciones',
            'rows': '4',
            'cols': '50'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_soli = cleaned_data.get('fecha_soli')
        fecha_util = cleaned_data.get('fecha_util')
        fecha_surt = cleaned_data.get('fecha_surt')

        if fecha_soli and fecha_util and fecha_soli > fecha_util:
            raise ValidationError('La fecha de solicitud no puede ser posterior a la fecha de utilidad.')

        if fecha_util and fecha_surt and fecha_util > fecha_surt:
            raise ValidationError('La fecha de utilidad no puede ser posterior a la fecha de surtimiento.')

        return cleaned_data
