from PIL import Image, ImageDraw

# Crear imagen 200x200
img = Image.new('RGB', (200, 200), color='#667eea')
draw = ImageDraw.Draw(img)

# Círculo blanco
draw.ellipse([20, 20, 180, 180], fill='white')

# Dibujar rectángulo central
draw.rectangle([70, 60, 130, 140], fill='#667eea')

# Texto SG
draw.text((75, 75), 'SG', fill='white')

# Guardar
img.save('mi_proyecto/documentos/static/images/logo.png')
print('Logo creado exitosamente')