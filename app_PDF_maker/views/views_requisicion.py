import os
from io import BytesIO
from datetime import datetime
import pytz

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

from empleados.models import Requisicion

# Función auxiliar para convertir string a date
def parse_fecha(fecha_str):
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def requisiciones(request):
    tz = pytz.timezone("America/Mexico_City")
    fecha_hora_creacion = datetime.now(tz)

    if request.method == "POST":
        # --- Recoger datos del formulario ---
        obra = request.POST.get('obra', '')
        ubicacion = request.POST.get('ubicacion', '')
        numero_de_articulos = request.POST.get('numero_de_articulos', '')

        fecha_soli = parse_fecha(request.POST.get('fecha_soli', ''))
        fecha_util = parse_fecha(request.POST.get('fecha_util', ''))
        fecha_surt = parse_fecha(request.POST.get('fecha_surt', ''))

        contratista_soli = request.POST.get('contratista_soli', '')
        contratista_auto = request.POST.get('contratista_auto', '')
        area_util = request.POST.get('area_util', '')
        observaciones = request.POST.get('observaciones', '')



        try:
            # --- Buscar o crear la requisición ---
            requisicion, creada = Requisicion.objects.get_or_create(
                obra=obra,
                ubicacion=ubicacion,
                contratista_soli=contratista_soli,
                contratista_auto=contratista_auto,
                defaults={
                    "numero_de_articulos": int(numero_de_articulos) if numero_de_articulos else 0,
                    "fecha_soli": fecha_soli,
                    "fecha_util": fecha_util,
                    "fecha_surt": fecha_surt,
                    "area_util": area_util,
                    "observaciones": observaciones,
                }
            )

            # --- Registrar fecha/hora de primera impresión ---
            if not requisicion.fecha_hora_creacion:
                requisicion.fecha_hora_creacion = fecha_hora_creacion
                requisicion.save(update_fields=["fecha_hora_creacion"])

            # --- Crear detalles de requisición ---
            from empleados.models import DetalleRequisicion
            for i in range(1, 15):  # 14 items
                descripcion = request.POST.get(f'item{i}_descripcion', '').strip()
                unidad = request.POST.get(f'item{i}_unidad', '').strip()
                cantidad_str = request.POST.get(f'item{i}_cantidad', '').strip()

                if descripcion:  # Solo crear si hay descripción
                    try:
                        cantidad = float(cantidad_str) if cantidad_str else 0.0
                        DetalleRequisicion.objects.create(
                            requisicion=requisicion,
                            descripcion=descripcion,
                            unidad=unidad,
                            cantidad=cantidad
                        )
                    except ValueError:
                        pass  # Ignorar si cantidad no es válida

            # --- Obtener detalles para mostrar en PDF ---
            detalles = DetalleRequisicion.objects.filter(requisicion=requisicion)

            # Dividir fecha y hora en strings
            fecha_str = requisicion.fecha_hora_creacion.strftime("%d/%m/%Y")
            hora_str = requisicion.fecha_hora_creacion.strftime("%H:%M")

            # --- Ruta de la plantilla PDF ---
            base_pdf_path = os.path.join(
                settings.BASE_DIR,
                'app_PDF_maker', 'static', 'media', 'requiscion_template.pdf'
            )
            if not os.path.exists(base_pdf_path):
                return HttpResponse(f"Error: plantilla base no encontrada en {base_pdf_path}", status=500)

            # --- Leer PDF base ---
            base_reader = PdfReader(base_pdf_path)
            base_page = base_reader.pages[0]
            page_width = float(base_page.mediabox.width)
            page_height = float(base_page.mediabox.height)

            # --- Crear overlay ---
            overlay_buffer = BytesIO()
            c = canvas.Canvas(overlay_buffer, pagesize=(page_width, page_height))

            # --- Campos a dibujar en PDF ---
            campos = {
                'obra':               (430, 1009, str(obra)),
                'ubicacion':          (470, 974, str(ubicacion)),
                'numero_de_articulos':(558, 936, str(numero_de_articulos or 0)),
                'fecha_soli':         (1250, 1009, fecha_soli.strftime("%Y-%m-%d") if fecha_soli else ""),
                'fecha_util':         (1250, 974, fecha_util.strftime("%Y-%m-%d") if fecha_util else ""),
                'fecha_surt':         (1250, 936, fecha_surt.strftime("%Y-%m-%d") if fecha_surt else ""),
                'contratista_soli':   (420, 885, str(contratista_soli)),
                'contratista_auto':   (275, 843, str(contratista_auto)),
                'area_util':          (400, 797, str(area_util)),
                'observaciones':      (50, 936, str(observaciones)),
                'fecha_creacion':     (1250, 875, fecha_str),  # solo fecha
                'hora_creacion':      (1250, 850, hora_str),   # solo hora
            }

            # --- Agregar campos de detalles ---
            y_start = 450
            for i, detalle in enumerate(detalles, start=1):
                y_pos = page_height - y_start - (i - 1) * 20
                campos[f'item{i}_descripcion'] = (50, y_pos, detalle.descripcion)
                campos[f'item{i}_unidad'] = (200, y_pos, detalle.unidad)
                campos[f'item{i}_cantidad'] = (250, y_pos, str(detalle.cantidad))

            # --- Dibujar texto ---
            c.setFont("Helvetica", 18)
            for x, y, text in campos.values():
                if text:
                    c.drawString(x, y, str(text))

            c.showPage()
            c.save()
            overlay_buffer.seek(0)

            # --- Combinar overlay con PDF base ---
            overlay_pdf = PdfReader(overlay_buffer)
            overlay_page = overlay_pdf.pages[0]

            writer = PdfWriter()
            base_page.merge_page(overlay_page)
            writer.add_page(base_page)

            # --- Generar PDF final ---
            final_buffer = BytesIO()
            writer.write(final_buffer)
            final_buffer.seek(0)

            response = HttpResponse(final_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="requisicion_completada.pdf"'
            return response

        except Exception as e:
            return HttpResponse(f"Error generando PDF: {str(e)}", status=500)

    # --- GET request: precargar formulario ---
    fecha_str = fecha_hora_creacion.strftime("%d/%m/%Y")
    hora_str = fecha_hora_creacion.strftime("%H:%M")
    return render(request, 'app_PDF_maker/requisiciones.html', {
        "fecha_creacion": fecha_str,
        "hora_creacion": hora_str
    })
