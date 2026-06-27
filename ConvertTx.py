import os
import subprocess
import maya.cmds as cmds

def generate_tx_for_scene():
    # Ruta al maketx de Arnold (ajústalo según tu instalación)
    # En Windows normalmente:
    # maketx = r"C:\Program Files\Autodesk\Maya2024\bin\maketx.exe"
    # En Linux/Mac suele estar junto a kick
    maketx = cmds.pluginInfo("mtoa", query=True, path=True)
    if maketx:
        arnold_bin = os.path.dirname(maketx)
        maketx = os.path.join(arnold_bin, "bin", "maketx.exe" if os.name == "nt" else "maketx")
    else:
        cmds.error("No se pudo localizar MtoA ni maketx.")
        return

    print("Usando maketx:", maketx)

    # Busca todos los nodos de textura tipo "file"
    file_nodes = cmds.ls(type="file")
    if not file_nodes:
        print("No hay texturas en la escena.")
        return

    for node in file_nodes:
        tex_path = cmds.getAttr(node + ".fileTextureName")
        if not tex_path:
            continue

        tex_path = os.path.normpath(tex_path)
        if not os.path.exists(tex_path):
            print("❌ No existe:", tex_path)
            continue

        # Calcula ruta del .tx
        folder, name = os.path.split(tex_path)
        base, ext = os.path.splitext(name)
        tx_path = os.path.join(folder, base + ".tx")

        print("→ Generando TX para:", tex_path)
        cmd = [maketx, "-u", "-o", tx_path, tex_path]

        try:
            subprocess.check_call(cmd)
            print("✅ Creado:", tx_path)
        except subprocess.CalledProcessError as e:
            print("⚠️ Error con:", tex_path, " -> ", e)

    print("🎉 Conversión terminada.")

# Ejecutar
generate_tx_for_scene()
