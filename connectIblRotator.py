import maya.cmds as cmds
def connectRotator():
    asset = cmds.ls(selection=True, long=True)
    if not asset:
        cmds.warning(f"❌ Selecciona el root del asset")
        return
    cmds.connectAttr("rotator_loc.rotateY", (str(asset[0]) + ".rotateY"), force=True)
    cmds.setAttr("defaultArnoldRenderOptions.autotx", 0)
    cmds.playbackOptions(min = 1001, max = 1048, animationStartTime = 1001, animationEndTime = 1048)

    # Configurar el ancho a 1920
    cmds.setAttr('defaultResolution.width', 1280)
    cmds.setAttr('defaultResolution.height', 720)
    cmds.setAttr('defaultResolution.pixelAspect', 1.0)
    cmds.setAttr("defaultResolution.deviceAspectRatio", 1.778)
