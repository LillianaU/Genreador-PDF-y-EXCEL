# Sistema de Generación de PDF y Excel - Django ORM + MySQL

## Descripción

Sistema web desarrollado en **Django** con **Django ORM** que permite gestionar usuarios y generar reportes en formato **PDF** y **Excel** con gráficos estadísticos profesionales (Barras, Torta, Dispersión) estilo Chart.js.

---

## Características

- ✅ Búsqueda de usuarios por ID
- ✅ Búsqueda de usuarios por nombre
- ✅ Generación de PDF con gráficos
- ✅ Generación de Excel con gráficos
- ✅ Reportes generales de todos los usuarios
- ✅ Menú flotante SPA moderno
- ✅ Paleta de colores cafés
- ✅ Pruebas unitarias automáticas (23 pruebas)
- ✅ Documentación completa

---

## Requisitos

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

## Installation

```bash
# 1. Clonar o descargar el proyecto
cd formularios

# 2. Crear entorno virtual
python -m venv ven

# 3. Activar entorno
ven\Scripts\activate  # Windows
source ven/bin/activate  # Linux/Mac

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar base de datos en settings.py

# 6. Crear migraciones
cd mi_proyecto
python manage.py makemigrations documentos

# 7. Aplicar migraciones
python manage.py migrate

# 8. Crear usuarios de prueba
python manage.py shell
>>> from documentos.models import Usuario
>>> Usuario.objects.create(nombre='Juan', correo='juan@email.com')

# 9. Ejecutar servidor
python manage.py runserver
```

---

## Ejecución

```bash
cd mi_proyecto

# Iniciar servidor
python manage.py runserver
```

**Navegador:** http://127.0.0.1:8000/

---

## Pruebas

### Ejecutar pruebas automáticas
```bash
cd mi_proyecto
python manage.py test documentos --verbosity=2
```

**Resultado:** 23 pruebas pasando

### Pruebas con pytest
```bash
pip install pytest pytest-django
pytest documentos/test.py -v
```

### Pruebas manuales

| # | Prueba | Resultado |
|---|-------|-----------|
| 1 | Abrir http://127.0.0.1:8000/ | Página principal |
| 2 | Buscar por ID | Muestra usuario |
| 3 | Buscar por nombre | Muestra resultados |
| 4 | Descargar PDF | Archivo PDF |
| 5 | Descargar Excel | Archivo Excel |
| 6 | Ver /lista/ | Tabla de usuarios |

---
----------

## Diagramas de Procesos
--- que hace estos diagramas ??
# 


### C1 - Diagrama de Contexto

```
┌─────────────────────────────────────────────┐
│           C1 - DIAGRAMA DE CONTEXTO         │
├─────────────────────────────────────────────┤
│                                             │
│    ┌──────────┐                             │
│    │ USUARIO  │──────► SISTEMA ──► MySQL   │
│    └──────────┘                             │
│         ▲              │                    │
│         │              ▼                   │
│         │        PDF / Excel               │
│         │              │                   │
│         └──────────────┘                   │
│            Resultados                      │
└─────────────────────────────────────────────┘
```

### C2 - Diagrama de Procesos

```
┌─────────────────────────────────────────────┐
│           C2 - DIAGRAMA DE PROCESOS         │
├─────────────────────────────────────────────┤
│                                             │
│   BÚSQUEDA      PDF        EXCEL   GENERAL  │
│      │           │           │        │     │
│      ▼           ▼           ▼        ▼     │
│   ORM        ReportLab   openpyxl    Todo    │
└─────────────────────────────────────────────┘
```

### C3 - Flujo de Datos

```
┌─────────────────────────────────────────────┐
│              C3 - FLUJO DE DATOS            │
├─────────────────────────────────────────────┤
│                                             │
│   INICIO → POST → View → ORM → MySQL       │
│              │           │                  │
│              ▼           ▼                  │
│           PDF        Excel                  │
│                                             │
└─────────────────────────────────────────────┘
```

### C4 - Componentes

```
┌─────────────────────────────────────────────┐
│            C4 - COMPONENTES                 │
├─────────────────────────────────────────────┤
│                                             │
│ PRESENTACIÓN:  HTML + CSS + JS (Bootstrap) │
│ LÓGICA:      Django ORM + Views           │
│ SERVICIOS:    PDF (ReportLab)              │
│              Excel (openpyxl)              │
│ DATOS:       MySQL + Migrations            │
└─────────────────────────────────────────────┘
```

---

## Estructura del Proyecto

```
formularios/
├── mi_proyecto/
│   ├── manage.py
│   ├── settings.py
│   └── urls.py
├── documentos/
│   ├── models.py         ← Modelo Usuario (ORM)
│   ├── views.py          ← Vistas con gráficos
│   ├── urls.py           ← Rutas
│   ├── test.py           ← Pruebas unitarias
│   ├── migrations/       ← Migraciones Django
│   ├── templates/
│   │   └── documentos/
│   │       ├── index.html
│   │       └── lista.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── requirements.txt
├── Tutorial.md
├── PlanDePruebas.md
├── PatronesDeDiseno.md
└── README.md
```

---

## Migraciones y Django ORM

```bash
# Crear modelo en models.py
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    ...

# Crear migraciones
python manage.py makemigrations documentos

# Aplicar
python manage.py migrate

# Consultas ORM
Usuario.objects.all()           # Todos
Usuario.objects.get(id=1)       # Por ID
Usuario.objects.filter(nombre__icontains='Juan')  # Buscar
```

---

## Paleta de Colores - Tema Cafés

| Color | Hex | Uso |
|-------|-----|-----|
| Café Oscuro | #4A3728 | Header |
| Café Medio | #6B4423 | Botones |
| Café Claro | #8B6914 | Iconos |
| Dorado | #B8860B | Destacados |
| Crema | #FAF8F5 | Fondo |

---

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [Tutorial.md](Tutorial.md) | Tutorial paso a paso |
| [PlanDePruebas.md](PlanDePruebas.md) | Plan de pruebas completo |
| [PatronesDeDiseno.md](PatronesDeDiseno.md) | Patrones de diseño |
| requirements.txt | Dependencias del proyecto |

---

## Tecnologías

- **Backend:** Django 4.2.28
- **Base de datos:** MySQL
- **ORM:** Django ORM
- **PDF:** ReportLab
- **Excel:** openpyxl
- **Frontend:** Bootstrap 5 + CSS personalizado

---

**Versión:** 1.0  
**Fecha:** Mayo 2026  
**Desarrollado con:** Django ORM + MySQL + ReportLab + openpyxl