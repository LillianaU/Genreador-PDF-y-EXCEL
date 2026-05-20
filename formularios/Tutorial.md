# Tutorial Completo - Sistema de Generación de PDF y Excel

## 📊 Diagramas del Proyecto

### C1 - Diagrama de Contexto

```
┌────────────────────────────────────────┐
│         C1 - CONTEXTO                  │
├────────────────────────────────────────┤
│                                        │
│  Usuario ──► Sistema ──► MySQL         │
│     ▲              │                   │
│     │              ▼                   │
│     │        PDF / Excel               │
│     │              │                   │
│     └──────────────┘                   │
│        Resultados                      │
└────────────────────────────────────────┘
```

### C2 - Diagrama de Procesos

```
┌────────────────────────────────────────┐
│         C2 - PROCESOS                 │
├────────────────────────────────────────┤
│                                        │
│  [Búsqueda] [PDF] [Excel] [General]   │
│      │        │       │        │      │
│      ▼        ▼       ▼        ▼      │
│   MySQL    ReportLab  openpyxl   Todo  │
└────────────────────────────────────────┘
```

### C3 - Flujo de Datos

```
┌────────────────────────────────────────┐
│         C3 - FLUJO                     │
├────────────────────────────────────────┤
│                                        │
│ INICIO → POST → View → MySQL          │
│    │              │         │          │
│    │    ┌────────┴────────┐│          │
│    │    ▼               ▼           │
│    │  PDF            Excel           │
│    │    │               │           │
│    └────┴───────────────┘           │
│              │                       │
│             FIN                       │
└────────────────────────────────────────┘
```

### C4 - Componentes

```
┌────────────────────────────────────────┐
│       C4 - COMPONENTES               │
├────────────────────────────────────────┤
│                                        │
│ PRESENTACIÓN:  HTML + CSS + JS        │
│      │                                 │
│ LÓGICA:      Django Views + URLs     │
│      │                                 │
│ SERVICIOS:    PDF (ReportLab)        │
│              Excel (openpyxl)          │
│      │                                 │
│ DATOS:       MySQL                     │
└────────────────────────────────────────┘
```

---

## 1. Requisitos Previos

### Software Necesario
- Python 3.12+
- MySQL 8.0+
- pip

### Dependencias a Instalar
```
Django==4.2.28
mysqlclient==2.2.4
reportlab==4.2.5
openpyxl==3.1.5
Pillow==10.4.0
```

---

## 2. PASO A PASO - Crear el Proyecto

### Paso 1: Crear carpeta del proyecto

```bash
# Crear carpeta principal
mkdir formularios
cd formularios
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv ven

# Activar entorno virtual (Windows)
ven\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source ven/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install django==4.2.28
pip install mysqlclient
pip install reportlab
pip install openpyxl
pip install Pillow
```

### Paso 4: Crear proyecto Django

```bash
# Dentro de la carpeta formularios/
django-admin startproject mi_proyecto .
```

### Paso 5: Crear app documentos

```bash
python manage.py startapp documentos
```

### Paso 6: Configurar settings.py

**Archivo:** `mi_proyecto/mi_proyecto/settings.py`

Agregar 'documentos' en INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'documentos',  # AGREGAR ESTA LÍNEA
]
```

Configurar base de datos MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ejemplo',
        'USER': 'root',
        'PASSWORD': 'tu_password_aqui',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Agregar STATICFILES_DIRS:

```python
import os

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'documentos', 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Paso 7: Configurar URLs principal

**Archivo:** `mi_proyecto/mi_proyecto/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documentos.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 3. Archivos a Crear/Editar

### 3.1 views.py
**Ruta:** `mi_proyecto/documentos/views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Wedge
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def index(request):
    usuario = None
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        if id_usuario:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
                columns = [col[0] for col in cursor.description]
                row = cursor.fetchone()
                if row:
                    usuario = dict(zip(columns, row))
                    return render(request, 'documentos/index.html', {'usuario': usuario, 'mostrar_modal': True})
        
        nombre = request.POST.get('nombre_busqueda')
        if nombre:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE nombre LIKE %s", [f'%{nombre}%'])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                usuarios = [dict(zip(columns, row)) for row in rows]
                return render(request, 'documentos/index.html', {'usuarios_encontrados': usuarios})
    
    return render(request, 'documentos/index.html', {'usuario': usuario})

def lista_usuarios(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios ORDER BY id")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        usuarios = [dict(zip(columns, row)) for row in rows]
    return render(request, 'documentos/lista.html', {'usuarios': usuarios})

def generar_pdf(request, id_usuario):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        cursor.execute("SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cnt FROM usuarios GROUP BY mes")
        datos_mes = cursor.fetchall()
        cursor.execute("SELECT LEFT(nombre, 1) as inicial, COUNT(*) as cnt FROM usuarios GROUP BY inicial")
        datos_inicial = cursor.fetchall()
    
    if not row:
        return HttpResponse("Usuario no encontrado", status=404)
    
    usuario = dict(zip(columns, row))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, fontSize=24)
    elements.append(Paragraph("INFORME DE USUARIO", title_style))
    
    data = [['Campo', 'Valor'], ['ID', str(usuario['id'])], ['Nombre', usuario['nombre']], ['Correo', usuario['correo']], ['Teléfono', usuario.get('telefono', 'N/A')]]
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("GRÁFICO DE BARRAS", ParagraphStyle('Section', fontSize=14)))
    drawing = Drawing(400, 200)
    max_val = max(cnt for _, cnt in datos_mes) if datos_mes else 1
    for i, (mes, cnt) in enumerate(datos_mes[:10]):
        bar_h = (cnt / max_val) * 120
        rect = Rect(50 + i*30, 30, 20, bar_h)
        rect.fillColor = HexColor('#3498db')
        drawing.add(rect)
    elements.append(drawing)
    
    elements.append(Paragraph("GRÁFICO DE TORTA", ParagraphStyle('Section', fontSize=14)))
    drawing_torta = Drawing(200, 200)
    total_inicial = sum(cnt for _, cnt in datos_inicial)
    angle = 0
    colores = ['#e74c3c', '#3498db', '#27ae60', '#f39c12']
    for i, (inicial, cnt) in enumerate(datos_inicial[:10]):
        if total_inicial > 0:
            span = (cnt / total_inicial) * 360
            wedge = Wedge(100, 100, 80, angle, angle + span - 1)
            wedge.fillColor = HexColor(colores[i % len(colores)])
            drawing_torta.add(wedge)
            angle += span
    elements.append(drawing_torta)
    
    doc.build(elements)
    return response

def generar_excel(request, id_usuario):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        cursor.execute("SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cnt FROM usuarios GROUP BY mes")
        datos_mes = cursor.fetchall()
    
    usuario = dict(zip(columns, row))
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos"
    data = [['Campo', 'Valor'], ['ID', str(usuario['id'])], ['Nombre', usuario['nombre']], ['Correo', usuario['correo']]]
    for row_idx, (campo, valor) in enumerate(data, 1):
        ws.cell(row=row_idx, column=1, value=campo)
        ws.cell(row=row_idx, column=2, value=valor)
    
    if datos_mes:
        ws_chart = wb.create_sheet("Gráfico")
        ws_chart['A1'] = 'Mes'
        ws_chart['B1'] = 'Cantidad'
        for i, (mes, cnt) in enumerate(datos_mes, 2):
            ws_chart.cell(row=i, column=1, value=mes)
            ws_chart.cell(row=i, column=2, value=cnt)
        chart = BarChart()
        data_ref = Reference(ws_chart, min_col=2, min_row=1, max_row=len(datos_mes)+1)
        cats_ref = Reference(ws_chart, min_col=1, min_row=2, max_row=len(datos_mes)+1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        ws_chart.add_chart(chart, "D3")
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.xlsx"'
    wb.save(response)
    return response

def generar_pdf_todos(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        usuarios = [dict(zip(columns, row)) for row in rows]
        cursor.execute("SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cnt FROM usuarios GROUP BY mes")
        datos_mes = cursor.fetchall()
        cursor.execute("SELECT LEFT(nombre, 1) as inicial, COUNT(*) as cnt FROM usuarios GROUP BY inicial")
        datos_inicial = cursor.fetchall()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios_general.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, fontSize=24)
    elements.append(Paragraph("INFORME GENERAL DE USUARIOS", title_style))
    elements.append(Spacer(1, 20))
    
    if usuarios:
        table_data = [['ID', 'Nombre', 'Correo', 'Teléfono']]
        for u in usuarios:
            table_data.append([str(u['id']), u['nombre'], u['correo'], u.get('telefono', 'N/A')])
        table = Table(table_data, colWidths=[0.5*inch, 2*inch, 2*inch, 1.5*inch])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('GRID', (0, 0), (-1, -1), 1, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("GRÁFICO DE BARRAS", ParagraphStyle('Section', fontSize=14)))
    drawing = Drawing(400, 200)
    max_val = max(cnt for _, cnt in datos_mes) if datos_mes else 1
    for i, (mes, cnt) in enumerate(datos_mes[:10]):
        bar_h = (cnt / max_val) * 120
        rect = Rect(50 + i*30, 30, 20, bar_h)
        rect.fillColor = HexColor('#3498db')
        drawing.add(rect)
    elements.append(drawing)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("GRÁFICO DE TORTA", ParagraphStyle('Section', fontSize=14)))
    drawing_torta = Drawing(200, 200)
    total_inicial = sum(cnt for _, cnt in datos_inicial)
    angle = 0
    colores = ['#e74c3c', '#3498db', '#27ae60', '#f39c12', '#9b59b6']
    for i, (inicial, cnt) in enumerate(datos_inicial[:10]):
        if total_inicial > 0:
            span = (cnt / total_inicial) * 360
            wedge = Wedge(100, 100, 80, angle, angle + span - 1)
            wedge.fillColor = HexColor(colores[i % len(colores)])
            drawing_torta.add(wedge)
            angle += span
    elements.append(drawing_torta)
    
    doc.build(elements)
    return response

def generar_excel_todos(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        usuarios = [dict(zip(columns, row)) for row in rows]
        cursor.execute("SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cnt FROM usuarios GROUP BY mes")
        datos_mes = cursor.fetchall()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Usuarios"
    ws.append(['ID', 'Nombre', 'Correo', 'Teléfono', 'Dirección', 'Fecha Creación'])
    for u in usuarios:
        ws.append([u['id'], u['nombre'], u['correo'], u.get('telefono', 'N/A'), u.get('direccion', 'N/A'), str(u.get('fecha_creacion', ''))])
    
    if datos_mes:
        ws_chart = wb.create_sheet("Gráfico")
        ws_chart['A1'] = 'Mes'
        ws_chart['B1'] = 'Cantidad'
        for i, (mes, cnt) in enumerate(datos_mes, 2):
            ws_chart.cell(row=i, column=1, value=mes)
            ws_chart.cell(row=i, column=2, value=cnt)
        chart = BarChart()
        data_ref = Reference(ws_chart, min_col=2, min_row=1, max_row=len(datos_mes)+1)
        cats_ref = Reference(ws_chart, min_col=1, min_row=2, max_row=len(datos_mes)+1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        ws_chart.add_chart(chart, "D3")
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="usuarios_general.xlsx"'
    wb.save(response)
    return response
```

### 3.2 urls.py
**Ruta:** `mi_proyecto/documentos/urls.py` (CREAR)

```python
from django.urls import path
from .views import index, lista_usuarios, generar_pdf, generar_excel, generar_pdf_todos, generar_excel_todos

urlpatterns = [
    path('', index, name='index'),
    path('lista/', lista_usuarios, name='lista_usuarios'),
    path('generar_pdf/<int:id_usuario>/', generar_pdf, name='generar_pdf'),
    path('generar_excel/<int:id_usuario>/', generar_excel, name='generar_excel'),
    path('generar_pdf_todos/', generar_pdf_todos, name='generar_pdf_todos'),
    path('generar_excel_todos/', generar_excel_todos, name='generar_excel_todos'),
]
```

### 3.3 index.html
**Ruta:** `mi_proyecto/documentos/templates/documentos/index.html` (CREAR)

Este archivo contiene el diseño SPA con menú flotante, paleta de colores cafés, y soporta logo.jpg.

### 3.4 lista.html
**Ruta:** `mi_proyecto/documentos/templates/documentos/lista.html` (CREAR)

Este archivo contiene el listado de usuarios con estética cafés y formularios centrados.

---

## 4. Archivos Estáticos

### 4.1 Descargar Bootstrap y SweetAlert2

Crear carpetas:
```
mi_proyecto/documentos/static/css/
mi_proyecto/documentos/static/js/
mi_proyecto/documentos/static/images/
```

**Bootstrap CSS:** Descargar de https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css
Guardar en: `static/css/bootstrap.min.css`

**Bootstrap JS:** Descargar de https://getbootstrap.com/docs/5.3/dist/js/bootstrap.bundle.min.js
Guardar en: `static/js/bootstrap.bundle.min.css`

**SweetAlert2:** Descargar de https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css y sweetalert2.min.js
Guardar en: `static/css/sweetalert2.min.css` y `static/js/sweetalert2.min.js`

### 4.2 Logo
**Ruta:** `mi_proyecto/documentos/static/images/logo.jpg`

Crear logo con extensión .jpg (soporta también .png, .jpeg)

---

## 5. Base de Datos MySQL

```sql
CREATE DATABASE ejemplo CHARACTER SET utf8mb4;
USE ejemplo;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nombre, correo, telefono, direccion) VALUES
('Juan Pérez', 'juan@email.com', '555-123-4567', 'Calle 123'),
('María García', 'maria@email.com', '555-987-6543', 'Avenida 456'),
('Carlos López', 'carlos@email.com', '555-456-7890', 'Boulevard 789');
```

---

## 6. Ejecutar el Proyecto

```bash
cd mi_proyecto
python manage.py runserver
```

**Navegador:** http://127.0.0.1:8000/

---

## 7. Paleta de Colores - Tema Cafés

| Color | Hex | Uso |
|-------|-----|-----|
| Café Oscuro | #4A3728 | Header, textos principales |
| Café Medio | #6B4423 | Botones, bordes |
| Café Claro | #8B6914 | Iconos, acentos |
| Café Dorado | #A67B5B | Fondos secundarios |
| Dorado Oscuro | #B8860B | Destacados, badges |
| Crema Claro | #FAF8F5 | Fondo principal |

---

## 📁 Estructura Final

```
formularios/
├── mi_proyecto/
│   ├── manage.py
│   ├── settings.py          ← Editar (DB, STATIC)
│   ├── urls.py             ← Editar (incluir documentos.urls)
│   └── __init__.py
├── documentos/
│   ├── views.py            ← CREAR (todas las vistas)
│   ├── urls.py            ← CREAR (rutas)
│   ├── apps.py
│   ├── models.py
│   ├── templates/
│   │   └── documentos/
│   │       ├── index.html  ← CREAR (menú flotante SPA)
│   │       └── lista.html  ← CREAR (listado centrado)
│   └── static/
│       ├── css/
│       │   ├── bootstrap.min.css
│       │   └── sweetalert2.min.css
│       ├── js/
│       │   ├── bootstrap.bundle.min.js
│       │   └── sweetalert2.min.js
│       └── images/
│           └── logo.jpg    ← CREAR (soporta jpg, png, jpeg)
├── requirements.txt
├── Tutorial.md
└── README.md
```

---

## Problemas Comunes

| Error | Solución |
|-------|----------|
| mysqlclient no instala | Instalar Visual C++ Build Tools |
| Static files not found | Verificar STATICFILES_DIRS en settings.py |
| Template not found | Verificar estructura templates/documentos/ |
| Port in use | Usar `python manage.py runserver 8080` |

---

**¡Listo para ejecutar!** 🎉