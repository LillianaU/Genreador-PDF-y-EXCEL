# Sistema de Generación de PDF y Excel - Django + MySQL

## 📋 Descripción del Proyecto

Sistema web desarrollado en **Django** que permite gestionar usuarios y generar reportes en formato **PDF** y **Excel** con gráficos estadísticos profesionales (Barras, Torta, Dispersión) estilo Chart.js.

## 🏗️ Arquitectura y Patrones de Diseño

### Patrones Utilizados

| Patrón | Descripción | Ubicación |
|--------|-------------|-----------|
| **MVC** | Modelo-Vista-Controlador de Django | Proyecto completo |
| **Factory Method** | Creación de documentos PDF/Excel | `views.py` |
| **Repository** | Acceso a datos MySQL mediante cursor | `views.py` |
| **Service Layer** | Lógica de negocio encapsulada | Funciones de views |
| **Template Method** | Estructura de generación de documentos | `generar_pdf/excel` |

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    DJANGO MVC                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   MODEL (MySQL)     VIEW (HTML/Template)    CONTROLLER │
│   ┌──────────┐      ┌──────────────┐      ┌─────────┐│
│   │ usuarios │ ───► │   index.html  │ ◄─── │ views.py││
│   │  tabla   │      │  lista.html   │      │         ││
│   └──────────┘      └──────────────┘      └─────────┘│
│                          │                    │         │
│                          ▼                    ▼         │
│                    (Bootstrap+           (PDF/Excel)    │
│                    SweetAlert2)                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Requisitos

### Dependencias Python

```
Django==4.2.28
mysqlclient==2.2.4
reportlab==4.2.5
openpyxl==3.1.5
Pillow==10.4.0
```

### Base de Datos

- **MySQL 8.0+**
- Base de datos: `ejemplo`
- Tabla: `usuarios`

## 📦 Estructura del Proyecto

```
mi_proyecto/
├── manage.py
├── mi_proyecto/
│   ├── settings.py          # Configuración Django
│   ├── urls.py              # Rutas principales
│   └── wsgi.py
└── documentos/
    ├── views.py             # Controladores con patrones de diseño
    ├── urls.py              # Rutas de la app
    ├── templates/
    │   └── documentos/
    │       ├── index.html   # Interfaz principal (menú flotante)
    │       └── lista.html   # Lista de usuarios
    └── static/
        ├── css/
        │   ├── bootstrap.min.css    # Bootstrap local
        │   ├── sweetalert2.min.css   # SweetAlert2 local
        │   └── estilos.css          # Estilos personalizados
        ├── js/
        │   ├── bootstrap.bundle.min.js
        │   └── sweetalert2.min.js
        ├── fonts/
        │   └── roboto-regular.woff2  # Fuente local
        └── images/
            └── logo.png              # Logo del sistema
```

## 🚀 Instalación

### 1. Clonar el proyecto

```bash
git clone <repositorio>
cd formularios
```

### 2. Crear entorno virtual

```bash
python -m venv ven
ven\Scripts\activate  # Windows
source ven/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

```sql
CREATE DATABASE ejemplo CHARACTER SET utf8mb4;
```

### 5. Ejecutar migraciones y cargar datos

```bash
cd mi_proyecto
python manage.py migrate
# O ejecutar el script SQL del README
```

### 6. Iniciar servidor

```bash
python manage.py runserver
```

## 📊 Características

### Interfaz de Usuario
- ✅ Menú flotante tipo acordeón (estilo MediAgenda Pro)
- ✅ Diseño moderno con gradientes
- ✅ Iconos de Font Awesome
- ✅ Alertas SweetAlert2
- ✅ Modal Bootstrap para mostrar usuario
- ✅ Búsqueda por ID y por Nombre

### PDF con Gráficos (Estilo Chart.js)
- 📊 **Gráfico de Barras**: Usuarios por mes
- 🥧 **Gráfico de Torta**: Distribución por inicial
- ⚡ **Gráfico de Dispersión**: Posición X/Y real
- 🖼️ Logo del sistema
- 📈 Estadísticas generales

### Excel con Gráficos
- 📋 Hoja 1: Datos del usuario
- 📊 Hoja 2: Estadísticas del sistema
- 📈 Hoja 3: Gráfico de Barras (interactivo)
- 🥧 Hoja 4: Gráfico de Torta (interactivo)
- ⚡ Hoja 5: Gráfico de Dispersión (interactivo)

## 📝 Rutas Disponibles

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal con menú flotante |
| `/lista/` | Listar todos los usuarios |
| `/generar_pdf/<id>/` | PDF de usuario específico |
| `/generar_excel/<id>/` | Excel de usuario específico |
| `/generar_pdf_todos/` | PDF de todos los usuarios |
| `/generar_excel_todos/` | Excel de todos los usuarios |

## 📄 Script de Base de Datos

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nombre, correo, telefono, direccion) VALUES
('Juan Pérez', 'juan.perez@email.com', '555-123-4567', 'Calle Principal 123'),
('María García', 'maria.garcia@email.com', '555-987-6543', 'Avenida Central 456'),
-- ... más registros
```

## 🔧 Configuración

### settings.py

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

STATICFILES_DIRS = [
    BASE_DIR / 'documentos' / 'static',
]
```

## 📚 Documentación Adicional

- [Tutorial.md](Tutorial.md) - Tutorial paso a paso
- [PatronesDeDiseno.md](PatronesDeDiseno.md) - Patrones de diseño detallados

## 👨‍💻 Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| Django 4.2 | Framework web |
| MySQL 8.0 | Base de datos |
| ReportLab | Generación PDF |
| openpyxl | Generación Excel |
| Bootstrap 5.3 | UI (local) |
| SweetAlert2 | Alertas (local) |
| Font Awesome | Iconos |

## 📄 Licencia

MIT License - 2026

---

**Desarrollado con Django + MySQL + ReportLab + openpyxl**
**Gráficos estilo Chart.js en PDF y Excel**