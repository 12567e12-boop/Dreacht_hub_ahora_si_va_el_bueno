from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    foto = models.ImageField(blank=True, null=True)  
    puesto = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    nss = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=50, blank=True, null=True)
    tel_emg = models.CharField(max_length=50, blank=True, unique=False, null=True)
    gafete_pdf = models.FileField(upload_to="gafetes/", blank=True, null=True)
    fecha_alta = models.DateField(auto_now_add=True)
    fecha_baja = models.DateField(blank=True, null=True)   
    nomina = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.nombre  
    

class Nomina(models.Model):
    def __str__(self):
        return f"Nómina de {self.empleado.nombre} del {self.fecha_inicio} al {self.fecha_fin}"