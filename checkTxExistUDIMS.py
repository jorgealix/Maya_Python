import maya.cmds as cmds
import os
import re
import glob

def get_texture_dir_from_standin(standin_path):
    """
    A partir del path del ASS o USD:
    example:
        P:/Proyecto/Asset01/shading/geo.ass
        → P:/Proyecto/Asset01/textures/
    """
    
    if not standin_path:
        return None
    
    standin_path = standin_path.replace("\\", "/")
    folder = os.path.dirname(standin_path)
    
    # Patrón estándar: shading → textures
    tokens = folder.split("/")
    if "shading" in tokens:
        idx = tokens.index("shading")
        tokens[idx] = "texture"
        tex_dir = "/".join(tokens)
        
        if os.path.isdir(tex_dir):
            return tex_dir

    # Fallback: buscar carpeta textures al nivel superior
    parent = os.path.dirname(folder)
    for candidate in ["texture", "Texture"]:
        try_path = os.path.join(parent, candidate)
        if os.path.isdir(try_path):
            return try_path
    
    return None
    print("get_texture_dir_from_standin")


def check_single_texture(path):
    """
    Chequea una textura normal o UDIM y busca .tx
    """
    results = []
    if not path:
        return results

    # Detectar UDIM
    is_udim = "<UDIM>" in path or re.search(r"\d{4}", os.path.basename(path))
    
    # --- Caso: textura normal ---
    if not is_udim:
        base, ext = os.path.splitext(path)
        tx = base + ".tx"
        if os.path.exists(tx):
            results.append(("OK", tx))
        else:
            results.append(("MISSING", tx))
        return results

    # --- Caso: UDIM ---
    if "<UDIM>" in path:
        udim_pattern = path.replace("<UDIM>", "1???")
    else:
        m = re.search(r"(.*?)(1\d{3})(.*)", path)
        if m:
            udim_pattern = m.group(1) + "1???" + m.group(3)
        else:
            udim_pattern = None
    
    if not udim_pattern:
        results.append(("ERROR", "No se pudo interpretar UDIM en " + path))
        return results

    # Buscar UDIMs reales
    udim_files = glob.glob(udim_pattern)
    if not udim_files:
        results.append(("MISSING", "No UDIMs found: " + udim_pattern))
        return results

    for f in udim_files:
        base, ext = os.path.splitext(f)
        tx = base + ".tx"
        if os.path.exists(tx):
            results.append(("OK", tx))
        else:
            results.append(("MISSING", tx))
    
    return results
    print("check_single_texture")


def check_tx_for_asset():
    sels = cmds.ls(sl=True)
    if not sels:
        cmds.warning("No hay selección.")
        return

    print("\n================ CHEQUEO DE TEXTURAS Y TX ================\n")
    # ---------------------------------------------------------------------
    # 1) FILE nodes directos del asset
    # ---------------------------------------------------------------------
    file_nodes = cmds.listConnections(sels, type="file", s=True, d=False) or []
    if file_nodes:
        print("---- Texturas de FILE nodes ----")
        for f in file_nodes:
            tex = cmds.getAttr(f + ".fileTextureName")
            print("\nNode:", f)
            print("Texture:", tex)
            for status, path in check_single_texture(tex):
                print(" ", "✔" if status == "OK" else "❌", status, "→", path)
        print("\n----------------------------------\n")

    # ---------------------------------------------------------------------
    # 2) aiStandIns seleccionados o dentro de la jerarquía
    # ---------------------------------------------------------------------
    all_nodes = cmds.listRelatives(sels, ad=True, fullPath=True) or []
    all_nodes += sels  # incluir selección directa

    standins = [n for n in all_nodes if cmds.nodeType(n) == "aiStandIn"]
    if standins:
        print("---- Texturas asociadas a aiStandIns ----")
        
    for s in standins:
        ass_path = cmds.getAttr(s + ".dso")
        print("\naiStandIn:", s)
        print("Asset file:", ass_path)

        tex_dir = get_texture_dir_from_standin(ass_path)
        if not tex_dir:
            print("❌ No se encontró carpeta textures asociada al asset.")
            continue

        print("Texture folder detectada:", tex_dir)
        
        # Buscar texturas en la carpeta
        texture_list = []
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff", "*.exr"]:
            texture_list.extend(glob.glob(os.path.join(tex_dir, ext)))

        if not texture_list:
            print("❌ No se encontraron texturas en:", tex_dir)
            continue

        # Procesar texturas encontradas
        for tex in texture_list:
            print("\nTexture:", tex)
            for status, path in check_single_texture(tex):
                print(" ", "✔" if status == "OK" else "❌", status, "→", path)
    print("check_tx_for_asset")
    print("\n================ FIN ==================\n")