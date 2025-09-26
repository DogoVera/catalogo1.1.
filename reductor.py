from PIL import Image

def compress_image(input_path, output_path, quality=70, max_width=1200):
    img = Image.open(input_path)
    
    # Convertir RGBA a RGB si es necesario (para imágenes con transparencia)
    if img.mode == 'RGBA':
        # Crear fondo blanco y pegar la imagen manteniendo la transparencia
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # Usar el canal alpha como máscara
        img = background
    elif img.mode != 'RGB':
        # Convertir otros modos a RGB
        img = img.convert('RGB')
    
    # Reducir tamaño si es muy grande
    if img.width > max_width:
        ratio = max_width / float(img.width)
        height = int(float(img.height) * ratio)
        img = img.resize((max_width, height), Image.LANCZOS)
    
    # Guardar comprimida
    img.save(output_path, optimize=True, quality=quality)
    print(f"Imagen comprimida y guardada como {output_path}")

# Ejemplo de uso
compress_image("original.jpg", "comprimida.jpg", quality=70, max_width=1200)