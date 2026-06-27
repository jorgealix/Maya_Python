import maya.cmds as cmds

def aim_lights_to_locator(locator=None, maintain_offset=False):
    sel = cmds.ls(sl=True, long=True) or []
    if not sel:
        cmds.warning("Selecciona una o varias luces.")
        return

    if locator is None:
        locs = cmds.ls(sl=True, type="transform") or []
        if not locs:
            cmds.warning("Selecciona un locator o pasa su nombre.")
            return
        locator = locs[-1]

    if not cmds.objExists(locator):
        cmds.warning("El locator no existe: {}".format(locator))
        return

    # Si el locator está dentro de la selección, lo quitamos de la lista de luces
    lights = [x for x in sel if x != locator]

    if not lights:
        cmds.warning("No hay luces válidas seleccionadas.")
        return

    for obj in lights:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        is_light = False
        for s in shapes:
            if cmds.nodeType(s).endswith("Light"):
                is_light = True
                break

        if not is_light:
            cmds.warning("{} no parece ser una luz, se omite.".format(obj))
            continue

        try:
            cmds.aimConstraint(
                locator,
                obj,
                mo=maintain_offset,
                aimVector=(0, 0, 1),
                upVector=(0, 1, 0),
                worldUpType="scene"
            )
        except Exception as e:
            cmds.warning("Error con {}: {}".format(obj, e))

# Uso:
# 1) Selecciona varias luces y luego el locator
# 2) Ejecuta:
im_lights_to_locator("locator1")