from PIL import Image, ImageDraw

# Crear imagen 200x200 con gradiente azul
img = Image.new('RGB', (200, 200), color='#0066cc')
draw = ImageDraw.Draw(img)

# Círculo blanco centrado
draw.ellipse([30, 30, 170, 170], fill='white')

# Rectángulo azul oscuro
draw.rectangle([70, 60, 130, 140], fill='#0066cc')

# Texto SG en blanco
draw.text((75, 82), 'SG', fill='white')

# Guardar
img.save('mi_proyecto/documentos/static/images/logo.png')
print('Logo creado exitosamente')