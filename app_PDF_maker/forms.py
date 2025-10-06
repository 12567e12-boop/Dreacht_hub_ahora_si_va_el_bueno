from django import forms
from empleados.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ['gafete_pdf', 'fecha_alta', 'fecha_baja', 'nomina']
