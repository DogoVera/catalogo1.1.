import os
import shutil
from pathlib import Path
from PIL import Image

def comprimir_imagen(input_path, output_path, quality=70, width=400, height=532):
    """
    Comprime una imagen y la redimensiona a un tamaño fijo
    """
    try:
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
        
        # Redimensionar a tamaño fijo manteniendo la relación de aspecto
        # Primero redimensionamos manteniendo la relación y luego recortamos al centro
        img_ratio = img.width / img.height
        target_ratio = width / height
        
        if img_ratio > target_ratio:
            # La imagen es más ancha que el objetivo
            new_height = height
            new_width = int(height * img_ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            # Recortar los lados
            left = (new_width - width) // 2
            right = left + width
            img = img.crop((left, 0, right, height))
        else:
            # La imagen es más alta que el objetivo
            new_width = width
            new_height = int(width / img_ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            # Recortar la parte superior e inferior
            top = (new_height - height) // 2
            bottom = top + height
            img = img.crop((0, top, width, bottom))
        
        # Guardar comprimida
        img.save(output_path, optimize=True, quality=quality)
        return True
        
    except Exception as e:
        print(f"Error al comprimir {input_path}: {e}")
        return False

def procesar_imagenes(carpeta_madre, calidad=70):
    """
    Procesa todas las imágenes en las subcarpetas de la carpeta madre,
    las comprime a 400x532px y las copia renombradas a una carpeta PORSUBIR
    """
    # Convertir a Path object
    carpeta_madre = Path(carpeta_madre)
    
    # Crear carpeta PORSUBIR si no existe
    carpeta_destino = carpeta_madre / "PORSUBIR"
    carpeta_destino.mkdir(exist_ok=True)
    
    # Contadores para productos y fotos
    contador_producto = 1
    contador_foto_total = 1
    
    # Extensiones de imagen válidas
    extensiones_validas = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    # Recorrer todas las subcarpetas
    for subcarpeta in carpeta_madre.iterdir():
        if subcarpeta.is_dir() and subcarpeta.name != "PORSUBIR":
            print(f"Procesando carpeta: {subcarpeta.name}")
            
            # Contador de fotos por producto
            contador_fotos_producto = 1
            
            # Buscar todas las imágenes en la subcarpeta
            for archivo in subcarpeta.iterdir():
                if archivo.is_file() and archivo.suffix.lower() in extensiones_validas:
                    # Generar nuevo nombre (siempre con extensión .jpg para las comprimidas)
                    nuevo_nombre = f"producto_{contador_producto}_foto{contador_fotos_producto}.jpg"
                    ruta_destino = carpeta_destino / nuevo_nombre
                    
                    # Comprimir y redimensionar la imagen a 400x532px
                    if comprimir_imagen(archivo, ruta_destino, quality=calidad, width=400, height=532):
                        print(f"  Procesado: {archivo.name} -> {nuevo_nombre} (400x532px, {calidad}% calidad)")
                    else:
                        # Si falla la compresión, copiar el original
                        shutil.copy2(archivo, ruta_destino)
                        print(f"  Copiado (sin procesar): {archivo.name} -> {nuevo_nombre}")
                    
                    contador_fotos_producto += 1
                    contador_foto_total += 1
            
            # Solo incrementar contador de producto si se encontraron imágenes
            if contador_fotos_producto > 1:
                contador_producto += 1
    
    print(f"\nProceso completado!")
    print(f"Total de productos procesados: {contador_producto - 1}")
    print(f"Total de fotos procesadas: {contador_foto_total - 1}")
    print(f"Todas las imágenes tienen tamaño: 400x532 píxeles")
    print(f"Las imágenes están en: {carpeta_destino}")

def main():
    # Solicitar la carpeta madre al usuario
    carpeta_madre = input("Ingrese la ruta de la carpeta madre (ej: H:\\SHEIN): ").strip()
    
    # Verificar que la carpeta existe
    if not os.path.exists(carpeta_madre):
        print(f"Error: La carpeta '{carpeta_madre}' no existe.")
        return
    
    # Solicitar calidad de compresión
    try:
        calidad = int(input("Calidad de compresión (1-100, recomiendo 70): ") or "70")
        calidad = max(1, min(100, calidad))  # Asegurar que esté entre 1-100
    except ValueError:
        calidad = 70
        print("Usando calidad por defecto: 70")
    
    # Procesar las imágenes
    procesar_imagenes(carpeta_madre, calidad=calidad)

if __name__ == "__main__":
    main()