from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    """Modelo de Usuario para el sistema de gestión"""
    
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'usuarios'
        ordering = ['-id']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.nombre
    
    def get_id(self):
        return self.id
    
    def get_nombre(self):
        return self.nombre
    
    def get_correo(self):
        return self.correo
    
    def get_telefono(self):
        return self.telefono if self.telefono else "N/A"
    
    def get_direccion(self):
        return self.direccion if self.direccion else "N/A"
    
    def get_fecha_creacion(self):
        return self.fecha_creacion.strftime('%Y-%m-%d')