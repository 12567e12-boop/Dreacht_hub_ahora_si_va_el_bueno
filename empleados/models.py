from django.db import models

#empleado
class Empleado(models.Model):
    id_empleado = models.AutoField(             primary_key=True, editable=False, unique=True,db_index=True)
    nombre = models.CharField(                  max_length=50)
    foto = models.ImageField(                   )  
    puesto = models.CharField(                  max_length=50)
    direccion = models.CharField(               max_length=200, blank=True)
    nss = models.CharField(                     max_length=50, blank=True)
    tel = models.CharField(                     max_length=50, blank=True)
    tel_emg = models.CharField(                 max_length=50, blank=True)
    gafete_pdf = models.FileField(              upload_to="gafetes/")
    fecha_alta = models.DateField(              auto_now_add=True)
    fecha_baja = models.DateField(              blank=True, null=True)   
    id_nomina = models.OneToOneField(          'Nomina', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.nombre  
    
#nominas
class Nomina(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"Nómina {self.fecha}"
    
#requisiciones
import uuid
from django.db import models


class Requisicion(models.Model):
    id_requisicion = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    obra = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    numero_de_articulos = models.PositiveIntegerField(default=0, editable=False)
    fecha_solicitud = models.DateField()
    fecha_a_utilizar = models.DateField()
    fecha_de_surtido = models.DateField(null=True, blank=True)
    hora_y_fecha_impresion = models.DateTimeField(auto_now_add=True)
    contratista_que_solicita = models.CharField(max_length=255)
    quien_autoriza = models.CharField(max_length=255)
    area_donde_se_utilizara = models.CharField(max_length=255)
    hoja_numero = models.PositiveIntegerField(default=1, editable=False)
    hoja_total = models.PositiveIntegerField(default=1, editable=False)
    materiales = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Requisición"
        verbose_name_plural = "Requisiciones"
        ordering = ["-hora_y_fecha_impresion"]

    def __str__(self):
        return f"Requisición {self.id_requisicion} - {self.obra}"

    def actualizar_numero_de_articulos(self):
        """Actualiza automáticamente el número de artículos al guardar."""
        self.numero_de_articulos = self.detalles.count()
        self.save(update_fields=["numero_de_articulos"])


class DetalleRequisicion(models.Model):
    requisicion = models.ForeignKey(
        Requisicion,
        related_name="detalles",
        on_delete=models.CASCADE
    )
    material_no = models.PositiveIntegerField(editable=False)
    descripcion = models.CharField(max_length=255)
    unidad = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Detalle de requisición"
        verbose_name_plural = "Detalles de requisición"
        ordering = ["material_no"]

    def save(self, *args, **kwargs):
        """Asigna automáticamente el número de material y actualiza el total de artículos."""
        if not self.material_no:
            last = (
                DetalleRequisicion.objects.filter(requisicion=self.requisicion)
                .aggregate(models.Max("material_no"))
                .get("material_no__max")
            )
            self.material_no = (last or 0) + 1

        super().save(*args, **kwargs)

        # Actualizar contador en la requisición principal
        self.requisicion.actualizar_numero_de_articulos()

    def __str__(self):
        return f"Material {self.material_no}: {self.descripcion}"
