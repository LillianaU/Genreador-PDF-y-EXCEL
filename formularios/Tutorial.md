# Tutorial Completo - Sistema de Generación de PDF y Excel

## Índice
1. [Requisitos](#1-requisitos)
2. [Instalación](#2-instalación)
3. [Configuración](#3-configuración)
4. [Estructura del Proyecto](#4-estructura-del-proyecto)
5. [Uso del Sistema](#5-uso-del-sistema)
6. [Gráficos Implementados](#6-gráficos-implementados)
7. [Patrones de Diseño](#7-patrones-de-diseño)
8. [Solución de Problemas](#8-solución-de-problemas)

---

## 1. Requisitos

### Software Necesario
- Python 3.12+
- MySQL 8.0+
- pip (gestor de paquetes)

### Dependencias Python
```
Django==4.2.28
mysqlclient==2.2.4
reportlab==4.2.5
openpyxl==3.1.5
Pillow==10.4.0
```

---

## 2. Instalación

### Paso 1: Clonar o extraer el proyecto
```bash
cd formularios
```

### Paso 2: Crear entorno virtual
```bash
python -m venv ven
ven\Scripts\activate  # Windows
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

**Nota para Windows**: Si mysqlclient falla, instala [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

---

## 3. Configuración

### 3.1 Configurar MySQL

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
('Juan Pérez', 'juan.perez@email.com', '555-123-4567', 'Calle Principal 123'),
('María García', 'maria.garcia@email.com', '555-987-6543', 'Avenida Central 456'),
('Carlos López', 'carlos.lopez@email.com', '555-456-7890', 'Boulevard Norte 789');
```

### 3.2 Configurar Django

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

STATICFILES_DIRS = [
    BASE_DIR / 'documentos' / 'static',
]
```

---

## 4. Estructura del Proyecto

```
formularios/
├── README.md              # Documentación principal
├── Tutorial.md            # Este archivo
├── PatronesDeDiseno.md    # Patrones de diseño
├── requirements.txt       # Dependencias Python
├── crear_logo.py         # Script para crear logo
├── mi_proyecto/
│   ├── manage.py
│   ├── mi_proyecto/
│   │   ├── settings.py
│   │   └── urls.py
│   └── documentos/
│       ├── views.py       # Controladores (MVC)
│       ├── urls.py        # Rutas
│       ├── templates/
│       │   └── documentos/
│       │       ├── index.html    # Interfaz principal
│       │       └── lista.html    # Lista usuarios
│       └── static/
│           ├── css/       # Bootstrap + SweetAlert2
│           ├── js/        # JS lokal
│           ├── fonts/     # Fuentes locales
│           └── images/   # Logo
```

---

## 5. Uso del Sistema

### 5.1 Iniciar Servidor
```bash
cd mi_proyecto
python manage.py runserver
```

### 5.2 Acceder
Abre en tu navegador: **http://127.0.0.1:8000/**

### 5.3 Navegación

#### Menú Flotante (Lado izquierdo)
- **Búsqueda**: Buscar por ID o por Nombre
- **Informes**: Generar PDF/Excel general
- **Gráficos**: Ver tipos de gráficos disponibles
- **Usuarios**: Ver lista completa

#### Buscar Usuario
1. Click en "Buscar por ID" en el menú
2. Ingresa el ID (ej: 1)
3. Click en "Buscar"
4. Se abre **modal Bootstrap** con resumen
5. Desde el modal: imprimir PDF o exportar Excel

#### Generar Informe General
1. Click en "Informes" en el menú
2. Selecciona "Generar PDF General" o "Generar Excel General"
3. Se descarga el archivo con todos los gráficos

---

## 6. Gráficos Implementados

### 6.1 PDF (Estilo Chart.js - ReportLab)

| Gráfico | Descripción | Datos |
|---------|-------------|-------|
| **Barras** | Usuarios registrados por mes | Distribución mensual real |
| **Torta** | Distribución por inicial del nombre | Porcentaje real |
| **Dispersión** | Posición X/Y basada en longitud de datos | Datos reales |

### 6.2 Excel (openpyxl con gráficos interactivos)

| Hoja | Contenido |
|------|-----------|
| 1 | Datos del usuario |
| 2 | Estadísticas del sistema |
| 3 | Gráfico de Barras (interactivo) |
| 4 | Gráfico de Torta (interactivo) |
| 5 | Gráfico de Dispersión (interactivo) |

---

## 7. Patrones de Diseño

### 7.1 MVC (Model-View-Controller)
```python
# MODEL - Acceso a datos
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id])

# VIEW - Renderizado
return render(request, 'documentos/index.html', {'usuario': usuario})

# CONTROLLER - Lógica
def generar_pdf(request, id_usuario):
    # Procesamiento y generación
```

### 7.2 Factory Method
```python
def generar_pdf(request, id_usuario):
    """Fábrica de documentos PDF"""
    doc = SimpleDocTemplate(...)
    # Crear elementos...
    doc.build(elements)

def generar_excel(request, id_usuario):
    """Fábrica de documentos Excel"""
    wb = Workbook()
    # Crear hojas...
    wb.save(response)
```

### 7.3 Repository
```python
# Acceso centralizado a datos
cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id])
cursor.execute("SELECT COUNT(*) FROM usuarios")
```

---

## 8. Solución de Problemas

### Error: Can't connect to MySQL
**Solución**: Verifica que MySQL esté ejecutándose
```bash
net start mysql  # Windows
```

### Error: mysqlclient not found
**Solución**: Instala Visual C++ Build Tools o usa:
```bash
pip install PyMySQL
```

### Error: Port 8000 in use
**Solución**: Usa otro puerto
```bash
python manage.py runserver 8080
```

### Error: Static files not found
**Solución**: Verifica STATICFILES_DIRS en settings.py

---

## 📚 Archivos de Documentación

| Archivo | Descripción |
|---------|-------------|
| README.md | Documentación general del proyecto |
| Tutorial.md | Este tutorial de instalación |
| PatronesDeDiseno.md | Explicación de patrones de diseño |
| requirements.txt | Lista de dependencias |

---

## 🎨 Características del Interfaz

- ✅ Menú flotante tipo acordeón
- ✅ Diseño moderno con gradientes azules
- ✅ Iconos de Font Awesome
- ✅ Modal Bootstrap para ver usuario
- ✅ Alertas SweetAlert2
- ✅ Logo del sistema
- ✅ Diseño responsive

---

## 👨‍💻 Tecnologías

- **Django 4.2** - Framework web
- **MySQL 8.0** - Base de datos
- **ReportLab 4.2** - Gráficos en PDF
- **openpyxl 3.1** - Gráficos en Excel
- **Bootstrap 5.3** - Interfaz (local)
- **SweetAlert2** - Alertas (local)

---

**Desarrollado con Django + MySQL + ReportLab + openpyxl**
**Gráficos estilo Chart.js**