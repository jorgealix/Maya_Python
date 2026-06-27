import maya.cmds as cmds

def set_pivot_to_base_without_moving_object():
    selected = cmds.ls(selection=True, long=True)
    if not selected:
        cmds.warning("Selecciona al menos un objeto.")
        return

    for obj in selected:
        # Guardar posición original del objeto
        original_pos = cmds.xform(obj, query=True, worldSpace=True, translation=True)

        # Obtener el centro de la base del bounding box en world space
        bbox = cmds.exactWorldBoundingBox(obj)
        center_x = (bbox[0] + bbox[3]) / 2.0
        center_z = (bbox[2] + bbox[5]) / 2.0
        bottom_y = bbox[1]

        # Mover el pivot
        cmds.xform(obj, pivots=(center_x, bottom_y, center_z), worldSpace=True)

        # Restaurar la posición original
        cmds.xform(obj, worldSpace=True, translation=original_pos)

    print("✅ Pivot movido a la base del bounding box sin afectar la posición del objeto.")

# USO:
# Selecciona el objeto(s) y ejecuta:
set_pivot_to_base_without_moving_object()
