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

### Dependencias
```
Django==4.2.28
mysqlclient==2.2.4
reportlab==4.2.5
openpyxl==3.1.5
Pillow==10.4.0
```

---

## 2. Instalación Paso a Paso

### Paso 1: Entorno Virtual

```bash
# Crear proyecto
mkdir formularios
cd formularios

# Crear entorno virtual
python -m venv ven

# Activar (Windows)
ven\Scripts\activate

# Activar (Linux/Mac)
source ven/bin/activate
```

### Paso 2: Instalar Django

```bash
pip install django==4.2.28
pip install mysqlclient
pip install reportlab
pip install openpyxl
pip install Pillow
```

### Paso 3: Crear Proyecto

```bash
cd mi_proyecto
django-admin startproject mi_proyecto .
python manage.py startapp documentos
```

---

## 3. Configuración de Base de Datos

### MySQL - Crear Tabla

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

### Django - settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ejemplo',
        'USER': 'root',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATICFILES_DIRS = [
    BASE_DIR / 'documentos' / 'static',
]
```

---

## 4. Estructura de Archivos

```
formularios/
├── mi_proyecto/
│   ├── manage.py
│   ├── settings.py    ← Editar aquí
│   └── urls.py        ← Editar aquí
└── documentos/
    ├── views.py       ← CREAR código aquí
    ├── urls.py       ← CREAR aquí
    ├── templates/
    │   └── documentos/
    │       └── index.html  ← CREAR aquí
    └── static/
        ├── css/        ← Descargar Bootstrap
        ├── js/         ← Descargar Bootstrap
        ├── images/     ← Logo
        └── fonts/      ← Fuentes
```

---

## 5. Código Completo - views.py

### 5.1 Importaciones

```python
# Documentos/views.py

# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# PDF - ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, String, Circle, Rect, Wedge
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

# Excel - openpyxl
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
```

### 5.2 Vista index()

```python
def index(request):
    """Vista principal - Búsqueda de usuarios"""
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
        
        # Buscar por nombre
        nombre = request.POST.get('nombre_busqueda')
        if nombre:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE nombre LIKE %s", 
                            [f'%{nombre}%'])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                usuarios = [dict(zip(columns, row)) for row in rows]
                return render(request, 'documentos/index.html', 
                            {'usuarios_encontrados': usuarios})
    
    return render(request, 'documentos/index.html', {'usuario': usuario})
```

### 5.3 generar_pdf()

```python
def generar_pdf(request, id_usuario):
    """Genera PDF con gráficos estilo Chart.js"""
    
    with connection.cursor() as cursor:
        # Datos del usuario
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        # Estadísticas
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        
        # Gráficos
        cursor.execute("""SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, 
                          COUNT(*) as cnt FROM usuarios GROUP BY mes""")
        datos_mes = cursor.fetchall()
        
        cursor.execute("""SELECT LEFT(nombre, 1) as inicial, COUNT(*) as cnt 
                          FROM usuarios GROUP BY inicial""")
        datos_inicial = cursor.fetchall()
    
    if not row:
        return HttpResponse("Usuario no encontrado", status=404)
    
    usuario = dict(zip(columns, row))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter, 
                            rightMargin=40, leftMargin=40, 
                            topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], 
                                 alignment=1, fontSize=24)
    elements.append(Paragraph("INFORME DE USUARIO", title_style))
    
    # Tabla de datos
    data = [['Campo', 'Valor'], 
            ['ID', str(usuario['id'])],
            ['Nombre', usuario['nombre']],
            ['Correo', usuario['correo']],
            ['Teléfono', usuario.get('telefono', 'N/A')]]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # GRÁFICO DE BARRAS
    elements.append(Paragraph("GRÁFICO DE BARRAS", 
                ParagraphStyle('Section', fontSize=14, textColor=colors.blue)))
    
    drawing = Drawing(400, 200)
    max_val = max(cnt for _, cnt in datos_mes) if datos_mes else 1
    for i, (mes, cnt) in enumerate(datos_mes[:10]):
        bar_h = (cnt / max_val) * 120
        rect = Rect(50 + i*30, 30, 20, bar_h)
        rect.fillColor = HexColor('#3498db')
        drawing.add(rect)
    elements.append(drawing)
    
    # GRÁFICO DE TORTA
    elements.append(Paragraph("GRÁFICO DE TORTA", 
                ParagraphStyle('Section', fontSize=14, textColor=colors.blue)))
    
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
```

### 5.4 generar_excel()

```python
def generar_excel(request, id_usuario):
    """Genera Excel con gráficos interactivos"""
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        
        cursor.execute("""SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, 
                          COUNT(*) as cnt FROM usuarios GROUP BY mes""")
        datos_mes = cursor.fetchall()
    
    usuario = dict(zip(columns, row))
    
    wb = Workbook()
    
    # Hoja 1: Datos
    ws = wb.active
    ws.title = "Datos"
    
    data = [['Campo', 'Valor'], ['ID', str(usuario['id'])],
            ['Nombre', usuario['nombre']], ['Correo', usuario['correo']]]
    
    for row_idx, (campo, valor) in enumerate(data, 1):
        ws.cell(row=row_idx, column=1, value=campo)
        ws.cell(row=row_idx, column=2, value=valor)
    
    # Hoja 2: Gráfico
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
```

---

## 6. Rutas - urls.py

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

---

## 7. Template - index.html

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>Sistema de Gestión</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'css/sweetalert2.min.css' %}">
</head>
<body>
    <!-- Menú Flotante -->
    <div class="floating-menu">
        <button onclick="toggleMenu()">☰ Menú</button>
    </div>
    
    <!-- Contenido -->
    <div class="main-content">
        <h1>Sistema de Gestión</h1>
        
        <!-- Buscar por ID -->
        <input type="number" id="buscarId" placeholder="ID usuario">
        <button onclick="buscarUsuario()">Buscar</button>
        
        <!-- Buscar por Nombre -->
        <input type="text" id="buscarNombre" placeholder="Nombre">
        <button onclick="buscarPorNombre()">Buscar</button>
    </div>
    
    <!-- Modal -->
    <div class="modal" id="usuarioModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">Usuario</div>
                <div class="modal-body" id="modalContent"></div>
            </div>
        </div>
    </div>
    
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    <script src="{% static 'js/sweetalert2.min.js' %}"></script>
    <script>
        function buscarUsuario() {
            // POST con CSRF
            let form = document.createElement('form');
            form.method = 'POST';
            form.action = '{% url "index" %}';
            
            let csrf = document.createElement('input');
            csrf.name = 'csrfmiddlewaretoken';
            csrf.value = '{{ csrf_token }}';
            
            let id = document.createElement('input');
            id.name = 'id_usuario';
            id.value = document.getElementById('buscarId').value;
            
            form.append(csrf, id);
            document.body.append(form);
            form.submit();
        }
    </script>
</body>
</html>
```

---

## 8. Ejecutar el Proyecto

```bash
cd mi_proyecto
python manage.py runserver
```

Navegador: **http://127.0.0.1:8000/**

---

## 9. Problemas Comunes

| Error | Solución |
|-------|----------|
| mysqlclient no install | Instalar Visual C++ Build Tools |
| Static files not found | Verificar STATICFILES_DIRS |
| Template not found | Verificar estructura templates/ |
| Port in use | Usar `runserver 8080` |

---

## 📁 Archivos del Proyecto

- **README.md** - Descripción general
- **Tutorial.md** - Este tutorial
- **PatronesDeDiseno.md** - Patrones de diseño
- **requirements.txt** - Dependencias
- **diagramas/** - Diagramas C1-C4

---

**Listo para ejecutar** 🎉