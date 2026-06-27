import os
import subprocess
import maya.cmds as cmds

# Ruta a maketx.exe
MAKETX = r"C:\Program Files\Autodesk\Arnold\maya2026\bin\maketx.exe"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".exr", ".bmp", ".hdr"}

DATA_MAP_KEYWORDS = ["rough", "normal", "bump", "disp", "metal", "mask", "spec", "gloss", "opacity"]

def is_data_map(filename):
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

                if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
                    print(f"⏩ Ya existe actualizado: {dst}")
                    continue

                cmd = [MAKETX, "-v", "--oiio", "--unpremult", "--compression", "zip"]

                if not is_data_map(f):
                    cmd += ["--colorconvert", "sRGB", "linear"]

                cmd += ["-o", dst, src]

                try:
                    print(f"🔄 Convirtiendo: {src}")
                    subprocess.run(
                        cmd,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    converted += 1
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error al convertir {src}: {e}")

    cmds.confirmDialog(
        title="Conversión completada",
        message=f"Texturas revisadas: {checked}\n.tx generados: {converted}",
        button=["OK"]
    )

def ask_directory_and_run():
    folder = cmds.fileDialog2(
        dialogStyle=2,
        fileMode=3,  # Selección de carpeta
        caption="Selecciona carpeta raíz para convertir a .tx"
    )

    if not folder:
        return

    folder = folder[0]

    confirm = cmds.confirmDialog(
        title="Confirmar conversión",
        message=f"¿Convertir todas las texturas recursivamente en:\n\n{folder}?",
        button=["Sí", "No"],
        defaultButton="Sí",
        cancelButton="No",
        dismissString="No"
    )

    if confirm == "Sí":
        convert_to_tx(folder)