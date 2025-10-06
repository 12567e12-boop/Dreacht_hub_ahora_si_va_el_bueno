from django.shortcuts import render
from .forms import EmpleadoForm

def home(request):
    return render(request, 'app_PDF_maker/home.html')

def recursos(request):
    # For now, just render the recursos template
    return render(request, 'app_PDF_maker/recursos.html')

def requisiciones(request):
    # For now, just render the requisiciones template
    return render(request, 'app_PDF_maker/requisiciones.html')

def gafetes(request):
    form = EmpleadoForm()
    return render(request, 'app_PDF_maker/gafetes.html', {'form': form})
