# Documentación de Patrones de Diseño

## Sistema de Generación de PDF y Excel - Django + MySQL

---

## 1. Patrones de Arquitectura

### 1.1 MVC (Model-View-Controller)

Django implementa el patrón MVC de forma natural:

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA MVC                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   MODEL (Model)              VIEW (Template)                │
│   ┌─────────────┐            ┌─────────────────┐          │
│   │   MySQL     │            │    HTML/CSS     │          │
│   │  usuarios   │            │   Bootstrap     │          │
│   └─────────────┘            └─────────────────┘          │
│         ↑                          ↑                       │
│         │    connection.cursor()   │  render()             │
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

**Implementación en el código:**

```python
# MODEL - Acceso a datos MySQL
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])

# VIEW - Renderizado de plantillas
return render(request, 'documentos/index.html', {'usuario': usuario})

# CONTROLLER - Lógica de negocio
def generar_pdf(request, id_usuario):
    # Procesamiento y generación de PDF
```

---

### 1.2 Patrón de Servicio (Service Layer)

Las funciones de views actúan como servicios:

```python
class GeneradorPDF:
    """Servicio de generación de PDF"""
    
    @staticmethod
    def generar(informe):
        # Lógica de generación
        doc.build(elements)
        return response

class GeneradorExcel:
    """Servicio de generación de Excel"""
    
    @staticmethod
    def generar(informe):
        # Lógica de generación
        wb.save(response)
        return response
```

---

### 1.3 Factory Method

Creación de objetos pdf y excel encapsulada:

```
┌─────────────────────────────────────────────┐
│            FACTORY METHOD                   │
├─────────────────────────────────────────────┤
│                                             │
│   generar_pdf() ─────────────────────────►  │
│       │                                      │
│       ├── Crea SimpleDocTemplate            │
│       ├── Configura estilos                 │
│       ├── Genera tablas                     │
│       ├── Genera gráficos                   │
│       └── Retorna HttpResponse              │
│                                             │
│   generar_excel() ─────────────────────────► │
│       │                                      │
│       ├── Crea Workbook                     │
│       ├── Crea hojas                        │
│       ├── Genera gráficos                   │
│       └── Retorna HttpResponse              │
│                                             │
└─────────────────────────────────────────────┘
```

---

### 1.4 Repository Pattern

Acceso a datos centralizado:

```python
class UsuarioRepository:
    """Repositorio de usuarios"""
    
    @staticmethod
    def get_by_id(id_usuario):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
            return cursor.fetchone()
    
    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios ORDER BY id")
            return cursor.fetchall()
    
    @staticmethod
    def get_stats():
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM usuarios")
            return cursor.fetchone()
```

---

## 2. Patrones de Diseño de Software

### 2.1 Singleton

Configuración de Django como singleton:

```python
# settings.py - Configuración única
SECRET_KEY = 'django-insecure-...'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Configuración única de base de datos
    }
}
```

---

### 2.2 Strategy Pattern

Diferentes estrategias de exportación:

```
┌─────────────────────────────┐
│      EXPORT STRATEGY        │
├─────────────────────────────┤
│                             │
│  + export()                 │
│         │                   │
│    ┌────┴────┐              │
│    ▼         ▼              │
│ ┌──────┐  ┌──────┐         │
│ │ PDF  │  │Excel │         │
│ │Strategy│ │Strategy│        │
│ └──────┘  └──────┘         │
│    │         │              │
│    ▼         ▼              │
│ ReportLab  openpyxl         │
│                             │
└─────────────────────────────┘
```

---

### 2.3 Template Method

Estructura de generación de documentos:

```python
class DocumentoGenerador:
    """Template Method para generación de documentos"""
    
    def generar(self, datos):
        self.preparar_estilos()
        self.agregar_encabezado(datos)
        self.agregar_contenido(datos)
        self.agregar_graficos(datos)
        self.agregar_pie()
        return self.construir()
    
    def preparar_estilos(self):
        pass  # Implementación específica
    
    def agregar_encabezado(self, datos):
        pass  # Implementación específica

class PDFGenerador(DocumentoGenerador):
    def preparar_estilos(self):
        # Estilos específicos para PDF
    
    def construir(self):
        return doc.build(elements)

class ExcelGenerador(DocumentoGenerador):
    def preparar_estilos(self):
        # Estilos específicos para Excel
    
    def construir(self):
        return wb.save(response)
```

---

## 3. Patrones de Presentación

### 3.1 SPA (Single Page Application)

Interfaz de una sola página:

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ SPA                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────────────────────────────────────┐  │
│  │ SIDEBAR │  │              MAIN CONTENT               │  │
│  │         │  │                                          │  │
│  │ [Buscar]│  │  ┌────────────────────────────────────┐  │  │
│  │ [Opciones]│ │  │         SECCIONES                 │  │  │
│  │ [Listar] │  │  │  - buscar (default)                │  │  │
│  │         │  │  │  - opciones                        │  │  │
│  │         │  │  │  - listar                          │  │  │
│  └─────────┘  │  └────────────────────────────────────┘  │  │
│               └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.2 Observador

Eventos en la interfaz:

```javascript
// Observador de eventos
document.getElementById('buscarForm').addEventListener('submit', function(e) {
    // Notifica al observador (SweetAlert)
    Swal.fire({
        title: 'Buscando...',
        showLoaderOnLoading: true
    });
});
```

---

## 4. Diagramas de Flujo

### 4.1 Flujo de Generación de PDF

```
                    ┌─────────────────┐
                    │  Solicitud PDF  │
                    │ /generar_pdf/1  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Validar ID     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼─────────┐        ┌──────────▼──────────┐
    │  Usuario existe  │        │   Usuario no existe   │
    └────────┬────────┘        └──────────┬───────────┘
              │                            │
    ┌─────────▼────────────────────────────▼──────────┐
    │              CONSULTAR DATOS                    │
    │  - Datos del usuario                           │
    │  - Estadísticas globales                       │
    │  - Distribución por mes                       │
    │  - Distribución por inicial                   │
    └────────────────────┬──────────────────────────┘
                         │
              ┌──────────▼────────────┐
              │  CREAR DOCUMENTO     │
              │  - Logo              │
              │  - Estilos           │
              │  - Tabla datos       │
              │  - Gráfico barras    │
              │  - Gráfico torta     │
              │  - Estadísticas      │
              └──────────┬────────────┘
                         │
              ┌──────────▼──────────┐
              │  RETORNAR PDF       │
              │  HttpResponse      │
              └─────────────────────┘
```

### 4.2 Flujo de Generación de Excel

```
                    ┌──────────────────┐
                    │ Solicitud Excel │
                    │ /generar_excel/1│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Validar ID     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼─────────┐        ┌─────────▼─────────┐
    │  Usuario existe  │        │  Usuario no existe │
    └────────┬────────┘        └──────────┬──────────┘
              │                            │
    ┌─────────▼────────────────────────────▼──────────┐
    │              CONSULTAR DATOS                       │
    │  - Usuario, estadísticas, gráficos                │
    └────────────────────┬──────────────────────────────┘
                         │
              ┌──────────▼────────────┐
              │  CREAR WORKBOOK       │
              │                       │
              │  HOJA 1: Datos         │
              │  HOJA 2: Estadísticas │
              │  HOJA 3: Gráfico Barras│
              │  HOJA 4: Gráfico Torta │
              │                       │
              └──────────┬────────────┘
                         │
              ┌──────────▼──────────┐
              │  RETORNAR EXCEL     │
              │  HttpResponse       │
              └─────────────────────┘
```

---

## 5. Resumen de Patrones

| Patrón | Ubicación | Descripción |
|--------|-----------|-------------|
| MVC | Django completo | Arquitectura del framework |
| Factory Method | views.py | Creación de PDF/Excel |
| Repository | views.py | Acceso a datos MySQL |
| Strategy | generar_pdf/excel | Diferentes formatos de exportación |
| Template Method | views.py | Estructura de generación |
| SPA | index.html | Interfaz de una página |
| Singleton | settings.py | Configuración única |

---

## 6. Beneficios de los Patrones

1. **Mantenibilidad**: Código organizado y separable
2. **Reutilización**: Funciones genéricas reutilizables
3. **Testabilidad**: Fácil de probar cada componente
4. **Flexibilidad**: Fácil agregar nuevos formatos
5. **Claridad**: Estructura clara y documentada

---

## 7. Tecnologías que Implementan los Patrones

- **Django**: MVC, Singleton, Factory
- **ReportLab**: Template Method, Factory
- **openpyxl**: Strategy, Template Method
- **Bootstrap**: SPA pattern
- **SweetAlert2**: Observer pattern