import re
from pathlib import Path

def procesar_urls(archivo_entrada, archivo_salida):
    """
    Procesa las URLs del archivo de entrada y genera el formato deseado
    """
    try:
        # Leer todas las URLs del archivo
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        # Filtrar solo las líneas que contienen URLs
        urls = [linea.strip() for linea in lineas if linea.strip().startswith('http')]
        
        if not urls:
            print("No se encontraron URLs en el archivo")
            return
        
        print(f"URLs encontradas: {len(urls)}")
        
        # Agrupar URLs por producto
        productos = {}
        for url in urls:
            # Buscar el patrón producto-X-fotoY en la URL (con guiones)
            match = re.search(r'producto-(\d+)-foto(\d+)', url)
            if match:
                num_producto = match.group(1)
                num_foto = int(match.group(2))
                
                if num_producto not in productos:
                    productos[num_producto] = []
                
                productos[num_producto].append((num_foto, url))
                print(f"Encontrado: producto-{num_producto}-foto{num_foto}")
            else:
                print(f"URL no coincide con el patrón: {url}")
        
        if not productos:
            print("No se encontraron URLs con el patrón 'producto-XX-fotoYY'")
            return
        
        # Ordenar las fotos de cada producto por número de foto
        for producto in productos:
            productos[producto].sort(key=lambda x: x[0])
            productos[producto] = [url for _, url in productos[producto]]
        
        # Generar el contenido del archivo
        contenido = "const rawProducts = `\n"
        
        for i, (num_producto, urls_producto) in enumerate(productos.items(), 1):
            contenido += f"(PRODUCTO{i}\n"
            for url in urls_producto:
                contenido += f"{url}\n"
            contenido += ")\n"
        
        contenido += "`;"
        
        # Guardar el archivo de salida
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"\nProceso completado!")
        print(f"Productos procesados: {len(productos)}")
        print(f"Total de URLs procesadas: {sum(len(urls) for urls in productos.values())}")
        print(f"Archivo generado: {archivo_salida}")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_entrada}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    # Archivos de entrada y salida
    archivo_entrada = "sinfiltrar.txt"
    archivo_salida = "filtrado.txt"
    
    # Verificar que el archivo de entrada existe
    if not Path(archivo_entrada).exists():
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        print("Asegúrate de que el archivo 'sinfiltrar.txt' esté en la misma carpeta que este script.")
        return
    
    # Procesar las URLs
    procesar_urls(archivo_entrada, archivo_salida)

if __name__ == "__main__":
    main()