# Sistema de Generación de PDF y Excel - Django + MySQL

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

-- Verificar datos
SELECT * FROM usuarios;
```

## Configuración de Conexión

En `mi_proyecto/mi_proyecto/settings.py`:

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

## Instalación de Dependencias

```bash
pip install mysqlclient django reportlab openpyxl
```

## Iniciar Servidor

```bash
cd mi_proyecto
python manage.py runserver
```

## Rutas Disponibles

- **Inicio:** http://127.0.0.1:8000/
- **PDF:** http://127.0.0.1:8000/generar_pdf/<id>/
- **Excel:** http://127.0.0.1:8000/generar_excel/<id>/