# Sistema de Generación de PDF y Excel - Django + MySQL

## Descripción del Proyecto

Sistema web desarrollado en Django que permite gestionar usuarios y generar reportes en formato PDF y Excel con gráficos estadísticos (barras y torta).

## Patrones de Diseño Utilizados

### 1. MVC (Model-View-Controller)
- **Model**: MySQL con tabla de usuarios
- **View**: Plantillas HTML con Bootstrap local
- **Controller**: Views de Django

### 2. Patrón de Servicio
- Lógica de negocio encapsulada en funciones de views
- Generación de documentos separada del controller

### 3. Factory Method
- `generar_pdf()` - Factory para crear documentos PDF
- `generar_excel()` - Factory para crear documentos Excel

### 4. Repository Pattern
- Acceso a datos mediante `connection.cursor()`
- Consultas SQL encapsuladas en métodos

## Arquitectura del Proyecto

```
mi_proyecto/
├── documentos/
│   ├── templates/
│   │   └── documentos/
│   │       ├── index.html    # Interfaz SPA
│   │       └── lista.html    # Listado de usuarios
│   ├── static/
│   │   ├── css/
│   │   │   ├── bootstrap.min.css    # Bootstrap local
│   │   │   ├── sweetalert2.min.css  # SweetAlert2 local
│   │   │   └── estilos.css          # Estilos personalizados
│   │   ├── js/
│   │   │   ├── bootstrap.bundle.min.js
│   │   │   └── sweetalert2.min.js
│   │   ├── fonts/
│   │   │   └── roboto-regular.woff2  # Fuente local
│   │   └── images/
│   │       └── logo.svg               # Logo del sistema
│   ├── views.py    # Controladores con lógica de negocio
│   ├── urls.py     # Rutas del proyecto
│   └── apps.py
└── mi_proyecto/
    ├── settings.py    # Configuración Django
    └── urls.py
```

## Requisitos

- Python 3.12+
- MySQL 8.0+
- Django 4.2+
- ReportLab (para PDF)
- openpyxl (para Excel)

## Instalación de Dependencias

```bash
pip install django mysqlclient reportlab openpyxl
```

## Script de Base de Datos MySQL

```sql
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS ejemplo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ejemplo;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar datos de ejemplo
INSERT INTO usuarios (nombre, correo, telefono, direccion) VALUES
('Juan Pérez', 'juan.perez@email.com', '555-123-4567', 'Calle Principal 123, Ciudad de México'),
('María García', 'maria.garcia@email.com', '555-987-6543', 'Avenida Central 456, Guadalajara'),
('Carlos López', 'carlos.lopez@email.com', '555-456-7890', 'Boulevard Norte 789, Monterrey'),
('Ana Martínez', 'ana.martinez@email.com', '555-321-0987', 'Plaza Juárez 101, Puebla'),
('Pedro Sánchez', 'pedro.sanchez@email.com', '555-654-3210', 'Calle Sur 202, Tijuana'),
('Laura Rodríguez', 'laura.rodriguez@email.com', '555-789-0123', 'Avenida Poniente 303, León'),
('Miguel Torres', 'miguel.torres@email.com', '555-111-2222', 'Calle Oriente 404, Torreón'),
('Sofia Hernández', 'sofia.hernandez@email.com', '555-333-4444', 'Boulevard Sur 505, Querétaro'),
('Diego Rivera', 'diego.riva@email.com', '555-555-6666', 'Avenida Norte 606, Aguascalientes'),
('Carmen Díaz', 'carmen.diaz@email.com', '555-777-8888', 'Calle Centro 707, San Luis Potosí');
```

## Configuración de Conexión

Editar `mi_proyecto/mi_proyecto/settings.py`:

```python
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
```

## Archivos Estáticos Locales

### Bootstrap 5.3 (Local)
- `static/css/bootstrap.min.css`
- `static/js/bootstrap.bundle.min.js`

### SweetAlert2 11.x (Local)
- `static/css/sweetalert2.min.css`
- `static/js/sweetalert2.min.js`

### Fuentes Google (Local)
- `static/fonts/roboto-regular.woff2`

### Logo del Sistema
- `static/images/logo.svg`

## Ejecutar el Proyecto

```bash
cd mi_proyecto
python manage.py runserver
```

## Rutas Disponibles

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal con menú SPA |
| `/lista/` | Listar todos los usuarios |
| `/generar_pdf/<id>/` | PDF de usuario específico |
| `/generar_excel/<id>/` | Excel de usuario específico |
| `/generar_pdf_todos/` | PDF de todos los usuarios |
| `/generar_excel_todos/` | Excel de todos los usuarios |

## Características

### PDF con Gráficos (3 tipos)
- **Gráfico de Barras**: Usuarios registrados por mes
- **Gráfico de Torta**: Distribución por inicial del nombre
- **Gráfico de Dispersión**: Posición X/Y por usuario
- **Logo**: Imagen del sistema en el encabezado
- **Estadísticas**: Métricas del sistema

### Excel con Gráficos (5 hojas)
- **Hoja 1**: Datos del usuario
- **Hoja 2**: Estadísticas del sistema
- **Hoja 3**: Gráfico de barras (visual + interactivo)
- **Hoja 4**: Gráfico de torta (visual + interactivo)
- **Hoja 5**: Gráfico de dispersión (visual + interactivo)

### Búsqueda Avanzada
- **Por ID**: Buscar usuario específico por identificador
- **Por Nombre**: Buscar usuarios por nombre (múltiples resultados)
- **Estadísticas**: Visualización de gráficos del usuario
- **Impresión**: Opción de imprimir directamente el PDF

### Interfaz SPA
- Menú lateral de navegación
- Búsqueda de usuario por ID
- Opciones de informe (PDF/Excel global)
- Listado de todos los usuarios
- Diseño moderno con Bootstrap local
- Notificaciones con SweetAlert2 local

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|------------|
| Django | 4.2+ | Framework web |
| MySQL | 8.0+ | Base de datos |
| Bootstrap | 5.3 | UI/UX local |
| SweetAlert2 | 11.x | Alertas local |
| ReportLab | - | Generación PDF |
| openpyxl | - | Generación Excel |
| Roboto | - | Fuente local |

## Estructura de Código

### views.py - Funciones Principales

```python
def index(request):
    """Vista principal - Búsqueda de usuarios"""

def generar_pdf(request, id_usuario):
    """Genera PDF con gráficos de barras y torta"""

def generar_excel(request, id_usuario):
    """Genera Excel con múltiples hojas y gráficos"""

def generar_pdf_todos(request):
    """Genera PDF de todos los usuarios"""

def generar_excel_todos(request):
    """Genera Excel de todos los usuarios"""

def listar_usuarios(request):
    """Lista todos los usuarios"""
```

## Licencia

MIT License - 2026