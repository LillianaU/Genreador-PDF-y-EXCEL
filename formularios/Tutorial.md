# Tutorial Completo - Sistema de Generación de PDF y Excel

## Índice
1. [Requisitos Previos](#1-requisitos-previos)
2. [Instalación de MySQL](#2-instalación-de-mysql)
3. [Configuración de Python y Dependencias](#3-configuración-de-python-y-dependencias)
4. [Instalación de Archivos Locales](#4-instalación-de-archivos-locales)
5. [Configuración del Proyecto](#5-configuración-del-proyecto)
6. [Ejecución del Sistema](#6-ejecución-del-sistema)
7. [Uso del Sistema](#7-uso-del-sistema)
8. [Solución de Problemas](#8-solución-de-problemas)

---

## 1. Requisitos Previos

### Software Necesario
- **Python 3.12+**: https://www.python.org/downloads/
- **MySQL 8.0+**: https://dev.mysql.com/downloads/installer/
- **Visual C++ Build Tools** (Windows): Para mysqlclient

### Verificar Instalación
```bash
python --version
mysql --version
```

---

## 2. Instalación de MySQL

### Windows
1. Descarga MySQL Installer desde https://dev.mysql.com/downloads/installer/
2. Ejecuta el instalador
3. Selecciona "Developer Default"
4. Configura la contraseña root
5. Completa la instalación

### Crear Base de Datos
```sql
CREATE DATABASE IF NOT EXISTS ejemplo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ejemplo;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Insertar Datos de Prueba
```sql
INSERT INTO usuarios (nombre, correo, telefono, direccion) VALUES
('Juan Pérez', 'juan.perez@email.com', '555-123-4567', 'Calle Principal 123'),
('María García', 'maria.garcia@email.com', '555-987-6543', 'Avenida Central 456'),
('Carlos López', 'carlos.lopez@email.com', '555-456-7890', 'Boulevard Norte 789');
```

---

## 3. Configuración de Python y Dependencias

### Instalar Python (si no tienes)
1. Descarga Python desde https://www.python.org/downloads/
2. Durante instalación, marca "Add Python to PATH"

### Crear Entorno Virtual (recomendado)
```bash
python -m venv ven
ven\Scripts\activate
```

### Instalar Dependencias
```bash
pip install django==4.2.28
pip install mysqlclient
pip install reportlab
pip install openpyxl
```

**Nota para Windows**: Si mysqlclient falla, instala Visual C++ Build Tools.

---

## 4. Instalación de Archivos Locales

### 4.1 Bootstrap 5.3 (Local)

Los archivos ya están descargados en:
- `static/css/bootstrap.min.css`
- `static/js/bootstrap.bundle.min.js`

**Verificación**:
```bash
dir mi_proyecto\documentos\static\css\bootstrap.min.css
dir mi_proyecto\documentos\static\js\bootstrap.bundle.min.js
```

### 4.2 SweetAlert2 11.x (Local)

Archivos en:
- `static/css/sweetalert2.min.css`
- `static/js/sweetalert2.min.js`

### 4.3 Fuentes Google (Local)

**Fuente Roboto**:
- `static/fonts/roboto-regular.woff2`

**Verificar fuente en CSS**:
```css
@font-face {
    font-family: 'Roboto';
    src: url('../fonts/roboto-regular.woff2') format('woff2');
}
```

### 4.4 Logo del Sistema

El logo está en: `static/images/logo.svg`

El sistema incluye:
- SVG vectorial con gradiente
- Diseño moderno con iniciales "SG"

---

## 5. Configuración del Proyecto

### 5.1 Actualizar settings.py

Editar `mi_proyecto/mi_proyecto/settings.py`:

```python
# Configuración de base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ejemplo',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña_mysql',
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

### 5.2 Verificar conexión
```bash
cd mi_proyecto
python manage.py check
```

---

## 6. Ejecución del Sistema

### Iniciar Servidor
```bash
cd mi_proyecto
python manage.py runserver
```

### Acceder al Sistema
Abre en tu navegador: **http://127.0.0.1:8000/**

---

## 7. Uso del Sistema

### 7.1 Menú Principal (SPA)

La interfaz tiene un menú lateral con tres opciones:

1. **Buscar Usuario**
   - Ingresa el ID del usuario
   - Haz clic en "Buscar"
   - Verás los datos del usuario
   - Botones para descargar PDF o Excel

2. **Opciones de Informe**
   - Generar PDF de todos los usuarios
   - Generar Excel de todos los usuarios

3. **Listar Todos**
   - Tabla con todos los usuarios
   - Botones de PDF/Excel por cada uno

### 7.2 Generar PDF

El PDF incluye:
- Logo del sistema
- Datos del usuario
- **Gráfico de Barras**: Usuarios por mes
- **Gráfico de Torta**: Distribución por inicial
- **Gráfico de Dispersión**: Posición X/Y por usuario
- Estadísticas del sistema

**Ruta**: `/generar_pdf/<id>/`

### 7.3 Generar Excel

El Excel tiene múltiples hojas:
- **Hoja 1**: Datos del usuario
- **Hoja 2**: Estadísticas
- **Hoja 3**: Gráfico de Barras (con gráfico interactivo)
- **Hoja 4**: Gráfico de Torta (con gráfico interactivo)
- **Hoja 5**: Gráfico de Dispersión (con gráfico interactivo)

**Ruta**: `/generar_excel/<id>/`

### 7.4 Búsqueda Avanzada

La búsqueda permite:
1. **Buscar por ID**: Ingresa el número de ID
2. **Buscar por Nombre**: Ingresa el nombre (múltiples resultados)
3. **Ver Estadísticas**: Gráficos de barras, torta, dispersión
4. **Imprimir**: Botón para abrir PDF en nueva pestaña

### 7.5 Impresión

- Click en botón "Imprimir" abre el PDF en nueva pestaña
- Desde el navegador se puede imprimir o guardar

### 7.4 Reporte General

**PDF de todos**: `/generar_pdf_todos/`
**Excel de todos**: `/generar_excel_todos/`

---

## 8. Solución de Problemas

### Error: Can't connect to MySQL server
**Solución**: Verifica que MySQL esté ejecutándose como servicio.
```bash
net start mysql
```

### Error: mysqlclient not found
**Solución**: Instala Visual C++ Build Tools o usa pip install mysqlclient.

### Error: Port 8000 in use
**Solución**: Usa otro puerto.
```bash
python manage.py runserver 8080
```

### Error: Static files not found
**Solución**: Verifica STATICFILES_DIRS en settings.py.

### Error: Template not found
**Solución**: Verifica que las plantillas estén en la ruta correcta.

---

## Estructura de Archivos

```
proyecto/
├── README.md                    # Documentación general
├── Tutorial.md                   # Este tutorial
├── PatronesDeDiseno.md           # Patrones utilizados
├── mi_proyecto/
│   ├── manage.py
│   ├── mi_proyecto/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── documentos/
│       ├── views.py              # Controladores
│       ├── urls.py               # Rutas
│       ├── templates/
│       │   └── documentos/
│       │       ├── index.html    # Interfaz SPA
│       │       └── lista.html    # Lista usuarios
│       └── static/
│           ├── css/
│           ├── js/
│           ├── fonts/
│           └── images/
```

---

## Código del Proyecto - views.py

### Funciones Principales

```python
# Vista principal
def index(request):
    """Maneja búsqueda de usuarios"""

# Generación de PDF
def generar_pdf(request, id_usuario):
    """Genera PDF con:
       - Logo del sistema
       - Datos del usuario
       - Gráfico de barras (usuarios por mes)
       - Gráfico de torta (distribución por inicial)
       - Estadísticas
    """

# Generación de Excel
def generar_excel(request, id_usuario):
    """Genera Excel con:
       - Hoja de datos del usuario
       - Hoja de estadísticas
       - Hoja con gráfico de barras
       - Hoja con gráfico de torta
    """

# Reportes globales
def generar_pdf_todos(request):
    """PDF de todos los usuarios"""

def generar_excel_todos(request):
    """Excel de todos los usuarios"""

def listar_usuarios(request):
    """Lista todos los usuarios"""
```

---

## Patrones de Diseño Utilizados

### MVC (Model-View-Controller)
- Django implementa este patrón naturalmente
- Model: Base de datos MySQL
- View: Templates HTML
- Controller: Functions en views.py

### Factory Method
- `generar_pdf()` - Crea documentos PDF
- `generar_excel()` - Crea documentos Excel

### Repository
- Acceso a datos mediante `connection.cursor()`
- Consultas SQL centralizadas

---

## Tecnologías del Proyecto

| Componente | Tecnología | Versión/Notas |
|------------|------------|----------------|
| Framework | Django | 4.2+ |
| Base de datos | MySQL | 8.0+ |
| PDF | ReportLab | Library |
| Excel | openpyxl | Library |
| UI | Bootstrap | 5.3 (local) |
| Alertas | SweetAlert2 | 11.x (local) |
| Fuente | Roboto | WOFF2 (local) |

---

## Créditos

Sistema desarrollado con Django + MySQL
Gráficos estadísticos: ReportLab (PDF) + openpyxl (Excel)
UI: Bootstrap 5.3 + SweetAlert2 - Todo local