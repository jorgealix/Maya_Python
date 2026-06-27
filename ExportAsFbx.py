import maya.cmds as cmds
import os

def exportar_fbx_individual():
    seleccion = cmds.ls(selection=True, long=False)

    if not seleccion:
        cmds.warning("No hay objetos seleccionados.")
        return

    # Asegurarse de que el plugin FBX está cargado
    if not cmds.pluginInfo("fbxmaya", query=True, loaded=True):
        try:
            cmds.loadPlugin("fbxmaya")
        except:
            cmds.error("No se pudo cargar el plugin 'fbxmaya'. Asegúrate de que está instalado.")

    # Obtener la ruta del proyecto y carpeta de exportación
    proyecto = cmds.workspace(q=True, rootDirectory=True)
    ruta_references = os.path.join(proyecto, "scenes", "references")

    if not os.path.exists(ruta_references):
        os.makedirs(ruta_references)

    for obj in seleccion:
        nombre_archivo = obj + ".fbx"
        ruta_export = os.path.join(ruta_references, nombre_archivo)

        # Seleccionar el objeto
        cmds.select(obj, r=True)

        # Exportar como FBX
        try:
            cmds.file(ruta_export, force=True, options="v=0;", typ="FBX export", exportSelected=True)
            print(f"✅ Exportado: {ruta_export}")
        except Exception as e:
            cmds.warning(f"❌ No se pudo exportar {obj}: {str(e)}")

    print("🎉 Exportación FBX completada.")

# Ejecutar
exportar_fbx_individual()
