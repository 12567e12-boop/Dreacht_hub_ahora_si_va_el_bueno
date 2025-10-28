import os
from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from pypdf import PdfReader, PdfWriter

from .forms import EmpleadoForm


# ===================================
# Páginas simples
# ===================================
def home(request):
    return render(request, 'app_PDF_maker/home.html')

def recursos(request):
    return render(request, 'app_PDF_maker/recursos.html')

def requisiciones(request):
    if request.method == "POST":
        obra = request.POST.get('obra', '')
        ubicacion = request.POST.get('ubicacion', '')
        numero_de_articulos = request.POST.get('numero_de_articulos', '')
        fecha_soli = request.POST.get('fecha_soli', '')
        fecha_util = request.POST.get('fecha_util', '')
        fecha_surt = request.POST.get('fecha_surt', '')
        contratista_soli = request.POST.get('contratista_soli', '')
        contratista_auto = request.POST.get('contratista_auto', '')
        area_util = request.POST.get('area_util', '')

        # Debug: print POST data
        print("POST data:", request.POST)

        try:
            base_pdf_path = os.path.join(
                settings.BASE_DIR,
                'app_PDF_maker', 'static', 'media', 'requiscion_template.pdf'
            )
            print(f"Usando plantilla base: {base_pdf_path}")
            if not os.path.exists(base_pdf_path):
                return HttpResponse(f"Error: plantilla base no encontrada en {base_pdf_path}", status=500)

            # --- Crear capa con texto ---
            overlay_buffer = BytesIO()
            c = canvas.Canvas(overlay_buffer, pagesize=letter)

            # Coordenadas en puntos (usa las que tienes en JS)
            campos = {
    'obra':               (231.4, 832, obra),
    'ubicacion':          (249.6, 801.2, ubicacion),
    'numero_de_articulos':(299, 769.6, numero_de_articulos),
    'fecha_soli':         (624, 832, fecha_soli),
    'fecha_util':         (624, 801.2, fecha_util),
    'fecha_surt':         (624, 769.6, fecha_surt),
    'contratista_soli':   (221, 730.6, contratista_soli),
    'contratista_auto':   (147.9, 693.9, contratista_auto),
    'area_util':          (212.9, 656.5, area_util),
}





            c.setFont("Helvetica", 10)  # Ajusta tamaño/fuente si es necesario
            for key, (x, y, text) in campos.items():
                if text:
                    c.drawString(x, y, text)
            c.showPage()
            c.save()
            overlay_buffer.seek(0)

            # --- Leer plantilla base PDF y combinar ---
            reader = PdfReader(base_pdf_path)
            writer = PdfWriter()

            base_page = reader.pages[0]
            overlay_pdf = PdfReader(overlay_buffer)
            overlay_page = overlay_pdf.pages[0]

            # Fusiona overlay sobre página base
            base_page.merge_page(overlay_page)
            writer.add_page(base_page)

            # --- Escribir PDF final ---
            final_buffer = BytesIO()
            writer.write(final_buffer)
            final_buffer.seek(0)

            response = HttpResponse(final_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="requisicion_completada.pdf"'
            return response

        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return HttpResponse(f"Error generando PDF: {str(e)}", status=500)

    # Si GET u otro método
    return render(request, 'app_PDF_maker/requisiciones.html')


# ===================================
# Generación de gafetes
# ===================================
def gafetes(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            area = form.cleaned_data.get('area')

            # Elegir plantillas según área
            if area == 'cyber_robotics':
                frente_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'cyber_front_gafete.jpg')
                reverso_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'cyber_back_gafete.jpg')
                empresa = "Cyber"
            elif area == 'dreacht_strukchur':
                frente_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_front_gafete.jpg')
                reverso_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_back_gafete.jpg')
                empresa = "Dreacht"
            else:
                frente_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_front_gafete.jpg')
                reverso_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_back_gafete.jpg')
                empresa = "Dreacht"

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # ======= LADO FRONTAL =======
            frente = ImageReader(frente_path)
            c.drawImage(frente, 0, 0, width=width, height=height)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(120, 500, form.cleaned_data['nombre'])
            c.setFont("Helvetica", 12)
            c.drawString(120, 480, form.cleaned_data['puesto'])

            # Foto del empleado
            if form.cleaned_data.get('foto'):
                uploaded_file = form.cleaned_data['foto']
                image_bytes = uploaded_file.read()
                image_io = BytesIO(image_bytes)
                foto = ImageReader(image_io)
                c.drawImage(foto, 50, 400, width=100, height=100)

            c.showPage()

            # ======= LADO TRASERO =======
            reverso = ImageReader(reverso_path)
            c.drawImage(reverso, 0, 0, width=width, height=height)
            c.setFont("Helvetica", 10)
            c.drawString(100, 200, f"Tel: {form.cleaned_data.get('tel', '')}")
            c.drawString(100, 180, f"Emergencia: {form.cleaned_data.get('tel_emg', '')}")
            c.drawString(100, 160, f"NSS: {form.cleaned_data.get('nss', '')}")

            c.save()
            buffer.seek(0)

            empleado = form.save()
            nombre_pdf = f'gafete de {empleado.nombre} {empresa}.pdf'
            empleado.gafete_pdf.save(nombre_pdf, buffer)
            empleado.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
            return response
    else:
        form = EmpleadoForm()

    return render(request, 'app_PDF_maker/gafetes.html', {'form': form})
