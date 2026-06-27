import maya.cmds as cmds

def move_object_so_pivot_base_is_at_origin():
    selection = cmds.ls(selection=True, long=True)

    if not selection:
        cmds.warning("Selecciona un objeto.")
        return

    obj = selection[0]

    # 1. Bounding box en world space
    bbox = cmds.exactWorldBoundingBox(obj)
    center_x = (bbox[0] + bbox[3]) / 2.0
    base_y   = bbox[1]
    center_z = (bbox[2] + bbox[5]) / 2.0

    # 2. Colocar el pivot en la base central del bounding box
    pivot_ws = [center_x, base_y, center_z]
    cmds.xform(obj, ws=True, pivots=pivot_ws)

    # 3. Obtener coordenadas actuales del pivot en world space
    actual_pivot_ws = cmds.xform(obj, q=True, ws=True, rp=True)

    # 4. Calcular la inversa y mover el objeto
    current_translate = cmds.xform(obj, q=True, ws=True, translation=True)
    new_translate = [
        current_translate[0] - actual_pivot_ws[0],
        current_translate[1] - actual_pivot_ws[1],
        current_translate[2] - actual_pivot_ws[2]
    ]
    cmds.xform(obj, ws=True, translation=new_translate)

    # 5. Freeze Transforms
    cmds.makeIdentity(obj, apply=True, t=True, r=True, s=True, n=0)

    print(f"✅ Objeto '{obj}' centrado y congelado con pivot en la base.")

# Ejecutar
# move_object_so_pivot_base_is_at_origin()
