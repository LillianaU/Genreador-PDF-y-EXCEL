# Sistema de Generación de PDF y Excel - Django + MySQL

## 📋 Descripción del Proyecto

Sistema web desarrollado en **Django** que permite gestionar usuarios y generar reportes en formato **PDF** y **Excel** con gráficos estadísticos profesionales (Barras, Torta, Dispersión) estilo Chart.js.

---

## 📊 Diagramas de Procesos

### C1 - Diagrama de Contexto

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           C1 - DIAGRAMA DE CONTEXTO                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────┐                    ┌─────────────────────┐                  │
│    │          │  1. Busca      ┌──►│                     │                  │
│    │  USUARIO │────────────────►│   │   SISTEMA DE        │                  │
│    │          │◄───────────────│   │   GESTIÓN           │                  │
│    └──────────┘  2. Resultados │   │   PDF/Excel         │                  │
│                              │   │                     │                  │
│    ┌──────────┐  3. Consulta  │   │  - Búsqueda ID      │                  │
│    │  MySQL   │◄───────────────►   │  - Búsqueda Nombre  │                  │
│    │  Server  │    4. Datos     │   │  - Generar PDF     │                  │
│    └──────────┘                │   │  - Generar Excel   │                  │
│                                └───────────────────────┘                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### C2 - Diagrama de Procesos

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        C2 - DIAGRAMA DE PROCESOS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. BÚSQUEDA DE USUARIO                                                   │
│   ┌──────────┬──────────┬──────────┐                                        │
│   │1.1 Por ID│1.2 Por  │1.3 Mostrar│                                       │
│   │          │Nombre   │Modal      │                                       │
│   └──────────┴──────────┴──────────┘                                        │
│          │              │           │                                        │
│          └──────────────┼───────────┘                                        │
│                         ▼                                                   │
│   2. GENERAR PDF                        3. GENERAR EXCEL                    │
│   ┌────────────────────────┐         ┌────────────────────────┐         │
│   │ 2.1 Datos Usuario       │         │ 3.1 Hoja Datos         │         │
│   │ 2.2 Gráfico Barras     │         │ 3.2 Hoja Estadísticas   │         │
│   │ 2.3 Gráfico Torta       │         │ 3.3 Gráficos Excel      │         │
│   │ 2.4 Gráfico Dispersión  │         │                        │         │
│   └────────────────────────┘         └────────────────────────┘         │
│                                                                             │
│   4. REPORTE GENERAL                                                       │
│   ┌─────────────────────────────────────┐                                 │
│   │ - PDF General con todos los datos   │                                 │
│   │ - Excel General con gráficos        │                                 │
│   └─────────────────────────────────────┘                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### C3 - Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        C3 - FLUJO DE DATOS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    INICIO                                                                  │
│       │                                                                     │
│       ▼                                                                     │
│  ┌──────────────┐                                                         │
│  │ Usuario      │ ──► Solicitud POST                                      │
│  │ envía datos  │                                                         │
│  └──────────────┘                                                         │
│       │                                                                     │
│       ▼                                                                     │
│  ┌──────────────┐     ¿Tipo de búsqueda?                                 │
│  │ View         │ ──► ┌──────────┐ ┌──────────┐                          │
│  │ (views.py)   │     │ Por ID   │ │ Por Nom  │                          │
│  └──────────────┘     └────┬─────┘ └────┬─────┘                          │
│       │                    │            │                                 │
│       ▼                    ▼            ▼                                 │
│  ┌────────────────────────────────────────────┐                          │
│  │           MySQL - Base de Datos             │                          │
│  │         SELECT * FROM usuarios             │                          │
│  └────────────────────────────────────────────┘                          │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                          │
│  │ Generar PDF │ │ Generar    │ │ Render     │                          │
│  │(ReportLab)  │ │ Excel      │ │ Template   │                          │
│  │             │ │(openpyxl)  │ │+ Modal     │                          │
│  └─────────────┘ └─────────────┘ └─────────────┘                          │
│       │               │             │                                      │
│       └───────────────┴─────────────┘                                      │
│                     ▼                                                      │
│                  FIN                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### C4 - Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       C4 - DIAGRAMA DE COMPONENTES                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    CAPA DE PRESENTACIÓN                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │index.html│  │lista.html│  │estilos.css│ │JavaScript│         │   │
│  │  │ (Menú)   │  │(Tabla)   │  │(Diseño)  │  │ (UI)     │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                       │
│                                    ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    CAPA DE LÓGICA (Django)                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │   │
│  │  │views.py │  │ urls.py  │  │settings │                            │   │
│  │  │Control  │  │  Rutas   │  │  Config │                            │   │
│  │  └──────────┘  └──────────┘  └──────────┘                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                       │
│          ┌─────────────────────────┼─────────────────────────┐           │
│          ▼                         ▼                         ▼           │
│  ┌──────────────┐  ┌──────────────────────┐  ┌──────────────┐          │
│  │ MySQL        │  │ PDF Service          │  │ Excel       │          │
│  │ (Datos)      │  │ (ReportLab)           │  │ Service     │          │
│  │              │  │ - Barras             │  │ (openpyxl)  │          │
│  │ Tabla:       │  │ - Torta              │  │ - Hojas     │          │
│  │ usuarios     │  │ - Dispersión          │  │ - Gráficos  │          │
│  └──────────────┘  └──────────────────────┘  └──────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Arquitectura y Patrones de Diseño

### Patrones Utilizados

| Patrón | Descripción | Ubicación |
|--------|-------------|-----------|
| **MVC** | Modelo-Vista-Controlador de Django | Proyecto completo |
| **Factory Method** | Creación de documentos PDF/Excel | `views.py` |
| **Repository** | Acceso a datos MySQL mediante cursor | `views.py` |
| **Service Layer** | Lógica de negocio encapsulada | Funciones de views |
| **Template Method** | Estructura de generación de documentos | `generar_pdf/excel` |

---

## 🚀 Tutorial: Cómo Codificar el Proyecto Paso a Paso

### Paso 1: Preparar el Entorno

```bash
# 1. Crear carpeta del proyecto
mkdir mi_proyecto
cd mi_proyecto

# 2. Crear entorno virtual
python -m venv ven
ven\Scripts\activate  # Windows

# 3. Instalar Django
pip install django==4.2.28

# 4. Crear proyecto Django
django-admin startproject mi_proyecto .
```

### Paso 2: Configurar MySQL

```python
# Editar mi_proyecto/mi_proyecto/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ejemplo',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'documentos' / 'static',
]
```

### Paso 3: Crear la Aplicación

```bash
# 1. Crear app documentos
python manage.py startapp documentos

# 2. Agregar a INSTALLED_APPS en settings.py
INSTALLED_APPS = [
    ...
    'documentos',
]

# 3. Crear estructura de carpetas
mkdir -p documentos/templates/documentos
mkdir -p documentos/static/css
mkdir -p documentos/static/js
mkdir -p documentos/static/fonts
mkdir -p documentos/static/images
```

### Paso 4: Crear las Vistas (views.py)

```python
# documentos/views.py

# 1. Importaciones necesarias
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# Para PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, String, Circle, Rect, Wedge
from reportlab.lib.colors import HexColor

# Para Excel
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference

# 2. Vista principal - Búsqueda
def index(request):
    usuario = None
    if request.method == 'POST':
        # Buscar por ID
        id_usuario = request.POST.get('id_usuario')
        if id_usuario:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
                columns = [col[0] for col in cursor.description]
                row = cursor.fetchone()
                if row:
                    usuario = dict(zip(columns, row))
                    return render(request, 'documentos/index.html', 
                                {'usuario': usuario, 'mostrar_modal': True})
        # Buscar por nombre...
    return render(request, 'documentos/index.html', {'usuario': usuario})

# 3. Generar PDF con gráficos
def generar_pdf(request, id_usuario):
    # Obtener datos del usuario
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        # Obtener estadísticas
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        
        # Obtener datos para gráficos
        cursor.execute("""SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, 
                          COUNT(*) as cantidad FROM usuarios GROUP BY mes""")
        usuarios_mes = cursor.fetchall()
        
        cursor.execute("""SELECT LEFT(nombre, 1) as inicial, COUNT(*) as cantidad 
                          FROM usuarios GROUP BY inicial""")
        usuarios_inicial = cursor.fetchall()
    
    if not row:
        return HttpResponse("Usuario no encontrado", status=404)
    
    usuario = dict(zip(columns, row))
    
    # Crear PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter, 
                            rightMargin=40, leftMargin=40, 
                            topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                alignment=1, fontSize=24)
    elements.append(Paragraph("INFORME DE USUARIO", title_style))
    
    # Tabla de datos
    data = [['Campo', 'Valor'], ['ID', str(usuario['id'])], 
            ['Nombre', usuario['nombre']], ['Correo', usuario['correo']]]
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    
    # GRÁFICO DE BARRAS
    drawing = Drawing(400, 200)
    # (código para crear gráfico de barras con ReportLab)
    elements.append(drawing)
    
    # GRÁFICO DE TORTA
    drawing_torta = Drawing(200, 200)
    # (código para crear gráfico de torta)
    elements.append(drawing_torta)
    
    doc.build(elements)
    return response

# 4. Generar Excel
def generar_excel(request, id_usuario):
    # Similar al PDF pero usando openpyxl
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos"
    
    # Agregar datos...
    
    # Agregar gráficos
    chart = BarChart()
    # Configurar gráfico...
    ws.add_chart(chart, "E3")
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.xlsx"'
    wb.save(response)
    return response
```

### Paso 5: Configurar URLs

```python
# documentos/urls.py

from django.urls import path
from .views import index, generar_pdf, generar_excel

urlpatterns = [
    path('', index, name='index'),
    path('generar_pdf/<int:id_usuario>/', generar_pdf, name='generar_pdf'),
    path('generar_excel/<int:id_usuario>/', generar_excel, name='generar_excel'),
]
```

```python
# mi_proyecto/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documentos.urls')),
]
```

### Paso 6: Crear Templates

```html
<!-- documentos/templates/documentos/index.html -->
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Gestión</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'css/sweetalert2.min.css' %}">
</head>
<body>
    <!-- Menú flotante -->
    <div class="floating-menu">
        <button onclick="toggleMenu()">☰</button>
        <!-- Acordeones -->
    </div>
    
    <!-- Contenido principal -->
    <div class="main-content">
        <!-- Búsqueda por ID -->
        <input type="number" id="buscarId" placeholder="ID">
        <button onclick="buscarUsuario()">Buscar</button>
    </div>
    
    <!-- Modal Bootstrap -->
    <div class="modal fade" id="usuarioModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">Resumen del Usuario</div>
                <div class="modal-body" id="modalContent"></div>
            </div>
        </div>
    </div>
    
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    <script src="{% static 'js/sweetalert2.min.js' %}"></script>
    <script>
        function buscarUsuario() {
            // Enviar formulario POST
        }
        
        function mostrarUsuario(usuario) {
            // Mostrar en modal
            document.getElementById('modalContent').innerHTML = 
                `<h4>${usuario.nombre}</h4><p>${usuario.correo}</p>`;
            new bootstrap.Modal(document.getElementById('usuarioModal')).show();
        }
    </script>
</body>
</html>
```

### Paso 7: Descargar Archivos Estáticos

```bash
# En la carpeta static/

# 1. Bootstrap CSS
curl -o css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css

# 2. Bootstrap JS
curl -o js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js

# 3. SweetAlert2
curl -o css/sweetalert2.min.css https://cdn.jsdelivr.net/npm/sweetalert2@11.10.8/dist/sweetalert2.min.css
curl -o js/sweetalert2.min.js https://cdn.jsdelivr.net/npm/sweetalert2@11.10.8/dist/sweetalert2.min.js
```

### Paso 8: Ejecutar y Probar

```bash
# 1. Verificar configuración
python manage.py check

# 2. Iniciar servidor
python manage.py runserver

# 3. Abrir navegador
# http://127.0.0.1:8000/
```

---

## 📋 Resumen de Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Este archivo |
| `Tutorial.md` | Tutorial detallado |
| `PatronesDeDiseno.md` | Documentación de patrones |
| `requirements.txt` | Dependencias Python |
| `diagramas/C1_Contexto.drawio` | Diagrama de contexto |
| `diagramas/C2_Procesos.drawio` | Diagrama de procesos |
| `diagramas/C3_Flujo.drawio` | Diagrama de flujo |
| `diagramas/C4_Componentes.drawio` | Diagrama de componentes |

---

## 📚 Documentación Adicional

- [Tutorial.md](Tutorial.md) - Tutorial completo paso a paso
- [PatronesDeDiseno.md](PatronesDeDiseno.md) - Explicación detallada de patrones

---

**Desarrollado con Django + MySQL + ReportLab + openpyxl**