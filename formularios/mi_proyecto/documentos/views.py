# Importaciones de Django
from django.shortcuts import render  # Para renderizar plantillas HTML
from django.http import HttpResponse, JsonResponse  # Para respuestas HTTP y JSON
from django.db import connection  # Para conexiones a base de datos

# Importaciones para PDF (ReportLab)
from reportlab.lib.pagesizes import letter  # Tamaño de página
from reportlab.pdfgen import canvas  # Generador de PDF
from reportlab.lib import colors  # Colores para PDF
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Estilos de texto
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer  # Elementos PDF
from reportlab.lib.units import inch  # Unidades de medida

# Importaciones del sistema y utilidades
import os  # Operaciones con el sistema de archivos
from django.conf import settings  # Configuraciones de Django
from datetime import datetime  # Manejo de fechas

# Importaciones para Excel
from openpyxl import Workbook  # Crear archivos Excel
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side  # Estilos Excel

def index(request):
    """
    Vista principal que maneja la búsqueda de usuarios y muestra sus datos.
    
    Args:
        request: Objeto HttpRequest que contiene los datos de la petición
    
    Returns:
        HttpResponse: Renderiza la plantilla index.html con los datos del usuario
    """
    usuario = None
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        if id_usuario:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
                columns = [col[0] for col in cursor.description]
                row = cursor.fetchone()
                if row:
                    usuario = dict(zip(columns, row))
                    return render(request, 'documentos/index.html', {'usuario': usuario})
                else:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
                    return render(request, 'documentos/index.html', {'error': 'Usuario no encontrado'})
    
    return render(request, 'documentos/index.html', {'usuario': usuario})

def generar_pdf(request, id_usuario):
    """
    Genera PDF con datos del usuario:
    1. Verifica el ID del usuario
    2. Consulta la base de datos
    3. Configura el documento PDF
    4. Agrega imagen del escudo
    5. Define estilos y formato
    6. Crea tabla con datos
    7. Construye y retorna el PDF
    """
    if not id_usuario:
        return HttpResponse("ID de usuario no proporcionado", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            usuario = dict(zip(columns, row))
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.pdf"'

            doc = SimpleDocTemplate(
                response,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            elements = []

            # Ruta correcta para el escudo
            img_path = os.path.join(settings.BASE_DIR, 'documentos', 'templates', 'documentos', 'escudo.png')
            if os.path.exists(img_path):
                img = Image(img_path)
                img.drawHeight = 1.5*inch
                img.drawWidth = 1.5*inch
                elements.append(img)

            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                alignment=1,
                spaceAfter=30
            )

            # Título
            elements.append(Paragraph("Información del Usuario", title_style))
            elements.append(Spacer(1, 12))

            # Datos para la tabla
            data = [
                ['Campo', 'Información'],
                ['ID', str(usuario['id'])],
                ['Nombre', usuario['nombre']],
                ['Correo', usuario['correo']],
                ['Teléfono', usuario['telefono']],
                ['Dirección', usuario['direccion']],
                ['Fecha de Creación', str(usuario['fecha_creacion'])]
            ]

            # Crear tabla
            table = Table(data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))

            elements.append(table)
            
            # Construir PDF
            doc.build(elements)
            
            return response
    return HttpResponse("Usuario no encontrado", status=404)

def generar_excel(request, id_usuario):
    """
    Genera Excel con datos del usuario:
    1. Verifica el ID del usuario
    2. Consulta la base de datos
    3. Crea nuevo libro Excel
    4. Define estilos:
       - Fuentes para encabezados
       - Colores de fondo
       - Bordes
       - Alineación
    5. Escribe datos en celdas
    6. Aplica estilos
    7. Configura anchos de columna
    8. Genera respuesta HTTP
    9. Guarda y retorna el archivo
    """
    if not id_usuario:
        return HttpResponse("ID de usuario no proporcionado", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            usuario = dict(zip(columns, row))
            
            # Crear un nuevo libro de trabajo Excel
            wb = Workbook()
            ws = wb.active
            ws.title = f"Usuario {id_usuario}"

            # Estilos
            # Configura fuente en blanco y negrita para encabezados
            header_font = Font(bold=True, color="FFFFFF")
            # Fondo azul para encabezados
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            # Define bordes finos para todas las celdas
            border = Border(
                left=Side(style='thin'), 
                right=Side(style='thin'), 
                top=Side(style='thin'), 
                bottom=Side(style='thin')
            )

            # Datos para el Excel
            data = [
                ['Campo', 'Información'],
                ['ID', str(usuario['id'])],
                ['Nombre', usuario['nombre']],
                ['Correo', usuario['correo']],
                ['Teléfono', usuario['telefono']],
                ['Dirección', usuario['direccion']],
                ['Fecha de Creación', str(usuario['fecha_creacion'])]
            ]

            # Escribir datos y aplicar estilos
            for row_idx, row_data in enumerate(data, 1):
                for col_idx, value in enumerate(row_data, 1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = border
                    cell.alignment = Alignment(horizontal='left')
                    
                    if row_idx == 1:  # Encabezados
                        cell.font = header_font
                        cell.fill = header_fill

            # Ajustar ancho de columnas
            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 40

            # Ajusta ancho de columnas para mejor lectura
            ws.column_dimensions['A'].width = 20  # Columna de campos
            ws.column_dimensions['B'].width = 40  # Columna de información

            # Crear respuesta HTTP
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}_{datetime.now().strftime("%Y%m%d")}.xlsx"'

            # Guardar el archivo
            wb.save(response)
            
            return response
            
    return HttpResponse("Usuario no encontrado", status=404)

