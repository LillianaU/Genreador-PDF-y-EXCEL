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
from openpyxl.chart import BarChart, Reference  # Gráficos Excel
from openpyxl.utils import get_column_letter

# Importaciones para gráficos
import io
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF

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
    if not id_usuario:
        return HttpResponse("ID de usuario no proporcionado", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT DATE(fecha_creacion) as fecha, COUNT(*) as cantidad FROM usuarios GROUP BY DATE(fecha_creacion) ORDER BY fecha")
        usuarios_fecha = cursor.fetchall()
        
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
                fontSize=16,
                textColor=colors.HexColor('#3498db'),
                spaceBefore=20,
                spaceAfter=10
            )

            elements.append(Paragraph("INFORME DE USUARIO", title_style))
            elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))

            logo_path = os.path.join(settings.BASE_DIR, 'documentos', 'static', 'images')
            elements.append(Paragraph(" ", Spacer(1, 10)))

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
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8f9fa')]),
            ]))
            elements.append(table)

            elements.append(Paragraph("ESTADÍSTICAS GENERALES", section_style))
            
            stats_data = [
                ['Métrica', 'Valor'],
                ['Total de Usuarios en el Sistema', str(total_usuarios)],
                ['Este Usuario representa', f'{(1/total_usuarios)*100:.2f}%' if total_usuarios > 0 else 'N/A'],
                ['Registros por Fecha', str(len(usuarios_fecha))],
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f8f5')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1e8449')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#27ae60')),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            elements.append(stats_table)

            if usuarios_fecha:
                elements.append(Paragraph("DISTRIBUCIÓN DE USUARIOS POR FECHA", section_style))
                
                chart_data = [['Fecha', 'Cantidad']]
                for fecha, cantidad in usuarios_fecha[:10]:
                    chart_data.append([str(fecha), str(cantidad)])
                
                chart_table = Table(chart_data, colWidths=[3*inch, 1.5*inch])
                chart_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ebf5fb')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#3498db')),
                ]))
                elements.append(chart_table)

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

def generar_excel(request, id_usuario):
    if not id_usuario:
        return HttpResponse("ID de usuario no proporcionado", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_usuario])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT DATE(fecha_creacion) as fecha, COUNT(*) as cantidad FROM usuarios GROUP BY DATE(fecha_creacion) ORDER BY fecha")
        usuarios_fecha = cursor.fetchall()
        
        if row:
            usuario = dict(zip(columns, row))
            
            wb = Workbook()
            
            ws_datos = wb.active
            ws_datos.title = "Datos del Usuario"

            header_font = Font(bold=True, color="FFFFFF", size=12)
            header_fill = PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")
            border = Border(
                left=Side(style='thin'), 
                right=Side(style='thin'), 
                top=Side(style='thin'), 
                bottom=Side(style='thin')
            )
            
            title_font = Font(bold=True, size=16, color="2c3e50")
            ws_datos.merge_cells('A1:B1')
            ws_datos['A1'] = f"Informe de Usuario - ID: {id_usuario}"
            ws_datos['A1'].font = title_font
            ws_datos['A1'].alignment = Alignment(horizontal='center')
            ws_datos.row_dimensions[1].height = 25

            ws_datos.merge_cells('A2:B2')
            ws_datos['A2'] = f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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

            ws_stats = wb.create_sheet("Estadísticas")
            
            ws_stats.merge_cells('A1:D1')
            ws_stats['A1'] = "ESTADÍSTICAS DEL SISTEMA"
            ws_stats['A1'].font = Font(bold=True, size=16, color="ffffff")
            ws_stats['A1'].fill = PatternFill(start_color="27ae60", end_color="27ae60", fill_type="solid")
            ws_stats['A1'].alignment = Alignment(horizontal='center')
            ws_stats.row_dimensions[1].height = 25

            stats_data = [
                ['Métrica', 'Valor', 'Descripción', 'Porcentaje'],
                ['Total de Usuarios', str(total_usuarios), 'Usuarios registrados', '100%'],
                ['Usuario Actual', '1', f'ID: {id_usuario}', f'{(1/total_usuarios)*100:.2f}%' if total_usuarios > 0 else 'N/A'],
                ['Fechas con Registros', str(len(usuarios_fecha)), 'Días con actividad', f'{(len(usuarios_fecha)/total_usuarios)*100:.1f}%' if total_usuarios > 0 else 'N/A'],
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

            if usuarios_fecha:
                ws_grafico = wb.create_sheet("Gráfico de Usuarios")
                
                ws_grafico.merge_cells('A1:C1')
                ws_grafico['A1'] = "DISTRIBUCIÓN DE USUARIOS POR FECHA"
                ws_grafico['A1'].font = Font(bold=True, size=14, color="ffffff")
                ws_grafico['A1'].fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")
                ws_grafico['A1'].alignment = Alignment(horizontal='center')

                chart_data = [['Fecha', 'Cantidad', 'Barras']]
                max_cantidad = 0
                for fecha, cantidad in usuarios_fecha[:10]:
                    if cantidad > max_cantidad:
                        max_cantidad = cantidad
                    chart_data.append([str(fecha), cantidad, cantidad])

                for row_idx, row_data in enumerate(chart_data, 3):
                    for col_idx, value in enumerate(row_data, 1):
                        cell = ws_grafico.cell(row=row_idx, column=col_idx, value=value)
                        cell.border = border
                        
                        if row_idx == 3:
                            cell.font = header_font
                            cell.fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")
                        elif row_idx > 3 and col_idx == 2:
                            cell.fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")

                ws_grafico.column_dimensions['A'].width = 20
                ws_grafico.column_dimensions['B'].width = 12
                ws_grafico.column_dimensions['C'].width = 12

                chart = BarChart()
                chart.type = "col"
                chart.style = 10
                chart.title = "Usuarios por Fecha"
                chart.y_axis.title = 'Cantidad'
                chart.x_axis.title = 'Fecha'

                data_ref = Reference(ws_grafico, min_col=2, min_row=3, max_row=3+len(usuarios_fecha[:10]))
                cats_ref = Reference(ws_grafico, min_col=1, min_row=4, max_row=3+len(usuarios_fecha[:10]))
                chart.add_data(data_ref, titles_from_data=True)
                chart.set_categories(cats_ref)
                chart.height = 10
                chart.width = 20

                ws_grafico.add_chart(chart, "E3")

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="usuario_{id_usuario}_{datetime.now().strftime("%Y%m%d")}.xlsx"'

            wb.save(response)
            return response
            
    return HttpResponse("Usuario no encontrado", status=404)

