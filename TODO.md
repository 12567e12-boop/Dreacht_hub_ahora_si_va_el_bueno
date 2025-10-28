# TODO: Arreglar formulario de requisiciones - Texto no visible en PDF

## Información Recopilada
- El formulario de requisiciones genera un PDF, pero el texto no aparece en los lugares correctos.
- El PDF base es 'requiscion_template.pdf', un PDF estático donde se dibuja texto encima usando ReportLab.
- En views.py, se crea un overlay con canvas.Canvas y se fusiona con el PDF base usando pypdf.
- Las coordenadas en el template HTML están definidas desde la parte superior (y=0 arriba), pero en views.py se invierten incorrectamente con height - y, causando que el texto se dibuje en posiciones equivocadas (cerca de abajo en lugar de arriba).

## Plan de Corrección
- Ajustar las coordenadas en views.py para usar y directamente (sin invertir), ya que las coordenadas del HTML están desde arriba.
- Remover el texto de debug en rojo para limpiar el PDF.
- Verificar que el merge del overlay funcione correctamente.

## Pasos a Seguir
- [x] Editar app_PDF_maker/views.py: Cambiar las coordenadas de drawString para usar y directamente en lugar de height - y.
- [x] Agregar debug temporal (texto rojo en la parte superior) para verificar que los datos se capturan correctamente.
- [ ] Probar el formulario generando un PDF y verificar que el texto aparezca en las posiciones correctas.
- [ ] Si aún no funciona, ajustar coordenadas manualmente basándose en el template PDF.

## Archivos Dependientes
- app_PDF_maker/views.py (principal)
- app_PDF_maker/templates/app_PDF_maker/requisiciones.html (para referencia de coordenadas)

## Seguimiento
- Después de editar, ejecutar el servidor y probar el formulario.
