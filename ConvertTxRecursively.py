import os
import subprocess

# Ruta a maketx.exe (ajústala según tu instalación de Arnold/OpenImageIO)
MAKETX = r"C:\Program Files\Autodesk\Arnold\maya2024\bin\maketx.exe"

# Extensiones de texturas soportadas
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".exr", ".bmp", ".hdr"}

# Palabras clave para identificar maps de "datos" (no se colorconvert)
DATA_MAP_KEYWORDS = ["rough", "normal", "bump", "disp", "metal", "mask", "spec", "gloss", "opacity"]

def is_data_map(filename):
    """Devuelve True si el archivo parece ser un mapa de datos (no color)"""
    fname = filename.lower()
    return any(k in fname for k in DATA_MAP_KEYWORDS)

def convert_to_tx(root_dir):
    converted = 0
    checked = 0

    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in IMAGE_EXTS:
                checked += 1
                src = os.path.join(dirpath, f)
                dst = os.path.splitext(src)[0] + ".tx"

                # Evitar reconvertir si el .tx ya existe y es más nuevo
                if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
                    print(f"⏩ Ya existe actualizado: {dst}")
                    continue

                # Armar comando base
                cmd = [MAKETX, "-v", "--oiio", "--unpremult", "--compression", "zip"]

                # Casuística ACEScg: colorconvert solo para mapas de color
                if not is_data_map(f):
                    cmd += ["--colorconvert", "sRGB", "acescg"]

                cmd += ["-o", dst, src]

                try:
                    print(f"🔄 Convirtiendo: {src}")
                    subprocess.run(cmd, check=True)
                    converted += 1
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error al convertir {src}: {e}")

    # Mensaje final
    print("\n📂 Escaneo de subdirectorios completado.")
    print(f"   Texturas revisadas: {checked}")
    print(f"   Archivos .tx generados: {converted}")


# 🔧 Ajusta esta ruta a tu proyecto
if __name__ == "__main__":
    convert_to_tx(r"S:\alma\assets\Character\youngAlma\txsh\work\textures")