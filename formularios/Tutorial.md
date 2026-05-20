# Tutorial Completo - Sistema de Generación de PDF y Excel

## Sistema con Django ORM + MySQL

---

## 📊 Diagramas del Proyecto
C1: Usuario usa sistema → busca/genera PDF/Excel -C1: Requerimientos del sistema
C2: 4 funciones: buscar, PDF, Excel, general -C2: Procesos funcionales
C3: Datos fluyen: formulario → servidor → BD → archivo- C3: Flujo de informació
C4: Capas: pantalla, código, generación, base de datos- C4: Componentes técnicos

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
│   ORM      ReportLab  openpyxl   Todo  │
└────────────────────────────────────────┘
```

### C3 - Flujo de Datos

```
┌────────────────────────────────────────┐
│         C3 - FLUJO                     │
├────────────────────────────────────────┤
│                                        │
│ INICIO → POST → View → ORM            │
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
│ LÓGICA:      Django ORM + Views      │
│      │                                 │
│ SERVICIOS:    PDF (ReportLab)        │
│              Excel (openpyxl)          │
│      │                                 │
│ DATOS:       MySQL + Migrations       │
└────────────────────────────────────────┘
```

---

## 1. Requisitos Previos

### Software Necesario
- Python 3.12+
- MySQL 8.0+
- pip

### Dependencias (requirements.txt)
```
Django==4.2.28
mysqlclient==2.2.4
reportlab==4.2.5
openpyxl==3.1.5
Pillow==10.4.0
pytest==8.3.3
pytest-django==4.9.0
```

---

## 2. INSTALACIÓN DEL PROYECTO

### Paso 1: Crear carpeta del proyecto
```bash
mkdir formularios
cd formularios
```

### Paso 2: Crear entorno virtual
```bash
python -m venv ven

# Activar (Windows)
ven\Scripts\activate

# Activar (Linux/Mac)
source ven/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt

# Si hay error con mysqlclient en Windows, instalar Visual C++ Build Tools
```

### Paso 4: Crear proyecto Django
```bash
django-admin startproject mi_proyecto .
python manage.py startapp documentos
```

### Paso 5: Configurar settings.py
**Archivo:** `mi_proyecto/mi_proyecto/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'documentos',  # ← AGREGAR
]

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

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'documentos', 'static')]
```

### Paso 6: Configurar URLs
**Archivo:** `mi_proyecto/mi_proyecto/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documentos.urls')),
]
```

---

## 3. MODELO Y MIGRACIONES (Django ORM)

### 3.1 Modelo - models.py
**Archivo:** `mi_proyecto/documentos/models.py`

```python
from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return self.nombre
```

### 3.2 Crear migraciones
```bash
cd mi_proyecto

# Crear archivos de migración
python manage.py makemimientos documentos

# Aplicar a la base de datos
python manage.py migrate

# Ver estado
python manage.py showmigrations
```

**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: documentos
Running migrations:
  Creating table usuarios...
```

---

## 4. CREAR USUARIOS DE PRUEBA

### Opción 1: Desde MySQL directamente
```sql
USE ejemplo;

INSERT INTO usuarios (nombre, correo, telefono, direccion) VALUES
('Juan Pérez', 'juan@email.com', '555-123-4567', 'Calle 123'),
('María García', 'maria@email.com', '555-987-6543', 'Avenida 456'),
('Carlos López', 'carlos@email.com', '555-456-7890', 'Boulevard 789');
```

### Opción 2: Desde Django Shell
```bash
python manage.py shell
```

```python
from documentos.models import Usuario

# Crear usuarios
Usuario.objects.create(nombre='Juan Pérez', correo='juan@email.com', telefono='555-123-4567')
Usuario.objects.create(nombre='María García', correo='maria@email.com', telefono='555-987-6543')
Usuario.objects.create(nombre='Carlos López', correo='carlos@email.com', telefono='555-456-7890')

# Verificar
Usuario.objects.all()
```

---

## 5. EJECUTAR EL PROYECTO

```bash
cd mi_proyecto
python manage.py runserver
```

**Navegador:**
- Inicio: http://127.0.0.1:8000/
- Lista: http://127.0.0.1:8000/lista/

---

## 6. PLAN DE PRUEBAS

### 6.1 Ejecutar pruebas unitarias

```bash
cd mi_proyecto
python manage.py test documentos --verbosity=2
```

**Resultados esperados:** 23 pruebas pasando

### 6.2 Tipos de pruebas

| Tipo | Descripción | Comandos |
|------|-------------|----------|
| Unitarias | Modelo y métodos | `test documentos.test.PruebasModeloUsuario` |
| Vistas | Rutas y templates | `test documentos.test.PruebasVistas` |
| PDF | Generación | `test documentos.test.PruebasGeneracionPDF` |
| Excel | Generación | `test documentos.test.PruebasGeneracionExcel` |
| ORM | Consultas | `test documentos.test.PruebasConsultasORM` |

### 6.3 Pruebas manuales

| # | Prueba | Resultado Esperado |
|---|-------|-------------------|
| 1 | Abrir http://127.0.0.1:8000/ | Página con menú flotante café |
| 2 | Buscar por ID "1" | Muestra modal con usuario |
| 3 | Buscar por nombre "Juan" | Muestra resultados |
| 4 | Click PDF en usuario | Descarga PDF |
| 5 | Click Excel en usuario | Descarga Excel |
| 6 | Ir a /lista/ | Muestra tabla de usuarios |
| 7 | Generar PDF general | PDF con todos los datos |
| 8 | Generar Excel general | Excel con gráficos |

### 6.4 Ejecutar con pytest (opcional)
```bash
pip install pytest pytest-django

pytest documentos/test.py -v
```

---

## 7. CONSULTAS ORM VS SQL

| Operación | SQL Directo | Django ORM |
|-----------|-------------|------------|
| Obtener uno | `SELECT * FROM usuarios WHERE id=1` | `Usuario.objects.get(id=1)` |
| Obtener todos | `SELECT * FROM usuarios` | `Usuario.objects.all()` |
| Buscar like | `WHERE nombre LIKE '%Juan%'` | `filter(nombre__icontains='Juan')` |
| Contar | `SELECT COUNT(*)` | `count()` |
| Ordenar | `ORDER BY nombre` | `order_by('nombre')` |
| Crear | `INSERT INTO...` | `Usuario.objects.create(...)` |

---

## 8. ESTRUCTURA DEL PROYECTO

```
formularios/
├── mi_proyecto/
│   ├── manage.py
│   ├── settings.py          ← DB, STATIC
│   └── urls.py              ← include documentos.urls
├── documentos/
│   ├── models.py            ← Modelo Usuario (ORM)
│   ├── views.py             ← Vistas con ORM
│   ├── urls.py              ← Rutas
│   ├── test.py              ← Pruebas
│   ├── migrations/
│   │   └── 0001_initial.py  ← Migración inicial
│   ├── templates/
│   │   └── documentos/
│   │       ├── index.html   ← Menú SPA
│   │       └── lista.html   ← Lista usuarios
│   └── static/
│       ├── css/             ← Bootstrap
│       ├── js/              ← Bootstrap
│       └── images/          ← logo.jpg
├── requirements.txt         ← Dependencias
├── Tutorial.md             ← Este archivo
├── README.md               ← Documentación
└── PatronesDeDiseno.md     ← Patrones de diseño
```

---

## 9. PALETA DE COLORES - TEMA CAFÉS

| Color | Hex | Uso |
|-------|-----|-----|
| Café Oscuro | #4A3728 | Header, textos |
| Café Medio | #6B4423 | Botones |
| Café Claro | #8B6914 | Iconos |
| Dorado | #B8860B | Destacados |
| Crema Claro | #FAF8F5 | Fondo |

---

## 10. SOLUCIÓN DE PROBLEMAS

| Error | Solución |
|-------|----------|
| mysqlclient no instala | Instalar Visual C++ Build Tools |
| Table 'usuarios' already exists | La tabla ya existe, usar migrate --fake |
| Static files not found | Verificar STATICFILES_DIRS |
| Port in use | Usar `runserver 8080` |
| Migration error | `python manage.py migrate --fake` |

---

**¡Proyecto listo para usar!** 🎉