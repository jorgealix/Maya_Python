import maya.cmds as cmds
import os

def exportar_y_reemplazar_por_referencias():
    seleccion = cmds.ls(selection=True, long=False)

    if not seleccion:
        cmds.warning("No hay objetos seleccionados.")
        return

    # Obtener la ruta del proyecto actual
    proyecto = cmds.workspace(q=True, rootDirectory=True)
    ruta_references = os.path.join(proyecto, "scenes", "references")

    # Crear carpeta si no existe
    if not os.path.exists(ruta_references):
        os.makedirs(ruta_references)

    for obj in seleccion:
        nombre_archivo = obj + ".ma"
        ruta_export = os.path.join(ruta_references, nombre_archivo)

        # Asegurarse de que el objeto está seleccionado
        cmds.select(obj, r=True)

        # Exportar como archivo ASCII
        try:
            cmds.file(ruta_export, force=True, options="v=0;", typ="mayaAscii", exportSelected=True)
            print(f"✅ Exportado: {ruta_export}")
        except Exception as e:
            cmds.warning(f"❌ No se pudo exportar {obj}: {str(e)}")
            continue

        # Eliminar el objeto original de la escena
        try:
            cmds.delete(obj)
        except Exception as e:
            cmds.warning(f"❌ No se pudo eliminar {obj}: {str(e)}")
            continue

        # Importar como referencia
        try:
            cmds.file(ruta_export, reference=True, namespace=obj)
            print(f"🔁 Reemplazado por referencia: {obj}")
        except Exception as e:
            cmds.warning(f"❌ No se pudo referenciar {obj}: {str(e)}")

    print("🎉 Todo listo: exportación + sustitución completada.")

# Ejecutar la función
exportar_y_reemplazar_por_referencias()