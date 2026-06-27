import maya.cmds as cmds
import os
import json
import fnmatch
def fix_textures_paths():
    
    # ----------------------------------------------------
    # CONFIG
    # ----------------------------------------------------
    
    SEARCH_ROOT = r"C:\Users\eviwo\Documents"
    LOG_FOLDER = os.path.join(SEARCH_ROOT, "_logs_texturas")
    
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    NOT_FOUND_LOG = os.path.join(LOG_FOLDER, "texturas_no_encontradas.json")
    UNUSED_FILES_LOG = os.path.join(LOG_FOLDER, "file_nodes_no_usados.json")
    
    SHADER_TYPES = cmds.listNodeTypes("shader")
    UDIM_TOKENS = ["<UDIM>", "<uvtile>"]
    
    # ----------------------------------------------------
    # INFO DE ESCENA
    # ----------------------------------------------------
    
    scene_path = cmds.file(query=True, sceneName=True)
    scene_name = os.path.basename(scene_path) if scene_path else "ESCENA_SIN_GUARDAR"
    scene_base_name = os.path.splitext(scene_name)[0]
    
    # ----------------------------------------------------
    # LOGS (con nombre de escena)
    # ----------------------------------------------------
    
    NOT_FOUND_LOG = os.path.join(
        LOG_FOLDER,
        f"{scene_base_name}_texturas_no_encontradas.json"
    )
    
    UNUSED_FILES_LOG = os.path.join(
        LOG_FOLDER,
        f"{scene_base_name}_file_nodes_no_usados.json"
    )
    
    
    # ----------------------------------------------------
    # UTILIDADES
    # ----------------------------------------------------
    
    def limpiar_nombre_udim(nombre):
        for token in UDIM_TOKENS:
            nombre = nombre.replace(token, "*")
        return nombre
    
    
    def buscar_archivo_udim(patron, raiz):
        encontrados = []
        for root, dirs, files in os.walk(raiz):
            for f in files:
                if fnmatch.fnmatch(f, patron):
                    encontrados.append(os.path.join(root, f))
        return encontrados
    
    
    def file_llega_a_shader_asignado(file_node):
        destinos = cmds.listConnections(
            file_node,
            source=False,
            destination=True,
            skipConversionNodes=True
        ) or []
    
        visitados = set()
        stack = list(destinos)
    
        while stack:
            nodo = stack.pop()
            if nodo in visitados:
                continue
            visitados.add(nodo)
    
            if cmds.nodeType(nodo) in SHADER_TYPES:
                sgs = cmds.listConnections(nodo, type="shadingEngine") or []
                for sg in sgs:
                    if cmds.sets(sg, query=True):
                        return True
    
            siguientes = cmds.listConnections(
                nodo,
                source=False,
                destination=True,
                skipConversionNodes=True
            ) or []
    
            stack.extend(siguientes)
    
        return False
    
    # ----------------------------------------------------
    # MAIN
    # ----------------------------------------------------
    
    file_nodes = cmds.ls(type="file")
    
    texturas_no_encontradas = []
    file_nodes_no_usados = []
    
    for file_node in file_nodes:
        ruta = cmds.getAttr(file_node + ".fileTextureName")
        if not ruta:
            continue
    
        nombre = os.path.basename(ruta)
        patron = limpiar_nombre_udim(nombre)
    
        encontrados = buscar_archivo_udim(patron, SEARCH_ROOT)
    
        if encontrados:
            nueva_ruta = encontrados[0].replace("\\", "/")
            cmds.setAttr(file_node + ".fileTextureName", nueva_ruta, type="string")
            print("✔ Actualizada:", file_node)
        else:
            texturas_no_encontradas.append({
                "file_node": file_node,
                "archivo": nombre,
                "ruta_original": ruta
            })
            print("✘ No encontrada:", file_node)
    
        if not file_llega_a_shader_asignado(file_node):
            file_nodes_no_usados.append({
                "file_node": file_node,
                "ruta": ruta
            })
    
    # ----------------------------------------------------
    # GUARDAR LOGS CON METADATA DE ESCENA
    # ----------------------------------------------------
    
    not_found_data = {
        "scene_name": scene_name,
        "scene_path": scene_path,
        "items": texturas_no_encontradas
    }
    
    unused_files_data = {
        "scene_name": scene_name,
        "scene_path": scene_path,
        "items": file_nodes_no_usados
    }
    
    with open(NOT_FOUND_LOG, "w", encoding="utf-8") as f:
        json.dump(not_found_data, f, indent=4, ensure_ascii=False)
    
    with open(UNUSED_FILES_LOG, "w", encoding="utf-8") as f:
        json.dump(unused_files_data, f, indent=4, ensure_ascii=False)
    
    print("\n--- TERMINADO ---")
    print("Escena:", scene_name)
    print("Texturas no encontradas:", len(texturas_no_encontradas))
    print("File nodes no usados:", len(file_nodes_no_usados))
    print("Logs en:", LOG_FOLDER)
if __name__ == "__main__":
    fix_textures_paths()