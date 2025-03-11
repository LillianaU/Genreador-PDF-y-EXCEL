from django.urls import path
from .views import index, generar_pdf, generar_excel

urlpatterns = [
    path('', index, name='index'),
    path('generar_pdf/<int:id_usuario>/', generar_pdf, name='generar_pdf'),
    path('generar_excel/<int:id_usuario>/', generar_excel, name='generar_excel'),
]
