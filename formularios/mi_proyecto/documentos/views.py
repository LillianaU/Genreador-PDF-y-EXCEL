"""
=======================================================
SISTEMA DE GENERACIÓN DE PDF Y EXCEL - DJANGO ORM
=======================================================

Este módulo contiene las vistas del sistema de gestión de usuarios.
Utiliza Django ORM para todas las operaciones de base de datos.

PATRONES DE DISEÑO UTILIZADOS:
=============================

1. MVC (Model-View-Controller) - Estructura de Django
   - Model: models.py (Usuario)
   - View: Templates HTML
   - Controller: Funciones de views.py

2. FACTORY METHOD
   - generar_pdf(): creación de documentos PDF
   - generar_excel(): creación de documentos Excel

3. REPOSITORY PATTERN
   - Abstracción mediante Django ORM
   - Métodos: get(), filter(), aggregate()

4. SERVICE LAYER
   - Lógica de negocio encapsulada en funciones

5. TEMPLATE METHOD
   - Estructura fija para documentos
"""

from django.shortcuts import render
from .models import Usuario
from django.http import HttpResponse
from django.db.models import Count
from django.db import connection
from django.utils import timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String, Circle, Line, Wedge, Rect
from reportlab.lib.colors import HexColor

import os
from django.conf import settings
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, PieChart, Reference, ScatterChart, Series


def index(request):
    """Vista principal - Búsqueda de usuarios por ID o nombre"""
    usuario = None
    usuarios_encontrados = None
    
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        if id_usuario:
            try:
                usuario = Usuario.objects.get(id=int(id_usuario))
                return render(request, 'documentos/index.html', {'usuario': usuario, 'mostrar_modal': True})
            except Usuario.DoesNotExist:
                return render(request, 'documentos/index.html', {'error': 'Usuario no encontrado'})
        
        nombre_busqueda = request.POST.get('nombre_busqueda')
        if nombre_busqueda:
            usuarios_encontrados = Usuario.objects.filter(nombre__icontains=nombre_busqueda)
            if usuarios_encontrados.count() == 1:
                usuario = usuarios_encontrados.first()
                return render(request, 'documentos/index.html', {'usuario': usuario})
            elif usuarios_encontrados.exists():
                return render(request, 'documentos/index.html', 
                           {'usuarios_encontrados': usuarios_encontrados, 'busqueda_nombre': nombre_busqueda})
            else:
                return render(request, 'documentos/index.html', {'error': 'No se encontraron usuarios con ese nombre'})
    
    return render(request, 'documentos/index.html', {'usuario': usuario})


def lista_usuarios(request):
    """Vista para listar todos los usuarios"""
    usuarios = Usuario.objects.all().order_by('-id')
    return render(request, 'documentos/lista.html', {'usuarios': usuarios})


def generar_pdf(request, id_usuario):
    """Genera PDF con gráficos estilo Chart.js"""
    try:
        usuario = Usuario.objects.get(id=id_usuario)
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)
    
    total_usuarios = Usuario.objects.count()
    
    usuarios_mes = Usuario.objects.extra(
        select={'mes': "DATE_FORMAT(fecha_creacion, '%%Y-%%m')"}
    ).values('mes').annotate(cantidad=Count('id')).order_by('mes')
    
    usuarios_inicial = Usuario.objects.extra(
        select={'inicial': "LEFT(nombre, 1)"}
    ).values('inicial').annotate(cantidad=Count('id')).order_by('-cantidad')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=1, fontSize=24, textColor=colors.HexColor('#2c3e50'), spaceAfter=20)
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], alignment=1, fontSize=12, textColor=colors.HexColor('#7f8c8d'), spaceAfter=30)
    section_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#3498db'), spaceBefore=20, spaceAfter=10)
    
    logo_path = os.path.join(settings.BASE_DIR, 'documentos', 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=1*inch, height=1*inch)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 10))
        except Exception as e:
            print(f"Error con logo: {e}")

    elements.append(Paragraph("INFORME DETALLADO DE USUARIO", title_style))
    elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))

    elements.append(Paragraph("DATOS DEL USUARIO", section_style))
    data = [
        ['Campo', 'Información'],
        ['ID', str(usuario.id)],
        ['Nombre', str(usuario.nombre)],
        ['Correo', str(usuario.correo)],
        ['Teléfono', str(usuario.telefono or 'N/A')],
        ['Dirección', str(usuario.direccion or 'N/A')],
        ['Fecha de Creación', str(usuario.fecha_creacion)]
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
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
    ]))
    elements.append(table)

    elements.append(Paragraph("ESTADÍSTICAS DEL SISTEMA", section_style))
    stats_data = [
        ['Métrica', 'Valor', 'Porcentaje'],
        ['Total de Usuarios', str(total_usuarios), '100%'],
        ['Usuario ID', str(usuario.id), f'{(1/total_usuarios)*100:.2f}%'],
    ]
    stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f8f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#27ae60')),
    ]))
    elements.append(stats_table)

    if usuarios_mes:
        elements.append(Paragraph("📊 GRÁFICO DE BARRAS - USUARIOS POR MES", section_style))
        drawing = Drawing(400, 200)
        datos_mes = [(u['mes'], u['cantidad']) for u in usuarios_mes[:10]]
        max_val = max(cant for _, cant in datos_mes) if datos_mes else 1
        
        colores_barras = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        for i, (mes, cantidad) in enumerate(datos_mes):
            bar_height = (cantidad / max_val) * 120
            x = 50 + i * 30
            rect = Rect(x, 30, 20, bar_height)
            rect.fillColor = HexColor(colores_barras[i % len(colores_barras)])
            drawing.add(rect)
            
            label = String(x + 10, 15, str(mes)[-2:] if mes else '')
            label.fontSize = 7
            label.textAnchor = 'middle'
            drawing.add(label)
        elements.append(drawing)
        elements.append(Spacer(1, 15))

    if usuarios_inicial:
        elements.append(Paragraph("🥧 GRÁFICO DE TORTA - DISTRIBUCIÓN POR INICIAL", section_style))
        drawing_torta = Drawing(200, 200)
        datos_inicial = [(u['inicial'], u['cantidad']) for u in usuarios_inicial[:10]]
        total_inicial = sum(cant for _, cant in datos_inicial)
        
        colores_torta = ['#667eea', '#f5576c', '#43e97b', '#fa709a', '#fee140']
        angle = 0
        for i, (inicial, cantidad) in enumerate(datos_inicial):
            if total_inicial > 0:
                span = (cantidad / total_inicial) * 360
                wedge = Wedge(100, 100, 80, angle, angle + span - 1)
                wedge.fillColor = HexColor(colores_torta[i % len(colores_torta)])
                drawing_torta.add(wedge)
                angle += span
        elements.append(drawing_torta)
        elements.append(Spacer(1, 15))

    elements.append(Paragraph("⚡ GRÁFICO DE DISPERSIÓN", section_style))
    usuarios_disp = Usuario.objects.all()[:15]
    drawing_disp = Drawing(350, 200)
    
    line_x = Line(40, 30, 40, 170)
    line_x.strokeColor = HexColor('#bdc3c7')
    drawing_disp.add(line_x)
    line_y = Line(40, 170, 320, 170)
    line_y.strokeColor = HexColor('#bdc3c7')
    drawing_disp.add(line_y)
    
    colores_disp = ['#667eea', '#f5576c', '#43e97b', '#fa709a', '#fee140']
    for i, u in enumerate(usuarios_disp):
        x = 40 + (len(u.nombre) or 1) * 8
        y = 30 + (len(u.correo) or 1) * 3
        if x > 310: x = 310
        if y > 165: y = 165
        
        circle = Circle(x, y, 6)
        circle.fillColor = HexColor(colores_disp[i % len(colores_disp)])
        drawing_disp.add(circle)
    elements.append(drawing_disp)

    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.HexColor('#95a5a6'), spaceBefore=30)
    elements.append(Paragraph("Sistema de Generación de PDF y Excel - Django ORM + MySQL", footer_style))
    
    doc.build(elements)
    return response


def generar_pdf_todos(request):
    """Genera PDF con todos los usuarios"""
    usuarios = Usuario.objects.all().order_by('id')
    total = usuarios.count()
    
    if not usuarios:
        return HttpResponse("No hay usuarios", status=404)

    usuarios_mes = Usuario.objects.extra(
        select={'mes': "DATE_FORMAT(fecha_creacion, '%%Y-%%m')"}
    ).values('mes').annotate(cantidad=Count('id')).order_by('mes')
    
    usuarios_inicial = Usuario.objects.extra(
        select={'inicial': "LEFT(nombre, 1)"}
    ).values('inicial').annotate(cantidad=Count('id')).order_by('-cantidad')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_todos_usuarios.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=1, fontSize=24, textColor=colors.HexColor('#2c3e50'), spaceAfter=20)
    section_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#3498db'), spaceBefore=15, spaceAfter=10)

    elements.append(Paragraph("📊 REPORTE GENERAL DE USUARIOS", title_style))
    elements.append(Paragraph(f"Total: {total} usuarios", section_style))
    
    data = [['ID', 'Nombre', 'Correo', 'Teléfono', 'Fecha']]
    for u in usuarios:
        data.append([str(u.id), str(u.nombre)[:25], str(u.correo)[:30], str(u.telefono or ''), str(u.fecha_creacion)[:10]])

    table = Table(data, colWidths=[0.5*inch, 1.5*inch, 2*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
    ]))
    elements.append(table)

    datos_mes = [(u['mes'], u['cantidad']) for u in usuarios_mes[:10]]
    if datos_mes:
        elements.append(Paragraph("📊 GRÁFICO DE BARRAS", section_style))
        drawing = Drawing(400, 200)
        max_val = max(cant for _, cant in datos_mes) if datos_mes else 1
        colores_barras = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        for i, (mes, cantidad) in enumerate(datos_mes):
            bar_height = (cantidad / max_val) * 120
            rect = Rect(50 + i * 30, 30, 20, bar_height)
            rect.fillColor = HexColor(colores_barras[i % len(colores_barras)])
            drawing.add(rect)
        elements.append(drawing)

    datos_inicial = [(u['inicial'], u['cantidad']) for u in usuarios_inicial[:10]]
    if datos_inicial:
        elements.append(Paragraph("🥧 GRÁFICO DE TORTA", section_style))
        drawing_torta = Drawing(200, 200)
        total_inicial = sum(cant for _, cant in datos_inicial)
        colores_torta = ['#667eea', '#f5576c', '#43e97b', '#fa709a', '#fee140']
        angle = 0
        for i, (inicial, cantidad) in enumerate(datos_inicial):
            if total_inicial > 0:
                span = (cantidad / total_inicial) * 360
                wedge = Wedge(100, 100, 80, angle, angle + span - 1)
                wedge.fillColor = HexColor(colores_torta[i % len(colores_torta)])
                drawing_torta.add(wedge)
                angle += span
        elements.append(drawing_torta)

    doc.build(elements)
    return response


def generar_excel(request, id_usuario):
    """Genera Excel con gráficos"""
    try:
        usuario = Usuario.objects.get(id=id_usuario)
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)

    total_usuarios = Usuario.objects.count()
    
    usuarios_mes = Usuario.objects.extra(
        select={'mes': "DATE_FORMAT(fecha_creacion, '%%Y-%%m')"}
    ).values('mes').annotate(cantidad=Count('id')).order_by('mes')
    
    usuarios_inicial = Usuario.objects.extra(
        select={'inicial': "LEFT(nombre, 1)"}
    ).values('inicial').annotate(cantidad=Count('id')).order_by('-cantidad')

    wb = Workbook()
    ws_datos = wb.active
    ws_datos.title = "Datos del Usuario"

    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    ws_datos.merge_cells('A1:B1')
    ws_datos['A1'] = f"Informe de Usuario - ID: {id_usuario}"
    ws_datos['A1'].font = Font(bold=True, size=16, color="2c3e50")
    ws_datos['A1'].alignment = Alignment(horizontal='center')

    data = [
        ['Campo', 'Información'],
        ['ID', str(usuario.id)],
        ['Nombre', str(usuario.nombre)],
        ['Correo', str(usuario.correo)],
        ['Teléfono', str(usuario.telefono or 'N/A')],
        ['Dirección', str(usuario.direccion or 'N/A')],
        ['Fecha de Creación', str(usuario.fecha_creacion)]
    ]

    for row_idx, row_data in enumerate(data, 3):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws_datos.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border
            if row_idx == 3:
                cell.font = header_font
                cell.fill = header_fill

    ws_datos.column_dimensions['A'].width = 25
    ws_datos.column_dimensions['B'].width = 45

    if usuarios_mes:
        ws_barras = wb.create_sheet("Gráfico Barras")
        ws_barras['A1'] = "GRÁFICO DE BARRAS"
        ws_barras['A1'].font = Font(bold=True, size=14, color="ffffff")
        ws_barras['A1'].fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")
        
        datos_mes = [(u['mes'], u['cantidad']) for u in usuarios_mes[:12]]
        ws_barras['A3'] = 'Mes'
        ws_barras['B3'] = 'Cantidad'
        
        for i, (mes, cantidad) in enumerate(datos_mes, 4):
            ws_barras.cell(row=i, column=1, value=str(mes))
            ws_barras.cell(row=i, column=2, value=cantidad)

        chart = BarChart()
        chart.title = "Usuarios por Mes"
        data_ref = Reference(ws_barras, min_col=2, min_row=3, max_row=3+len(datos_mes))
        cats_ref = Reference(ws_barras, min_col=1, min_row=4, max_row=3+len(datos_mes))
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        ws_barras.add_chart(chart, "D3")

    if usuarios_inicial:
        ws_torta = wb.create_sheet("Gráfico Torta")
        ws_torta['A1'] = "GRÁFICO DE TORTA"
        ws_torta['A1'].font = Font(bold=True, size=14, color="ffffff")
        ws_torta['A1'].fill = PatternFill(start_color="9b59b6", end_color="9b59b6", fill_type="solid")
        
        datos_inicial = [(u['inicial'], u['cantidad']) for u in usuarios_inicial[:10]]
        ws_torta['A3'] = 'Inicial'
        ws_torta['B3'] = 'Cantidad'
        
        for i, (inicial, cantidad) in enumerate(datos_inicial, 4):
            ws_torta.cell(row=i, column=1, value=inicial or '?')
            ws_torta.cell(row=i, column=2, value=cantidad)

        pie = PieChart()
        data_ref = Reference(ws_torta, min_col=2, min_row=3, max_row=3+len(datos_inicial))
        cats_ref = Reference(ws_torta, min_col=1, min_row=4, max_row=3+len(datos_inicial))
        pie.add_data(data_ref, titles_from_data=True)
        pie.set_categories(cats_ref)
        ws_torta.add_chart(pie, "D3")

    ws_dispersion = wb.create_sheet("Gráfico Dispersión")
    ws_dispersion['A1'] = "GRÁFICO DE DISPERSIÓN"
    ws_dispersion['A1'].font = Font(bold=True, size=14, color="ffffff")
    ws_dispersion['A1'].fill = PatternFill(start_color="e67e22", end_color="e67e22", fill_type="solid")
    
    usuarios_disp = list(Usuario.objects.all()[:15])
    ws_dispersion['A3'] = 'ID'
    ws_dispersion['B3'] = 'Long. Nombre'
    ws_dispersion['C3'] = 'Long. Correo'
    
    for i, u in enumerate(usuarios_disp, 4):
        ws_dispersion.cell(row=i, column=1, value=u.id)
        ws_dispersion.cell(row=i, column=2, value=len(u.nombre) if u.nombre else 0)
        ws_dispersion.cell(row=i, column=3, value=len(u.correo) if u.correo else 0)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}.xlsx"'
    wb.save(response)
    return response


def generar_excel_todos(request):
    """Genera Excel con todos los usuarios"""
    usuarios = Usuario.objects.all().order_by('id')
    
    usuarios_mes = Usuario.objects.extra(
        select={'mes': "DATE_FORMAT(fecha_creacion, '%%Y-%%m')"}
    ).values('mes').annotate(cantidad=Count('id')).order_by('mes')

    wb = Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    ws.merge_cells('A1:F1')
    ws['A1'] = f"REPORTE GENERAL - Total: {usuarios.count()} usuarios"
    ws['A1'].font = Font(bold=True, size=14, color="2c3e50")
    ws['A1'].alignment = Alignment(horizontal='center')

    headers = ['ID', 'Nombre', 'Correo', 'Teléfono', 'Dirección', 'Fecha Creación']
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border
        cell.alignment = Alignment(horizontal='center')

    for row_idx, usuario in enumerate(usuarios, 4):
        ws.cell(row=row_idx, column=1, value=usuario.id).border = border
        ws.cell(row=row_idx, column=2, value=usuario.nombre).border = border
        ws.cell(row=row_idx, column=3, value=usuario.correo).border = border
        ws.cell(row=row_idx, column=4, value=usuario.telefono or 'N/A').border = border
        ws.cell(row=row_idx, column=5, value=usuario.direccion or 'N/A').border = border
        ws.cell(row=row_idx, column=6, value=str(usuario.fecha_creacion)[:19]).border = border

    if usuarios_mes:
        ws_grafico = wb.create_sheet("Estadísticas")
        ws_grafico['A1'] = "Gráfico de Usuarios por Mes"
        ws_grafico['A1'].font = Font(bold=True, size=14)
        
        datos_mes = [(u['mes'], u['cantidad']) for u in usuarios_mes[:12]]
        ws_grafico['A3'] = 'Mes'
        ws_grafico['B3'] = 'Cantidad'
        
        for i, (mes, cantidad) in enumerate(datos_mes, 4):
            ws_grafico.cell(row=i, column=1, value=str(mes))
            ws_grafico.cell(row=i, column=2, value=cantidad)

        chart = BarChart()
        chart.title = "Usuarios por Mes"
        data_ref = Reference(ws_grafico, min_col=2, min_row=3, max_row=3+len(datos_mes))
        cats_ref = Reference(ws_grafico, min_col=1, min_row=4, max_row=3+len(datos_mes))
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        ws_grafico.add_chart(chart, "D3")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_todos_usuarios.xlsx"'
    wb.save(response)
    return response