# Tutorial Paso a Paso - Sistema de Generación de PDF y Excel

## 1. Instalación de MySQL

### Windows
1. Descarga MySQL Installer desde https://dev.mysql.com/downloads/installer/
2. Ejecuta el instalador y selecciona "Developer Default"
3. Configura la contraseña root
4. Completa la instalación

### Verificar instalación
```bash
mysql --version
```

## 2. Configuración de la Base de Datos

### Crear base de datos
```sql
CREATE DATABASE ejemplo;
```

### Ejecutar script SQL
```bash
mysql -u root -p ejemplo < script.sql
```

## 3. Instalación de Python y Dependencias

### Instalar Python (si no tienes)
1. Descarga Python desde https://www.python.org/downloads/
2. Durante instalación, marca "Add Python to PATH"

### Instalar dependencias
```bash
pip install django mysqlclient reportlab openpyxl
```

## 4. Configuración del Proyecto Django

### Actualizar settings.py
Edita `mi_proyecto/mi_proyecto/settings.py`:
```python
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
```

### Verificar conexión
```bash
cd mi_proyecto
python manage.py check
```

## 5. Instalación de Bootstrap Local

### Paso 1: Descargar Bootstrap
1. Ve a https://getbootstrap.com/docs/5.3/getting-started/download/
2. Descarga "Compiled CSS and JS" (no(Source))
3. Extrae los archivos

### Paso 2: Copiar archivos
- Copia `bootstrap.min.css` → `mi_proyecto/documentos/static/css/`
- Copia `bootstrap.bundle.min.js` → `mi_proyecto/documentos/static/js/`

### Paso 3: Verificar estructura
```
static/
├── css/
│   └── bootstrap.min.css
└── js/
    └── bootstrap.bundle.min.js
```

## 6. Instalación de SweetAlert2 Local

### Paso 1: Descargar SweetAlert2
1. Ve a https://sweetalert2.github.io/#download
2. Descarga la versión "zip"

### Paso 2: Copiar archivos
- Copia `sweetalert2.min.js` → `mi_proyecto/documentos/static/js/`
- Copia `sweetalert2.min.css` → `mi_proyecto/documentos/static/css/`

### Paso 3: Verificar estructura
```
static/
├── css/
│   ├── bootstrap.min.css
│   └── sweetalert2.min.css
└── js/
    ├── bootstrap.bundle.min.js
    └── sweetalert2.min.js
```

## 7. Instalación de Fuentes Google Local

### Opción 1: Descargar fuentes (recomendado)

1. Ve a Google Fonts (fonts.google.com)
2. Selecciona las fuentes deseadas (ej: Roboto, Open Sans)
3. Descarga los archivos WOFF2

### Opción 2: Usar fuentes del sistema

Edita el CSS:
```css
/* Usar fuentes del sistema como alternativa */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
```

### Paso a paso descargar fuentes Roboto:

1. Ve a https://fonts.google.com/specimen/Roboto
2. Descarga los archivos TTF
3. Convierte a WOFF2 usando https://transfonter.org/
4. Copia a `mi_proyecto/documentos/static/fonts/`

### Estructura final fonts
```
static/
├── fonts/
│   ├── Roboto-Regular.woff2
│   ├── Roboto-Bold.woff2
│   └── Roboto-Medium.woff2
```

## 8. Agregar Logo/Imagen

### Paso 1: Colocar imagen
Copia tu imagen (logo.png) en:
```
static/
└── images/
    └── logo.png
```

### Paso 2: Actualizar HTML
```html
<img src="{% static 'images/logo.png' %}" alt="Logo" width="150">
```

## 9. Ejecutar el Proyecto

### Iniciar servidor
```bash
cd mi_proyecto
python manage.py runserver
```

### Acceder
- Navegador: http://127.0.0.1:8000/

## 10. Solución de Problemas

### Error de conexión MySQL
```
Error 2003: Can't connect to MySQL server
```
**Solución:** Verifica que MySQL esté ejecutándose como servicio.

### Error de mysqlclient
```
OSError: mysqlclient not found
```
**Solución:**
```bash
pip install mysqlclient
# En Windows, necesitas Visual C++ Build Tools
```

### Error de puertos
```
Port 8000 in use
```
**Solución:** Usa otro puerto
```bash
python manage.py runserver 8080
```

## 11. Generar PDF con Estadísticas

El PDF ahora incluye gráficos estadísticos usando ReportLab:
- Gráfico de barras de usuarios por mes
- Tabla de resumen de estadísticas

## 12. Generar Excel con Gráficos

El Excel incluye:
- Datos organizados en tablas
- Estilos profesionales con bordes y colores
- Encabezados formateados