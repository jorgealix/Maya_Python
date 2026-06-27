import hou
import os
import shutil

# Obtener el valor del parámetro "cachedir"
cachedir_parm = hou.parm("cachedir")
cachedir = cachedir_parm.eval()

# Obtener el nombre del archivo hip actual
hipfile_path = hou.hipFile.name()

# Obtener el nombre del archivo hip original sin la ruta
hipfile_name = os.path.basename(hipfile_path)

# Construir la nueva ubicación del archivo hip (copia)
new_hipfile = os.path.join(cachedir, hipfile_name)

# Guardar la versión actual en su ubicación actual
hou.hipFile.save(file_name=hipfile_path)

# Verificar si la ruta especificada en "cachedir" existe, si no, crearla
if not os.path.exists(cachedir):
    os.makedirs(cachedir)

# Copiar el proyecto actual a la nueva ubicación
shutil.copy(hipfile_path, new_hipfile)

print("Copia del proyecto creada en:", new_hipfile)
