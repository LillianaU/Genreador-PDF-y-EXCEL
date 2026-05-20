# Documentación de Patrones de Diseño

## Sistema de Generación de PDF y Excel - Django ORM + MySQL

---

## 1. Introducción

Este documento describe los patrones de diseño utilizados en el proyecto, implementados en **Python/Django ORM** para la generación de informes PDF y Excel con gráficos estadísticos.

---

## 2. Patrones de Arquitectura

### 2.1 MVC (Model-View-Controller)

**Descripción**: Patrón implementado por Django naturalmente con Django ORM.

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA MVC                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   MODEL (Model)              VIEW (Template)                │
│   ┌─────────────┐            ┌─────────────────┐          │
│   │  models.py  │            │    HTML/CSS     │          │
│   │  Usuario    │            │   Bootstrap     │          │
│   └─────────────┘            └─────────────────┘          │
│         ↑                          ↑                       │
│         │    Usuario.objects       │  render()           │
│         └──────────────────────────┘                       │
│                          ↓                                  │
│                   CONTROLLER                              │
│                   ┌─────────────┐                          │
│                   │   views.py  │                          │
│                   │  funciones  │                          │
│                   └─────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Implementación con Django ORM**:
```python
# MODEL - models.py
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

# CONTROLADOR - Acceso a datos con ORM
usuario = Usuario.objects.get(id=id_usuario)
usuarios = Usuario.objects.filter(nombre__icontains=nombre)

# VIEW - Renderizado de plantillas
return render(request, 'documentos/index.html', {'usuario': usuario})
```

---

### 2.2 Factory Method (Patrón Fábrica)

**Descripción**: Encapsula la creación de objetos PDF/Excel sin especificar clases concretas.

```
┌─────────────────────────────────────────────┐
│            FACTORY METHOD                   │
├─────────────────────────────────────────────┤
│                                             │
│   generar_pdf() ─────────────────────────►  │
│       │                                      │
│       ├── Crea SimpleDocTemplate           │
│       ├── Configura estilos                 │
│       ├── Genera tablas                     │
│       ├── Genera gráficos (Barras,Torta)   │
│       └── Retorna HttpResponse              │
│                                             │
│   generar_excel() ─────────────────────────► │
│       │                                      │
│       ├── Crea Workbook                     │
│       ├── Crea hojas múltiples               │
│       ├── Genera gráficos interactivos      │
│       └── Retorna HttpResponse              │
│                                             │
└─────────────────────────────────────────────┘
```

**Implementación en views.py**:
```python
def generar_pdf(request, id_usuario):
    """FÁBRICA de documentos PDF"""
    response = HttpResponse(content_type='application/pdf')
    doc = SimpleDocTemplate(response, pagesize=letter, ...)
    elements = []
    # Agregar logo, estilos, datos, gráficos...
    doc.build(elements)
    return response

def generar_excel(request, id_usuario):
    """FÁBRICA de documentos Excel"""
    wb = Workbook()
    ws = wb.active
    # Agregar datos, hojas, gráficos...
    wb.save(response)
    return response
```

---

### 2.3 Repository Pattern (Patrón Repositorio)

**Descripción**: Abstrae el acceso a datos mediante Django ORM.

```
┌─────────────────────────────────────────────┐
│           REPOSITORY PATTERN (Django ORM)   │
├─────────────────────────────────────────────┤
│                                             │
│   View ──────► ORM ──────► MySQL           │
│                     │                       │
│         ┌──────────┼──────────┐            │
│         │          │          │            │
│    .get()   .filter()  .count()           │
│                                             │
└─────────────────────────────────────────────┘
```

**Implementación con Django ORM**:
```python
# Django ORM como Repository
from documentos.models import Usuario

# get_by_id()
usuario = Usuario.objects.get(id=id_usuario)

# get_all()
usuarios = Usuario.objects.all()

# get_stats()
total = Usuario.objects.count()

# filter() con condiciones
usuarios = Usuario.objects.filter(nombre__icontains='Juan')
```

---

### 2.4 Service Layer (Patrón de Servicio)

**Descripción**: Lógica de negocio encapsulada en servicios independientes.

```
┌─────────────────────────────────────────────┐
│           SERVICE LAYER                     │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ PDFService │  │ExcelService │          │
│  ├─────────────┤  ├─────────────┤          │
│  │ +generar() │  │ +generar()  │          │
│  │ +agregar() │  │ +agregar()  │          │
│  │ +graficos() │  │ +graficos() │          │
│  └─────────────┘  └─────────────┘          │
│       │                 │                   │
│       └────────┬────────┘                    │
│                ▼                             │
│         HttpResponse                         │
│                                             │
└─────────────────────────────────────────────┘
```

**Implementación en views.py**:
```python
class PDFService:
    """Servicio de generación de PDF"""
    
    @staticmethod
    def generar(usuario_id):
        # 1. Obtener datos
        usuario = obtener_usuario(usuario_id)
        estadisticas = obtener_estadisticas()
        
        # 2. Crear documento
        doc = SimpleDocTemplate(...)
        
        # 3. Agregar contenido
        elements = []
        elements.append(Paragraph("INFORME", title_style))
        elements.append(crear_tabla_datos(usuario))
        elements.append(crear_grafico_barras(estadisticas))
        elements.append(crear_grafico_torta(estadisticas))
        
        # 4. Retornar
        doc.build(elements)
        return response

class ExcelService:
    """Servicio de generación de Excel"""
    
    @staticmethod
    def generar(usuario_id):
        # Similar al servicio PDF
        pass
```

---

### 2.5 Template Method (Patrón Método Plantilla)

**Descripción**: Define el esqueleto de un algoritmo, delegando pasos específicos a subclases.

```
┌─────────────────────────────────────────────┐
│          TEMPLATE METHOD                    │
├─────────────────────────────────────────────┤
│                                             │
│   generar_documento()                       │
│   ┌────────────────────────────────────┐    │
│   │ 1. preparar_estilos()      ──────┼────│► inheritance implícita en Python
│   │ 2. agregar_encabezado()           │    │
│   │ 3. agregar_contenido()            │    │
│   │ 4. agregar_graficos()             │    │
│   │ 5. agregar_pie()                  │    │
│   │ 6. construir()                    │    │
│   └────────────────────────────────────┘    │
│                                             │
│   PDF: usa ReportLab (SimpleDocTemplate)    │
│   Excel: usa openpyxl (Workbook)            │
│                                             │
└─────────────────────────────────────────────┘
```

**Implementación**:
```python
def generar_pdf(request, id_usuario):
    """MÉTODO PLANTILLA para PDF"""
    
    # 1. Preparar estilos (Step 1)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(...)
    
    # 2. Agregar encabezado (Step 2)
    elements.append(Paragraph("INFORME", title_style))
    
    # 3. Agregar contenido (Step 3)
    data = [['Campo', 'Valor'], ['ID', str(usuario['id'])]]
    table = Table(data)
    
    # 4. Agregar gráficos (Step 4)
    elements.append(crear_grafico_barras())
    elements.append(crear_grafico_torta())
    elements.append(crear_grafico_dispersion())
    
    # 5. Agregar pie (Step 5)
    elements.append(Paragraph("Sistema Django + MySQL", footer_style))
    
    # 6. Construir (Step 6)
    doc.build(elements)
    return response
```

---

## 3. Diagrama de Flujo de Datos

```
USUARIO → PETICIÓN HTTP → VIEW (Controller)
                              │
                              ├─► Repository (MySQL)
                              │       │
                              │       └─► TABLA usuarios
                              │
                              ├─► Service Layer
                              │       │
                              │       ├─► PDF Service
                              │       │       └─► ReportLab (PDF)
                              │       │
                              │       └─► Excel Service
                              │               └─► openpyxl (Excel)
                              │
                              └─► VIEW (Template)
                                      └─► HTML + Bootstrap
```

---

## 4. Resumen de Patrones

| Patrón | Ubicación | Descripción |
|--------|-----------|-------------|
| **MVC** | Django completo | Arquitectura del framework |
| **Factory Method** | `generar_pdf()`, `generar_excel()` | Creación de documentos |
| **Repository** | `connection.cursor()` | Acceso a datos MySQL |
| **Service Layer** | Funciones de views | Lógica de negocio |
| **Template Method** | `generar_pdf()`, `generar_excel()` | Estructura de generación |

---

## 5. Beneficios de los Patrones

1. **Mantenibilidad**: Código organizado y separable
2. **Reutilización**: Funciones genéricas reutilizables
3. **Testabilidad**: Fácil de probar cada componente
4. **Flexibilidad**: Fácil agregar nuevos formatos
5. **Claridad**: Estructura clara y documentada

---

## 6. Tecnologías que Implementan los Patrones

| Tecnología | Patrón Principal |
|------------|------------------|
| **Django** | MVC, Service Layer |
| **ReportLab** | Factory Method, Template Method |
| **openpyxl** | Factory Method, Template Method |
| **Bootstrap** | SPA Pattern |
| **SweetAlert2** | Observer Pattern |

---

## 7. Conclusión

Este proyecto demuestra la aplicación práctica de múltiples patrones de diseño en un sistema real de generación de informes, utilizando:

- **Python/Django** para el backend
- **MySQL** para datos
- **ReportLab** para PDF con gráficos
- **openpyxl** para Excel con gráficos interactivos
- **Bootstrap** para interfaz moderna

Los patrones de diseño permiten un código mantenible, escalable y testeable.