"""
======================================================
PRUEBAS DEL SISTEMA - DJANGO ORM + MySQL
======================================================

Este archivo contiene pruebas para verificar el correcto
funcionamiento del sistema de gestión de usuarios.

EJECUTAR PRUEBAS:
=================
python manage.py test documentos.test

O directamente con Python:
python documentos/test.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse

from .models import Usuario
from .views import index, generar_pdf, generar_excel


class PruebasModeloUsuario(TestCase):
    """Pruebas para el modelo de Usuario"""
    
    def setUp(self):
        """Crear usuario de prueba"""
        self.usuario = Usuario.objects.create(
            nombre='Juan Pérez',
            correo='juan@email.com',
            telefono='555-123-4567',
            direccion='Calle 123'
        )
    
    def test_crear_usuario(self):
        """Verificar que se crea correctamente"""
        self.assertEqual(self.usuario.nombre, 'Juan Pérez')
        self.assertEqual(self.usuario.correo, 'juan@email.com')
        self.assertEqual(self.usuario.telefono, '555-123-4567')
    
    def test_str_usuario(self):
        """Verificar representación string"""
        self.assertEqual(str(self.usuario), 'Juan Pérez')
    
    def test_get_telefono(self):
        """Verificar método get_telefono"""
        self.assertEqual(self.usuario.get_telefono(), '555-123-4567')
    
    def test_get_telefono_vacio(self):
        """Verificar método con teléfono vacío"""
        usuario = Usuario.objects.create(correo='test@test.com')
        self.assertEqual(usuario.get_telefono(), 'N/A')
    
    def test_get_direccion_vacio(self):
        """Verificar método con dirección vacía"""
        usuario = Usuario.objects.create(correo='test2@test.com')
        self.assertEqual(usuario.get_direccion(), 'N/A')
    
    def test_fecha_creacion_auto(self):
        """Verificar que fecha se asigna automáticamente"""
        self.assertIsNotNone(self.usuario.fecha_creacion)
    
    def test_correo_unico(self):
        """Verificar que el correo es único"""
        with self.assertRaises(Exception):
            Usuario.objects.create(nombre='Otro', correo='juan@email.com')


class PruebasVistas(TestCase):
    """Pruebas para las vistas del sistema"""
    
    def setUp(self):
        """Crear datos de prueba"""
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre='María García',
            correo='maria@email.com',
            telefono='555-987-6543'
        )
    
    def test_index_get(self):
        """Probar página principal con GET"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_post_buscar_id(self):
        """Probar búsqueda por ID"""
        response = self.client.post(reverse('index'), {
            'id_usuario': str(self.usuario.id)
        })
        self.assertEqual(response.status_code, 200)
    
    def test_index_post_buscar_nombre(self):
        """Probar búsqueda por nombre"""
        response = self.client.post(reverse('index'), {
            'nombre_busqueda': 'María'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_index_usuario_no_encontrado(self):
        """Probar búsqueda con ID inexistente"""
        response = self.client.post(reverse('index'), {
            'id_usuario': '9999'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
    
    def test_lista_usuarios(self):
        """Probar vista de lista"""
        response = self.client.get(reverse('lista_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('usuarios', response.context)


class PruebasGeneracionPDF(TestCase):
    """Pruebas para generación de PDF"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre='Carlos López',
            correo='carlos@email.com'
        )
    
    def test_generar_pdf_existe(self):
        """Verificar que la función existe"""
        self.assertTrue(callable(generar_pdf))
    
    def test_generar_pdf_ruta(self):
        """Probar ruta de generación PDF"""
        url = reverse('generar_pdf', args=[self.usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_generar_pdf_no_existe(self):
        """Probar PDF con usuario inexistente"""
        url = reverse('generar_pdf', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PruebasGeneracionExcel(TestCase):
    """Pruebas para generación de Excel"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre='Ana Rodríguez',
            correo='ana@email.com'
        )
    
    def test_generar_excel_ruta(self):
        """Probar ruta de generación Excel"""
        url = reverse('generar_excel', args=[self.usuario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    def test_generar_excel_no_existe(self):
        """Probar Excel con usuario inexistente"""
        url = reverse('generar_excel', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PruebasReportesGenerales(TestCase):
    """Pruebas para reportes generales"""
    
    def setUp(self):
        Usuario.objects.create(nombre='Usuario 1', correo='u1@test.com')
        Usuario.objects.create(nombre='Usuario 2', correo='u2@test.com')
    
    def test_pdf_todos(self):
        """Probar PDF de todos los usuarios"""
        response = self.client.get(reverse('generar_pdf_todos'))
        self.assertEqual(response.status_code, 200)
    
    def test_excel_todos(self):
        """Probar Excel de todos los usuarios"""
        response = self.client.get(reverse('generar_excel_todos'))
        self.assertEqual(response.status_code, 200)


class PruebasConsultasORM(TestCase):
    """Pruebas específicas de consultas ORM"""
    
    def setUp(self):
        Usuario.objects.create(nombre='Usuario A', correo='a@test.com')
        Usuario.objects.create(nombre='Usuario B', correo='b@test.com')
        Usuario.objects.create(nombre='Usuario C', correo='c@test.com')
    
    def test_count(self):
        """Probar count()"""
        self.assertEqual(Usuario.objects.count(), 3)
    
    def test_filter_icontains(self):
        """Probar búsqueda con icontains"""
        resultados = Usuario.objects.filter(nombre__icontains='Usuario')
        self.assertEqual(resultados.count(), 3)
    
    def test_filter_exacto(self):
        """Probar filtro exacto"""
        usuario = Usuario.objects.get(correo='a@test.com')
        self.assertEqual(usuario.nombre, 'Usuario A')
    
    def test_order_by(self):
        """Probar ordenamiento"""
        usuarios = Usuario.objects.all().order_by('nombre')
        self.assertEqual(usuarios[0].nombre, 'Usuario A')


# ==================================================
# EJECUCIÓN DIRECTA (sin pytest)
# ==================================================

def ejecutar_pruebas():
    """Ejecutar pruebas manualmente"""
    print("=" * 50)
    print("EJECUTANDO PRUEBAS DEL SISTEMA")
    print("=" * 50)
    
    # Crear datos de prueba
    print("\n1. Creando usuario de prueba...")
    usuario = Usuario.objects.create(
        nombre='Test Usuario',
        correo='test@email.com',
        telefono='555-000-0000',
        direccion='Test Dirección'
    )
    print(f"   ✓ Usuario creado: {usuario.nombre} (ID: {usuario.id})")
    
    # Probar modelo
    print("\n2. Probando modelo...")
    assert usuario.nombre == 'Test Usuario'
    assert usuario.get_telefono() == '555-000-0000'
    assert usuario.get_direccion() == 'Test Dirección'
    print("   ✓ Modelo funciona correctamente")
    
    # Probar consultas
    print("\n3. Probando consultas ORM...")
    total = Usuario.objects.count()
    assert total >= 1
    print(f"   ✓ Total usuarios: {total}")
    
    usuario_buscar = Usuario.objects.filter(nombre__icontains='Test')
    assert usuario_buscar.count() >= 1
    print(f"   ✓ Búsqueda por nombre: {usuario_buscar.count()} resultados")
    
    # Probar Client
    print("\n4. Probando vistas con Client...")
    client = Client()
    
    response = client.get(reverse('index'))
    assert response.status_code == 200
    print("   ✓ Página principal funciona")
    
    # Probar búsqueda POST
    response = client.post(reverse('index'), {'id_usuario': str(usuario.id)})
    assert response.status_code == 200
    print("   ✓ Búsqueda por ID funciona")
    
    # Probar PDF
    response = client.get(reverse('generar_pdf', args=[usuario.id]))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'
    print("   ✓ Generación PDF funciona")
    
    # Probar Excel
    response = client.get(reverse('generar_excel', args=[usuario.id]))
    assert response.status_code == 200
    assert 'spreadsheet' in response['Content-Type']
    print("   ✓ Generación Excel funciona")
    
    # Probar lista
    response = client.get(reverse('lista_usuarios'))
    assert response.status_code == 200
    print("   ✓ Página de lista funciona")
    
    # Limpiar
    print("\n5. Limpiando datos de prueba...")
    usuario.delete()
    print("   ✓ Datos eliminados")
    
    print("\n" + "=" * 50)
    print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 50)


if __name__ == '__main__':
    ejecutar_pruebas()