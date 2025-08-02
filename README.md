# 📄 Generador de Documentos PDF y Excel con Django

Este proyecto es una aplicación web construida con **Django** que permite generar documentos **PDF** y **Excel** a partir de datos de usuarios almacenados en una base de datos **MySQL/MariaDB**. Incluye una interfaz intuitiva para búsqueda de usuarios y generación de documentos.

---

## 🚀 Características

- 🔍 Búsqueda de usuarios por **ID**
- 🧾 Generación de PDF con:
  - Logo institucional (`escudo.png`)
  - Formato de tabla profesional
  - Estilos personalizados
- 📊 Generación de Excel con:
  - Formato profesional
  - Encabezados estilizados
  - Bordes y alineación
- ⚠️ Alertas interactivas con **SweetAlert2**
- 📱 Diseño **responsive** con **Bootstrap**

---

## 💻 Tecnologías utilizadas

- [Django 5.1](https://docs.djangoproject.com/en/5.1/)
- [Python 3.13](https://www.python.org/)
- [ReportLab](https://www.reportlab.com/) (para PDF)
- [OpenPyXL](https://openpyxl.readthedocs.io/) (para Excel)
- [MySQL / MariaDB](https://mariadb.org/)
- [Bootstrap 5.3](https://getbootstrap.com/)
- [SweetAlert2](https://sweetalert2.github.io/)

---

## 📋 Requisitos

- Python **3.13** o superior
- MariaDB **10.5** o superior
- Paquetes de Python:

```bash
pip install Django==5.1 reportlab openpyxl mysqlclient
instalacion
git clone [url-del-repositorio]
cd [nombre-del-proyecto]
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

pip install -r requirements.txt

