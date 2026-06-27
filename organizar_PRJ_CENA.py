import os
import re
import shutil

# ---------------- CONFIGURACIÓN ----------------

# Carpeta donde están los archivos .mb
FILES_DIR = r"F:\WORK\EMPRESAS\UTAD\U-tad\ANID_2026_PRY_CENA - Documentos\cena\sequences\Z_Pipeline_Seq\Z_Pipeline_Shot\lgt\publish\maya"

# Carpeta base que se va a duplicar
BASE_SHOT_DIR = r"F:\WORK\EMPRESAS\UTAD\U-tad\ANID_2026_PRY_CENA - Documentos\cena\sequences\SQ0010\SQ0010_SH0010"

# Carpeta donde se crearán las nuevas carpetas duplicadas
DESTINATION_ROOT = r"F:\WORK\EMPRESAS\UTAD\U-tad\ANID_2026_PRY_CENA - Documentos\cena\sequences\SQ0010"

# Subruta dentro del shot donde va el archivo .mb
MAYA_PUBLISH_SUBPATH = os.path.join("lgt", "publish", "maya")

# Expresión regular para capturar el número de plano
# Ejemplo: LUC_Shot_020_VF_VP.mb → 020
SHOT_REGEX = re.compile(r"_Shot_(\d+)_")

# -----------------------------------------------

for file_name in os.listdir(FILES_DIR):
    if not file_name.lower().endswith(".mb"):
        continue

    match = SHOT_REGEX.search(file_name)
    if not match:
        print(f"No se pudo extraer plano de: {file_name}")
        continue

    shot_number = match.group(1)  # respeta padding (ej: '020')

    # Construir nombre de la nueva carpeta
    new_shot_folder_name = f"SQ0010_SH{shot_number.zfill(len(shot_number))}"
    new_shot_path = os.path.join(DESTINATION_ROOT, new_shot_folder_name)

    # Duplicar la carpeta base si no existe
    if not os.path.exists(new_shot_path):
        shutil.copytree(BASE_SHOT_DIR, new_shot_path)
        print(f"Carpeta creada: {new_shot_folder_name}")
    else:
        print(f"La carpeta ya existe: {new_shot_folder_name}")

    # Ruta destino del archivo .mb
    maya_publish_path = os.path.join(new_shot_path, MAYA_PUBLISH_SUBPATH)
    os.makedirs(maya_publish_path, exist_ok=True)

    source_file = os.path.join(FILES_DIR, file_name)
    destination_file = os.path.join(maya_publish_path, file_name)

    shutil.copy2(source_file, destination_file)
    print(f"Archivo copiado: {file_name} → {destination_file}")
