"""
======================================================
MODELO DE USUARIO - DJANGO ORM
======================================================

Este archivo define el modelo de datos para usuarios.
Utiliza migraciones de Django para gestionar la base de datos.

MIGRACIONES:
============
Para crear y aplicar migraciones:

1. Crear migraciones:
   python manage.py makemigrations documentos

2. Aplicar migraciones:
   python manage.py migrate

3. Ver estado de migraciones:
   python manage.py showmigrations

CONSULTAS ORM:
==============
- Usuario.objects.get(id=1)     → Obtener por ID
- Usuario.objects.all()         → Obtener todos
- Usuario.objects.filter(...)  → Filtrar resultados
- Usuario.objects.count()       → Contar registros
- Usuario.objects.create(...)   → Crear registro
"""

from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    """
    Modelo de Usuario para el sistema de gestión.
    
    Campos:
        - nombre: Nombre completo del usuario
        - correo: Correo electrónico único
        - telefono: Teléfono de contacto (opcional)
        - direccion: Dirección (opcional)
        - fecha_creacion: Fecha de registro automática
    
    Tabla en MySQL: usuarios
    """
    
    nombre = models.CharField(max_length=100, help_text="Nombre completo del usuario")
    correo = models.EmailField(unique=True, help_text="Correo electrónico único")
    telefono = models.CharField(max_length=20, blank=True, null=True, help_text="Teléfono de contacto")
    direccion = models.CharField(max_length=255, blank=True, null=True, help_text="Dirección completa")
    fecha_creacion = models.DateTimeField(default=timezone.now, help_text="Fecha de creación automática")
    
    class Meta:
        db_table = 'usuarios'
        ordering = ['-id']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.nombre
    
    def get_id(self):
        """Retorna el ID del usuario"""
        return self.id
    
    def get_nombre(self):
        """Retorna el nombre del usuario"""
        return self.nombre
    
    def get_correo(self):
        """Retorna el correo del usuario"""
        return self.correo
    
    def get_telefono(self):
        """Retorna el teléfono o 'N/A' si está vacío"""
        return self.telefono if self.telefono else "N/A"
    
    def get_direccion(self):
        """Retorna la dirección o 'N/A' si está vacío"""
        return self.direccion if self.direccion else "N/A"
    
    def get_fecha_creacion(self):
        """Retorna la fecha de creación en formato legible"""
        return self.fecha_creacion.strftime('%Y-%m-%d')