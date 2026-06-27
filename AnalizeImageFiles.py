import os
from PIL import Image   # Pillow, incluida con muchas instalaciones de Python/Maya

# Extensiones comunes de imágenes
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".exr", ".bmp", ".gif"}

def scan_images(root_dir):
    image_files = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in IMAGE_EXTS:
                full_path = os.path.join(dirpath, filename)
                info = {"path": full_path}

                # Intenta leer resolución si Pillow lo soporta
                try:
                    with Image.open(full_path) as img:
                        info["size"] = img.size  # (ancho, alto)
                        info["mode"] = img.mode
                except Exception as e:
                    info["size"] = None
                    info["mode"] = None

                # Tamaño en disco
                try:
                    info["filesize_mb"] = round(os.path.getsize(full_path) / (1024 * 1024), 2)
                except Exception:
                    info["filesize_mb"] = None

                image_files.append(info)

    return image_files


# Ejemplo de uso
if __name__ == "__main__":
    carpeta = r"C:\ruta\a\tu\carpeta"   # 🔧 cámbiala a tu ruta
    resultados = scan_images(carpeta)

    for r in resultados:
        print(f"{r['path']}")
        print(f"   -> Tamaño disco: {r['filesize_mb']} MB")
        if r["size"]:
            print(f"   -> Resolución: {r['size'][0]} x {r['size'][1]}  ({r['mode']})")
        else:
            print("   -> Resolución: [no legible]")
