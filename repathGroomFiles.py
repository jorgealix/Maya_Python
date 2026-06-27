import maya.cmds as cmds
import os
import re

def obtener_ultima_version(carpeta_base):
    """
    Devuelve la ruta completa de la subcarpeta con la versión más alta
    que tenga nombre en formato 'v001', 'v002', etc.
    """
 
    subcarpetas = [d for d in os.listdir(carpeta_base)
                   if os.path.isdir(os.path.join(carpeta_base, d))]

    version_pattern = re.compile(r"v(\d+)$")
    versiones = []
    for d in subcarpetas:
        m = version_pattern.match(d)
        if m:
            num = int(m.group(1))
            versiones.append((num, d))

    if not versiones:
        return None

    ultima_version = max(versiones, key=lambda x: x[0])[1]
    return os.path.join(carpeta_base, ultima_version)
    

def actualizar_ruta_cache_yeti():
    """
    Actualiza inputCacheFilename de nodos pgYetiGroom que terminen con '_groom'
    apuntando automáticamente a la última versión de groom
    deducida de la ruta del archivo Maya actual.
    """
    # Ruta del archivo de Maya actual
    maya_file = cmds.file(q=True, sn=True)
    if not maya_file:
        print("El archivo de Maya no está guardado. Guarda primero la escena.")
        return

    carpeta_scene = os.path.dirname(maya_file)
    partes = carpeta_scene.replace("\\", "/").split("/")
    scene_name = os.path.basename(maya_file)
    scene_name_no_ext = os.path.splitext(scene_name)[0]
    print(scene_name_no_ext)
    # Intentar deducir el nombre del personaje desde la carpeta Character
    try:
        idx_character = partes.index("Character") + 1
        character_name = partes[idx_character]
    except ValueError:
        print("No se pudo determinar el character desde la ruta:", carpeta_scene)
        return

    # Construir la ruta base de groom
    carpeta_base = os.path.join("/".join(partes[:idx_character + 1]), "groom")

    # Obtener última versión
    ultima_version = obtener_ultima_version(carpeta_base)
    if not ultima_version:
        print("No se encontraron subcarpetas de versión en:", carpeta_base)
        return

    ruta_nueva_carpeta = ultima_version.replace("\\", "/")
    print("Última versión de groom encontrada:", ruta_nueva_carpeta)

    # Lista nodos pgYetiGroom con sufijo _groom
    groom_nodes = [n for n in cmds.ls(type="pgYetiMaya") if n.endswith("_groomShape")]
    if not groom_nodes:
        print("No se encontraron nodos pgYetiGroom con sufijo '_groomShape' en la escena.")
        return

    # Actualizar cada nodo
    for groom in groom_nodes:
        attr = f"{groom}.cacheFileName"
        if not cmds.objExists(attr):
            continue

        path_actual = cmds.getAttr(attr)
        if not path_actual:
            continue

        nombre_archivo = ( scene_name_no_ext + "_" + groom + "_" + ultima_version.split("\\")[-1] + ".grm")
        #print(nombre_archivo)
        nueva_ruta = os.path.join(ruta_nueva_carpeta, nombre_archivo)
        nueva_ruta = nueva_ruta.replace("\\", "/")
        

        cmds.setAttr(attr, nueva_ruta, type="string")
        print(f"{groom}: {path_actual} -> {nueva_ruta}")


# -------------------------------
# Ejecutar
actualizar_ruta_cache_yeti()