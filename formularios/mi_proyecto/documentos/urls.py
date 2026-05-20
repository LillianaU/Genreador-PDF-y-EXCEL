from django.urls import path
from .views import index, generar_pdf, generar_excel, listar_usuarios, generar_pdf_todos, generar_excel_todos

urlpatterns = [
    path('', index, name='index'),
    path('lista/', listar_usuarios, name='lista_usuarios'),
    path('generar_pdf/<int:id_usuario>/', generar_pdf, name='generar_pdf'),
    path('generar_excel/<int:id_usuario>/', generar_excel, name='generar_excel'),
    path('generar_pdf_todos/', generar_pdf_todos, name='generar_pdf_todos'),
    path('generar_excel_todos/', generar_excel_todos, name='generar_excel_todos'),
]
