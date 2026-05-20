"""
=======================================================
SISTEMA DE GENERACIÓN DE PDF Y EXCEL - DJANGO + MySQL
=======================================================

Este módulo contiene las vistas del sistema de gestión de usuarios.
Proporciona funcionalidades para buscar usuarios, generar reportes
en PDF y Excel con gráficos estadísticos.

Patrones de Diseño Utilizados:
- MVC (Model-View-Controller) - Estructura de Django
- Patrón de Servicio - Lógica de negocio encapsulada
- Factory Method - Creación de documentos PDF/Excel
- Repository - Acceso a datos mediante cursor

Autor: Sistema de Gestión
Fecha: 2026
Versión: 1.0
=======================================================
"""

# Importaciones de Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection

# Importaciones para PDF (ReportLab)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String, Circle, Rect, Line
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader

# Importaciones del sistema y utilidades
import os
from django.conf import settings
from datetime import datetime

# Importaciones para Excel
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage


def index(request):
    """
    Vista principal que maneja la búsqueda de usuarios y muestra sus datos.
    Implementa el patrón MVC de Django.
    
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
    Genera PDF con datos del usuario incluyendo gráficos de barras y torta.
    Implementa el patrón Factory Method para la creación de documentos.
    
    Args:
        request: Objeto HttpRequest
        id_usuario: ID del usuario a generar informe
    
    Returns:
        HttpResponse: Archivo PDF con gráficos estadísticos
    """
    if not id_usuario:
        return HttpResponse("ID de usuario no proporcionado", status=400)

    with connection.cursor() as cursor:
        # Obtener datos del usuario
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        # Obtener estadísticas globales
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        # Distribución por mes
        cursor.execute("""
            SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cantidad 
            FROM usuarios 
            GROUP BY DATE_FORMAT(fecha_creacion, '%%Y-%%m')
            ORDER BY mes
        """)
        usuarios_mes = cursor.fetchall()
        
        # Distribución por primera letra del nombre
        cursor.execute("""
            SELECT LEFT(nombre, 1) as inicial, COUNT(*) as cantidad 
            FROM usuarios 
            WHERE nombre IS NOT NULL
            GROUP BY LEFT(nombre, 1)
            ORDER BY cantidad DESC
        """)
        usuarios_inicial = cursor.fetchall()
        
        if row:
            usuario = dict(zip(columns, row))
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.pdf"'

            doc = SimpleDocTemplate(
                response,
                pagesize=letter,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                alignment=1,
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=20
            )
            
            subtitle_style = ParagraphStyle(
                'SubTitle',
                parent=styles['Normal'],
                alignment=1,
                fontSize=12,
                textColor=colors.HexColor('#7f8c8d'),
                spaceAfter=30
            )
            
            section_style = ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#3498db'),
                spaceBefore=20,
                spaceAfter=10
            )

            # Logo
            logo_path = os.path.join(settings.BASE_DIR, 'documentos', 'static', 'images', 'logo.svg')
            if os.path.exists(logo_path):
                try:
                    img = Image(logo_path, width=1.5*inch, height=1.5*inch)
                    img.hAlign = 'CENTER'
                    elements.append(img)
                except:
                    pass

            elements.append(Paragraph("INFORME DETALLADO DE USUARIO", title_style))
            elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))

            # Datos del usuario
            elements.append(Paragraph("DATOS DEL USUARIO", section_style))
            
            data = [
                ['Campo', 'Información'],
                ['ID', str(usuario['id'])],
                ['Nombre', str(usuario['nombre'])],
                ['Correo', str(usuario['correo'])],
                ['Teléfono', str(usuario['telefono'] or 'N/A')],
                ['Dirección', str(usuario['direccion'] or 'N/A')],
                ['Fecha de Creación', str(usuario['fecha_creacion'])]
            ]

            table = Table(data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(table)

            # Estadísticas
            elements.append(Paragraph("ESTADÍSTICAS DEL SISTEMA", section_style))
            
            stats_data = [
                ['Métrica', 'Valor', 'Porcentaje'],
                ['Total de Usuarios', str(total_usuarios), '100%'],
                ['Usuario ID', str(usuario['id']), f'{(1/total_usuarios)*100:.2f}%'],
                ['Registros por Mes', str(len(usuarios_mes)), f'{(len(usuarios_mes)/total_usuarios)*100:.1f}%'],
            ]
            
            stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f8f5')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#27ae60')),
            ]))
            elements.append(stats_table)

            # Gráfico de Barras
            if usuarios_mes:
                elements.append(Paragraph("GRÁFICO DE BARRAS - USUARIOS POR MES", section_style))
                
                chart_data = [['Mes', 'Cantidad']]
                max_val = 0
                for mes, cantidad in usuarios_mes[:12]:
                    chart_data.append([str(mes), cantidad])
                    if cantidad > max_val:
                        max_val = cantidad
                
                # Crear gráfico de barras usando tabla visual
                bar_table = Table(chart_data, colWidths=[1.5*inch, 3*inch])
                bar_styles = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                ]
                
                for i, (_, cantidad) in enumerate(usuarios_mes[:12], 1):
                    bar_width = (cantidad / max_val) * 2.5 if max_val > 0 else 0
                    bar_styles.append(('BACKGROUND', (1, i), (1, i), colors.HexColor('#3498db')))
                    bar_styles.append(('BOX', (1, i), (1, i), 1, colors.HexColor('#2980b9')))
                
                bar_table.setStyle(TableStyle(bar_styles))
                elements.append(bar_table)

            # Gráfico de Torta (Distribución por inicial)
            if usuarios_inicial:
                elements.append(Paragraph("GRÁFICO DE TORTA - DISTRIBUCIÓN POR INICIAL", section_style))
                
                # Colores para torta
                colores_torta = ['#e74c3c', '#3498db', '#27ae60', '#f39c12', '#9b59b6', 
                                '#1abc9c', '#e67e22', '#34495e', '#16a085', '#2c3e50']
                
                torta_data = [['Inicial', 'Cantidad', 'Porcentaje']]
                total_inicial = sum(cant for _, cant in usuarios_inicial)
                
                for i, (inicial, cantidad) in enumerate(usuarios_inicial[:10]):
                    porcentaje = (cantidad / total_inicial) * 100 if total_inicial > 0 else 0
                    color = colores_torta[i % len(colores_torta)]
                    torta_data.append([inicial or '?', str(cantidad), f'{porcentaje:.1f}%'])
                
                torta_table = Table(torta_data, colWidths=[1*inch, 1.5*inch, 1.5*inch])
                torta_styles = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                ]
                
                for i in range(len(usuarios_inicial[:10])):
                    color = colores_torta[i % len(colores_torta)]
                    torta_styles.append(('BACKGROUND', (0, i+1), (-1, i+1), colors.HexColor(color + '20')))
                    torta_styles.append(('TEXTCOLOR', (0, i+1), (0, i+1), colors.HexColor(color)))
                    torta_styles.append(('FONTNAME', (0, i+1), (0, i+1), 'Helvetica-Bold'))
                
                torta_table.setStyle(TableStyle(torta_styles))
                elements.append(torta_table)

            # Leyenda del gráfico de torta
            elements.append(Paragraph("LEYENDA DE COLORES", section_style))
            leyenda_data = [['Color', 'Significado']]
            for i, (inicial, cantidad) in enumerate(usuarios_inicial[:10]):
                color = colores_torta[i % len(colores_torta)]
                leyenda_data.append([f'■ Inicial "{inicial}"', f'{cantidad} usuarios'])
            
            leyenda_table = Table(leyenda_data, colWidths=[2*inch, 3*inch])
            leyenda_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ]))
            elements.append(leyenda_table)

            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                alignment=1,
                fontSize=10,
                textColor=colors.HexColor('#95a5a6'),
                spaceBefore=30
            )
            elements.append(Paragraph("Sistema de Generación de PDF y Excel - Django + MySQL", footer_style))
            
            doc.build(elements)
            return response
    return HttpResponse("Usuario no encontrado", status=404)


def generar_pdf_todos(request):
    """
    Genera PDF con todos los usuarios del sistema.
    Incluye gráficos de barras y torta a nivel global.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios ORDER BY id")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        usuarios = [dict(zip(columns, row)) for row in rows]
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cantidad 
            FROM usuarios GROUP BY DATE_FORMAT(fecha_creacion, '%%Y-%%m') ORDER BY mes
        """)
        usuarios_mes = cursor.fetchall()

    if not usuarios:
        return HttpResponse("No hay usuarios", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_todos_usuarios.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=1, fontSize=24, textColor=colors.HexColor('#2c3e50'), spaceAfter=20)
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], alignment=1, fontSize=12, textColor=colors.HexColor('#7f8c8d'), spaceAfter=20)
    section_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#3498db'), spaceBefore=15, spaceAfter=10)

    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'documentos', 'static', 'images', 'logo.svg')
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=1*inch, height=1*inch)
            img.hAlign = 'CENTER'
            elements.append(img)
        except:
            pass

    elements.append(Paragraph("REPORTE GENERAL DE USUARIOS", title_style))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total: {total} usuarios", subtitle_style))

    # Listado
    elements.append(Paragraph("LISTADO COMPLETO DE USUARIOS", section_style))

    data = [['ID', 'Nombre', 'Correo', 'Teléfono', 'Fecha']]
    for u in usuarios:
        data.append([str(u['id']), str(u['nombre'] or '')[:25], str(u['correo'] or '')[:30], str(u['telefono'] or ''), str(u['fecha_creacion'])[:10]])

    table = Table(data, colWidths=[0.5*inch, 1.5*inch, 2*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(table)

    # Gráfico de barras
    if usuarios_mes:
        elements.append(Paragraph("ESTADÍSTICAS - USUARIOS POR MES", section_style))
        chart_data = [['Mes', 'Cantidad']]
        for mes, cantidad in usuarios_mes[:12]:
            chart_data.append([str(mes), cantidad])
        
        bar_table = Table(chart_data, colWidths=[1.5*inch, 3*inch])
        bar_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#3498db')),
        ]))
        elements.append(bar_table)

    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.HexColor('#95a5a6'), spaceBefore=20)
    elements.append(Paragraph("Sistema de Generación - Django + MySQL + ReportLab", footer_style))

    doc.build(elements)
    return response


def generar_excel(request, id_usuario):
    """
    Genera Excel con datos del usuario incluyendo gráficos de barras y torta.
    Implementa múltiples hojas: Datos, Estadísticas, Gráficos.
    """
    if not id_usuario:
        return HttpResponse("ID de usuario no proporcionado", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cantidad 
            FROM usuarios GROUP BY DATE_FORMAT(fecha_creacion, '%%Y-%%m') ORDER BY mes
        """)
        usuarios_mes = cursor.fetchall()
        
        cursor.execute("""
            SELECT LEFT(nombre, 1) as inicial, COUNT(*) as cantidad 
            FROM usuarios WHERE nombre IS NOT NULL
            GROUP BY LEFT(nombre, 1) ORDER BY cantidad DESC
        """)
        usuarios_inicial = cursor.fetchall()
        
        if row:
            usuario = dict(zip(columns, row))
            
            wb = Workbook()
            
            # Hoja 1: Datos del usuario
            ws_datos = wb.active
            ws_datos.title = "Datos del Usuario"

            header_font = Font(bold=True, color="FFFFFF", size=12)
            header_fill = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")
            border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
            
            title_font = Font(bold=True, size=16, color="2c3e50")
            ws_datos.merge_cells('A1:B1')
            ws_datos['A1'] = f"Informe de Usuario - ID: {id_usuario}"
            ws_datos['A1'].font = title_font
            ws_datos['A1'].alignment = Alignment(horizontal='center')
            ws_datos.row_dimensions[1].height = 25

            ws_datos.merge_cells('A2:B2')
            ws_datos['A2'] = f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ws_datos['A2'].font = Font(size=10, color="7f8c8d")
            ws_datos['A2'].alignment = Alignment(horizontal='center')

            data = [
                ['Campo', 'Información'],
                ['ID', str(usuario['id'])],
                ['Nombre', str(usuario['nombre'])],
                ['Correo', str(usuario['correo'])],
                ['Teléfono', str(usuario['telefono'] or 'N/A')],
                ['Dirección', str(usuario['direccion'] or 'N/A')],
                ['Fecha de Creación', str(usuario['fecha_creacion'])]
            ]

            for row_idx, row_data in enumerate(data, 4):
                for col_idx, value in enumerate(row_data, 1):
                    cell = ws_datos.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = border
                    cell.alignment = Alignment(horizontal='left')
                    
                    if row_idx == 4:
                        cell.font = header_font
                        cell.fill = header_fill
                    else:
                        cell.font = Font(size=11)
                        cell.fill = PatternFill(start_color="ecf0f1", end_color="ecf0f1", fill_type="solid")

            ws_datos.column_dimensions['A'].width = 25
            ws_datos.column_dimensions['B'].width = 45

            # Hoja 2: Estadísticas
            ws_stats = wb.create_sheet("Estadísticas")
            
            ws_stats.merge_cells('A1:D1')
            ws_stats['A1'] = "ESTADÍSTICAS DEL SISTEMA"
            ws_stats['A1'].font = Font(bold=True, size=16, color="ffffff")
            ws_stats['A1'].fill = PatternFill(start_color="27ae60", end_color="27ae60", fill_type="solid")
            ws_stats['A1'].alignment = Alignment(horizontal='center')
            ws_stats.row_dimensions[1].height = 25

            stats_data = [
                ['Métrica', 'Valor', 'Descripción', 'Porcentaje'],
                ['Total de Usuarios', str(total_usuarios), 'Registrados', '100%'],
                ['Usuario ID', str(usuario['id']), f'Usuario específico', f'{(1/total_usuarios)*100:.2f}%'],
                ['Meses con registros', str(len(usuarios_mes)), 'Meses activos', '-'],
            ]

            for row_idx, row_data in enumerate(stats_data, 3):
                for col_idx, value in enumerate(row_data, 1):
                    cell = ws_stats.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = border
                    
                    if row_idx == 3:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.alignment = Alignment(horizontal='center')
                    else:
                        if col_idx == 1:
                            cell.font = Font(bold=True, color="2c3e50")
                        cell.fill = PatternFill(start_color="e8f8f5", end_color="e8f8f5", fill_type="solid")

            ws_stats.column_dimensions['A'].width = 25
            ws_stats.column_dimensions['B'].width = 15
            ws_stats.column_dimensions['C'].width = 30
            ws_stats.column_dimensions['D'].width = 15

            # Hoja 3: Gráfico de Barras
            if usuarios_mes:
                ws_barras = wb.create_sheet("Gráfico Barras")
                
                ws_barras.merge_cells('A1:C1')
                ws_barras['A1'] = "GRÁFICO DE BARRAS - USUARIOS POR MES"
                ws_barras['A1'].font = Font(bold=True, size=14, color="ffffff")
                ws_barras['A1'].fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")
                ws_barras['A1'].alignment = Alignment(horizontal='center')

                chart_data = [['Mes', 'Cantidad']]
                for mes, cantidad in usuarios_mes[:12]:
                    chart_data.append([str(mes), cantidad])

                for row_idx, row_data in enumerate(chart_data, 3):
                    for col_idx, value in enumerate(row_data, 1):
                        cell = ws_barras.cell(row=row_idx, column=col_idx, value=value)
                        cell.border = border
                        
                        if row_idx == 3:
                            cell.font = header_font
                            cell.fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")
                        elif row_idx > 3 and col_idx == 2:
                            cell.fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")

                ws_barras.column_dimensions['A'].width = 20
                ws_barras.column_dimensions['B'].width = 15

                # Agregar gráfico de barras
                chart = BarChart()
                chart.type = "col"
                chart.style = 10
                chart.title = "Usuarios por Mes"
                chart.y_axis.title = 'Cantidad'
                chart.x_axis.title = 'Mes'

                data_ref = Reference(ws_barras, min_col=2, min_row=3, max_row=3+len(usuarios_mes[:12]))
                cats_ref = Reference(ws_barras, min_col=1, min_row=4, max_row=3+len(usuarios_mes[:12]))
                chart.add_data(data_ref, titles_from_data=True)
                chart.set_categories(cats_ref)
                chart.height = 12
                chart.width = 20

                ws_barras.add_chart(chart, "E3")

            # Hoja 4: Gráfico de Torta
            if usuarios_inicial:
                ws_torta = wb.create_sheet("Gráfico Torta")
                
                ws_torta.merge_cells('A1:C1')
                ws_torta['A1'] = "GRÁFICO DE TORTA - DISTRIBUCIÓN POR INICIAL"
                ws_torta['A1'].font = Font(bold=True, size=14, color="ffffff")
                ws_torta['A1'].fill = PatternFill(start_color="9b59b6", end_color="9b59b6", fill_type="solid")
                ws_torta['A1'].alignment = Alignment(horizontal='center')

                total_inicial = sum(cant for _, cant in usuarios_inicial)
                torta_data = [['Inicial', 'Cantidad', 'Porcentaje']]
                colores = ['e74c3c', '3498db', '27ae60', 'f39c12', '9b59b6', '1abc9c', 'e67e22', '34495e', '16a085', '2c3e50']
                
                for i, (inicial, cantidad) in enumerate(usuarios_inicial[:10]):
                    porcentaje = (cantidad / total_inicial) * 100 if total_inicial > 0 else 0
                    torta_data.append([inicial or '?', cantidad, f'{porcentaje:.1f}%'])

                for row_idx, row_data in enumerate(torta_data, 3):
                    for col_idx, value in enumerate(row_data, 1):
                        cell = ws_torta.cell(row=row_idx, column=col_idx, value=value)
                        cell.border = border
                        
                        if row_idx == 3:
                            cell.font = header_font
                            cell.fill = PatternFill(start_color="9b59b6", end_color="9b59b6", fill_type="solid")
                        elif row_idx > 3:
                            color = colores[(row_idx - 4) % len(colores)]
                            cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
                            cell.font = Font(color="ffffff", bold=True)

                ws_torta.column_dimensions['A'].width = 15
                ws_torta.column_dimensions['B'].width = 15
                ws_torta.column_dimensions['C'].width = 15

                # Agregar gráfico de torta
                pie = PieChart()
                pie.title = "Distribución por Inicial"
                
                data_ref = Reference(ws_torta, min_col=2, min_row=3, max_row=3+len(usuarios_inicial[:10]))
                cats_ref = Reference(ws_torta, min_col=1, min_row=4, max_row=3+len(usuarios_inicial[:10]))
                pie.add_data(data_ref, titles_from_data=True)
                pie.set_categories(cats_ref)
                pie.height = 12
                pie.width = 20

                ws_torta.add_chart(pie, "E3")

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}_{datetime.now().strftime("%Y%m%d")}.xlsx"'

            wb.save(response)
            return response
            
    return HttpResponse("Usuario no encontrado", status=404)


def generar_excel_todos(request):
    """Genera Excel con todos los usuarios del sistema."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios ORDER BY id")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        usuarios = [dict(zip(columns, row)) for row in rows]
        
        cursor.execute("""
            SELECT DATE_FORMAT(fecha_creacion, '%%Y-%%m') as mes, COUNT(*) as cantidad 
            FROM usuarios GROUP BY DATE_FORMAT(fecha_creacion, '%%Y-%%m') ORDER BY mes
        """)
        usuarios_mes = cursor.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    ws.merge_cells('A1:F1')
    ws['A1'] = f"REPORTE GENERAL - Total: {len(usuarios)} usuarios"
    ws['A1'].font = Font(bold=True, size=14, color="2c3e50")
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.row_dimensions[1].height = 20

    headers = ['ID', 'Nombre', 'Correo', 'Teléfono', 'Dirección', 'Fecha Creación']
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border
        cell.alignment = Alignment(horizontal='center')

    for row_idx, usuario in enumerate(usuarios, 4):
        ws.cell(row=row_idx, column=1, value=usuario['id']).border = border
        ws.cell(row=row_idx, column=2, value=usuario['nombre']).border = border
        ws.cell(row=row_idx, column=3, value=usuario['correo']).border = border
        ws.cell(row=row_idx, column=4, value=usuario['telefono'] or 'N/A').border = border
        ws.cell(row=row_idx, column=5, value=usuario['direccion'] or 'N/A').border = border
        ws.cell(row=row_idx, column=6, value=str(usuario['fecha_creacion'])[:19]).border = border

    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 35
    ws.column_dimensions['F'].width = 20

    # Gráfico
    if usuarios_mes:
        ws_grafico = wb.create_sheet("Estadísticas")
        ws_grafico['A1'] = "Gráfico de Usuarios por Mes"
        ws_grafico['A1'].font = Font(bold=True, size=14)
        
        chart_data = [['Mes', 'Cantidad']]
        for mes, cantidad in usuarios_mes[:12]:
            chart_data.append([str(mes), cantidad])
        
        for row_idx, row_data in enumerate(chart_data, 3):
            for col_idx, value in enumerate(row_data, 1):
                ws_grafico.cell(row=row_idx, column=col_idx, value=value)

        chart = BarChart()
        chart.title = "Usuarios por Mes"
        data_ref = Reference(ws_grafico, min_col=2, min_row=3, max_row=3+len(usuarios_mes[:12]))
        cats_ref = Reference(ws_grafico, min_col=1, min_row=4, max_row=3+len(usuarios_mes[:12]))
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        ws_grafico.add_chart(chart, "D3")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="reporte_todos_usuarios_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    wb.save(response)
    return response


def listar_usuarios(request):
    """Vista para listar todos los usuarios."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios ORDER BY id")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        usuarios = [dict(zip(columns, row)) for row in rows]
    
    return render(request, 'documentos/lista.html', {'usuarios': usuarios})