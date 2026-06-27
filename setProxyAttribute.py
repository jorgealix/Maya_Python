import maya.cmds as cmds

def add_bw_groomProxy_attr():
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.warning("No hay objetos seleccionados.")
        return

    for obj in sel:
        # Obtener shape node
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for shp in shapes:
            # Crear atributo si no existe
            if not cmds.attributeQuery("Bw_groomProxy", node=shp, exists=True):
                cmds.addAttr(shp, ln="Bw_groomProxy", at="bool")
                cmds.setAttr(shp + ".Bw_groomProxy", True)
                print("Atributo añadido en:", shp)
            else:
                # Si existe, ponerlo en True igualmente
                cmds.setAttr(shp + ".Bw_groomProxy", True)
                print("Atributo ya existía; valor actualizado en:", shp)


