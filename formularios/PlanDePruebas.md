# Plan de Pruebas - Sistema de Generación de PDF y Excel

---

## 1. RESUMEN EJECUTIVO

**Proyecto:** Sistema de Gestión de Usuarios con generación de PDF y Excel  
**Versión:** 1.0  
**Fecha:** Mayo 2026  
**Tecnología:** Django ORM + MySQL + ReportLab + openpyxl

---

## 2. ALCANCE DE PRUEBAS

### 2.1 Funcionalidades a probar

| Módulo | Funcionalidad | Tipo |
|--------|---------------|------|
| Modelo | Crear usuario | Prueba unitaria |
| Modelo | Validar correo único | Prueba unitaria |
| Modelo | Métodos helper | Prueba unitaria |
| Búsqueda | Buscar por ID | Prueba funcional |
| Búsqueda | Buscar por nombre | Prueba funcional |
| Búsqueda | Usuario no encontrado | Prueba funcional |
| PDF | Generar PDF por ID | Prueba funcional |
| PDF | Generar PDF general | Prueba funcional |
| PDF | PDF con usuario inexistente | Prueba funcional |
| Excel | Generar Excel por ID | Prueba funcional |
| Excel | Generar Excel general | Prueba funcional |
| Excel | Excel con usuario inexistente | Prueba funcional |
| ORM | count() | Prueba unitaria |
| ORM | filter() | Prueba unitaria |
| ORM | order_by() | Prueba unitaria |

---

## 3. ESTRATEGIA DE PRUEBAS

### 3.1 Tipos de pruebas

1. **Pruebas Unitarias**: Validar modelo y métodos individuales
2. **Pruebas de Integración**: Validar interacción entre componentes
3. **Pruebas Funcionales**: Validar funcionalidades del sistema

### 3.2 Ambiente de pruebas

- Base de datos de prueba: `test_ejemplo`
- Framework: Django Test Framework + pytest
- Navegador para pruebas manuales: Chrome/Firefox

---

## 4. CASOS DE PRUEBA

### 4.1 Pruebas del Modelo

| ID | Caso de prueba | Entrada | Resultado esperado | Estado |
|----|---------------|---------|-------------------|--------|
| M-01 | Crear usuario válido | nombre='Test', correo='test@test.com' | Usuario creado | ✅ |
| M-02 | Verificar __str__ | Usuario('Juan') | Retorna 'Juan' | ✅ |
| M-03 | get_telefono con valor | telefono='555-1234' | Retorna '555-1234' | ✅ |
| M-04 | get_telefono vacío | telefono=None | Retorna 'N/A' | ✅ |
| M-05 | get_direccion vacía | direccion=None | Retorna 'N/A' | ✅ |
| M-06 | Fecha creación automática | - | Fecha no nula | ✅ |
| M-07 | Correo único |重复correo | Exception | ✅ |

### 4.2 Pruebas de Vistas

| ID | Caso de prueba | Entrada | Resultado esperado | Estado |
|----|---------------|---------|-------------------|--------|
| V-01 | GET a index | GET / | Código 200 | ✅ |
| V-02 | POST buscar por ID | POST {id_usuario: 1} | Muestra usuario | ✅ |
| V-03 | POST buscar por nombre | POST {nombre_busqueda: 'Juan'} | Muestra resultados | ✅ |
| V-04 | POST ID inexistente | POST {id_usuario: 9999} | Muestra error | ✅ |
| V-05 | GET lista usuarios | GET /lista/ | Código 200 | ✅ |

### 4.3 Pruebas de PDF

| ID | Caso de prueba | Resultado esperado |
|----|---------------|-------------------|
| P-01 | GET /generar_pdf/1/ | Content-Type: application/pdf |
| P-02 | GET /generar_pdf/9999/ | Código 404 |
| P-03 | GET /generar_pdf_todos/ | PDF con todos los usuarios |

### 4.4 Pruebas de Excel

| ID | Caso de prueba | Resultado esperado |
|----|---------------|-------------------|
| E-01 | GET /generar_excel/1/ | Content-Type: spreadsheet |
| E-02 | GET /generar_excel/9999/ | Código 404 |
| E-03 | GET /generar_excel_todos/ | Excel con gráficos |

---

## 5. EJECUCIÓN DE PRUEBAS

### 5.1 Comandos de ejecución

```bash
# Ejecutar todas las pruebas
python manage.py test documentos

# Ejecutar con verbose
python manage.py test documentos --verbosity=2

# Ejecutar clase específica
python manage.py test documentos.test.PruebasModeloUsuario

# Ejecutar con pytest
pytest documentos/test.py -v
```

### 5.2 Resultados esperados

```
Ran 23 tests in 0.468s
OK
```

---

## 6. PRUEBAS MANUALES

### 6.1 Checklist de verificación

| # | Funcionalidad | Verificación | OK |
|---|---------------|--------------|-----|
| 1 | Página principal carga | http://127.0.0.1:8000/ | ☐ |
| 2 | Menú flotante SPA funciona | Click en botón menú | ☐ |
| 3 | Buscar usuario por ID | Ingresar ID y buscar | ☐ |
| 4 | Buscar usuario por nombre | Ingresar nombre y buscar | ☐ |
| 5 | Modal muestra datos usuario | Después de buscar por ID | ☐ |
| 6 | Descargar PDF individual | Click botón PDF | ☐ |
| 7 | Descargar Excel individual | Click botón Excel | ☐ |
| 8 | Página lista de usuarios | http://127.0.0.1:8000/lista/ | ☐ |
| 9 | Tabla muestra todos usuarios | Verificar datos | ☐ |
| 10 | PDF general | Botón PDF General | ☐ |
| 11 | Excel general | Botón Excel General | ☐ |
| 12 | Estética cafés aplicada | Verificar colores | ☐ |
| 13 | Logo se muestra | En header | ☐ |

### 6.2 Navegadores compatibles

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

---

## 7. REPORTE DE DEFECTOS

### Formato para reportar errores

```markdown
## Defecto #XXX

**Título:** [Breve descripción]
**Severidad:** Alta / Media / Baja
**Pasos para reproducir:**
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado esperado:** [Qué debería pasar]
**Resultado actual:** [Qué está pasando]

**Captura de pantalla:** [Adjuntar imagen]
```

---

## 8. MATRIZ DE TRAZABILIDAD

| Requisito | Caso de prueba | Estado |
|-----------|---------------|--------|
| RQ-01: Buscar por ID | V-02 | ✅ |
| RQ-02: Buscar por nombre | V-03 | ✅ |
| RQ-03: Generar PDF | P-01, P-02, P-03 | ✅ |
| RQ-04: Generar Excel | E-01, E-02, E-03 | ✅ |
| RQ-05: Ver lista usuarios | V-05 | ✅ |
| RQ-06: Gráficos en PDF | P-01 | ✅ |
| RQ-07: Gráficos en Excel | E-01 | ✅ |

---

## 9. CRITERIOS DE ACEPTACIÓN

### Para release 1.0:
- [x] 23 pruebas automáticas pasando
- [x] Todas las funcionalidades implementadas
- [x] Pruebas manuales completadas
- [x] Documentación actualizada

---

**Responsable de pruebas:** Sistema  
**Fecha de creación:** Mayo 2026  
**Última actualización:** Mayo 2026