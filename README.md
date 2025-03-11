Este proyecto es una aplicación Django que permite generar documentos PDF y Excel a partir de datos de usuarios almacenados en una base de datos MySQL. La aplicación incluye una interfaz web para buscar usuarios y generar los documentos correspondientes.

Características 🚀
Búsqueda de usuarios por ID
Generación de PDF con:
Logo institucional
Formato de tabla profesional
Estilos personalizados
Generación de Excel con:
Formato profesional
Encabezados estilizados
Bordes y alineación
Alertas interactivas con SweetAlert2
Diseño responsive con Bootstrap
Tecnologías utilizadas 💻
Django 5.1
Python 3.13
ReportLab (PDF)
OpenPyXL (Excel)
MySQL/MariaDB
Bootstrap 5.3
SweetAlert2
Requisitos 📋
Python 3.13 o superior
MariaDB 10.5 o superior

Django==5.1
reportlab
openpyxl
mysqlclient

git clone [url-del-repositorio]



c/
├── documentos/
│   ├── templates/
│   │   └── documentos/
│   │       ├── index.html
│   │       └── escudo.png
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   └── models.py
└── mi_proyecto/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
