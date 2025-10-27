from textwrap import wrap
from django.shortcuts import render
from django.http import HttpResponse
from .forms import EmpleadoForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings
from PIL import Image
from pypdf import PdfReader, PdfWriter


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

        # PDF base
        base_pdf_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'requiscion_template.pdf')

        # Leer el PDF base con pypdf
        reader = PdfReader(base_pdf_path)
        writer = PdfWriter()

        # Copiar la primera página
        page = reader.pages[0]
        writer.add_page(page)

        # Crear un buffer para el overlay
        overlay_buffer = BytesIO()
        c = canvas.Canvas(overlay_buffer, pagesize=letter)

        # Escribir los campos (coordenadas ajustadas al template, y invertida para y=0 arriba)
        height = 792
        c.setFont("Helvetica", 20)  # Aumentar tamaño para debug
        c.setFillColorRGB(1, 0, 0)  # Rojo para visibilidad
        # Debug text at top-left
        c.drawString(50, 750, f"Obra: {obra}")
        c.drawString(50, 720, f"Ubicacion: {ubicacion}")
        c.drawString(50, 690, f"Num Art: {numero_de_articulos}")
        c.drawString(50, 660, f"Fecha Soli: {fecha_soli}")
        c.drawString(50, 630, f"Fecha Util: {fecha_util}")
        c.drawString(50, 600, f"Fecha Surt: {fecha_surt}")
        c.drawString(50, 570, f"Contratista Soli: {contratista_soli}")
        c.drawString(50, 540, f"Contratista Auto: {contratista_auto}")
        c.drawString(50, 510, f"Area Util: {area_util}")
        # Original positions (adjusted)
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(178, height - 640, obra)
        c.drawString(192, height - 616, ubicacion)
        c.drawString(230, height - 592, numero_de_articulos)
        c.drawString(480, height - 640, fecha_soli)
        c.drawString(480, height - 616, fecha_util)
        c.drawString(480, height - 592, fecha_surt)
        c.drawString(170, height - 562, contratista_soli)
        c.drawString(113, height - 533, contratista_auto)
        c.drawString(163, height - 505, area_util)

        c.save()
        overlay_buffer.seek(0)

        # Leer el overlay como PDF
        overlay_reader = PdfReader(overlay_buffer)
        overlay_page = overlay_reader.pages[0]

        # Fusionar el overlay con la página base
        page.merge_page(overlay_page)

        # Escribir el PDF final
        final_buffer = BytesIO()
        writer.write(final_buffer)
        final_buffer.seek(0)

        # Mostrar PDF inline
        response = HttpResponse(final_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="requisicion_completada.pdf"'
        return response

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

            # Crear PDF en memoria
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

            # Guardar empleado en DB y PDF
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
# ===================================
# Generación de gafetes lado a lado
# ===================================
def gafetes(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            area = form.cleaned_data.get('area')

            # =====================================
            # Plantillas y coordenadas por área
            # =====================================
            if area == 'cyber_robotics':
                frente_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'cyber_front_gafete.jpg')
                reverso_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'cyber_back_gafete.jpg')
                empresa = "Cyber"
                text_x = 90
                text_y_start = 520
                foto_x = 135
                foto_y = 570

            elif area == 'dreacht_strukchur':
                frente_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_front_gafete.jpg')
                reverso_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_back_gafete.jpg')
                empresa = "Dreacht"
                text_x = 90
                text_y_start = 535
                foto_x = 131
                foto_y = 575

            else:
                frente_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_front_gafete.jpg')
                reverso_path = os.path.join(settings.BASE_DIR, 'app_PDF_maker', 'static', 'media', 'dreacht_back_gafete.jpg')
                empresa = "Dreacht"
                text_x = 90
                text_y_start = 720
                foto_x = 200
                foto_y = 675

            # =====================================
            # Crear PDF
            # =====================================
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            gafete_w = 174
            gafete_h = 302.4
            margin_y = height - gafete_h - 100
            margin_x = 70
            gap = 0

            # ======= Función auxiliar para texto multilinea =======
            def draw_wrapped_text(c, text, x, y, max_width, line_height=10):
                """
                Divide el texto si excede el ancho máximo (en puntos)
                y lo dibuja línea por línea hacia abajo.
                """
                wrapped_lines = []
                current_line = ""
                for word in text.split():
                    test_line = f"{current_line} {word}".strip()
                    if c.stringWidth(test_line, "Helvetica-Bold", 8) <= max_width:
                        current_line = test_line
                    else:
                        wrapped_lines.append(current_line)
                        current_line = word
                wrapped_lines.append(current_line)
                for line in wrapped_lines:
                    c.drawString(x, y, line)
                    y -= line_height
                return y  # Devuelve la nueva coordenada Y

            # ======= LADO FRONTAL =======
            frente = ImageReader(frente_path)
            c.drawImage(frente, margin_x, margin_y, width=gafete_w, height=gafete_h)

            c.setFont("Helvetica-Bold", 8)
            y = text_y_start
            max_text_width = 90  # ancho máximo en puntos (~1.1 pulgadas)

            y = draw_wrapped_text(c, f"Nombre: {form.cleaned_data['nombre']}", text_x, y, max_text_width)
            y = draw_wrapped_text(c, f"Puesto: {form.cleaned_data['puesto']}", text_x, y - 2, max_text_width)
            y = draw_wrapped_text(c, f"Dirección: {form.cleaned_data['direccion']}", text_x, y - 2, max_text_width)
            y = draw_wrapped_text(c, f"NSS: {form.cleaned_data['nss']}", text_x, y - 2, max_text_width)
            y = draw_wrapped_text(c, f"Tel: {form.cleaned_data['tel']}", text_x, y - 2, max_text_width)
            y = draw_wrapped_text(c, f"Emergencia: {form.cleaned_data['tel_emg']}", text_x, y - 2, max_text_width)

            # ======= FOTO =======
            if form.cleaned_data.get('foto'):
                uploaded_file = form.cleaned_data['foto']
                image_bytes = uploaded_file.read()
                image_io = BytesIO(image_bytes)
                foto = ImageReader(image_io)
                c.drawImage(foto, foto_x, foto_y, width=60, height=60)

            # ======= LADO TRASERO (derecha) =======
            reverso = ImageReader(reverso_path)
            c.drawImage(reverso, margin_x + gafete_w + gap, margin_y, width=gafete_w, height=gafete_h)

            # Guardar PDF
            c.save()
            buffer.seek(0)

            # Guardar empleado + PDF
            empleado = form.save()
            nombre_pdf = f'gafete de {empleado.nombre} {empresa}.pdf'
            empleado.gafete_pdf.save(nombre_pdf, buffer)
            empleado.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre_pdf}"'
            return response

    else:
        form = EmpleadoForm()

    return render(request, 'app_PDF_maker/gafetes.html', {'form': form})