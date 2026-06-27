import maya.cmds as cmds
def renameSG():
    global ShaderGroups
    ShaderGroups = []
    shapes = cmds.ls(sl=True, shapes=True, dag=True)
    ShaderGroups = list(set(cmds.listConnections(shapes, type='shadingEngine')))
    sel = cmds.ls(sl=True, tr=True)
    if sel:
        for shaderGroup in ShaderGroups:
            if shaderGroup != 'initialShadingGroup':
                mat = cmds.ls(cmds.listConnections(shaderGroup), materials=True)
                shaderGroup = cmds.rename(shaderGroup, (mat[0] + 'SG'))
        cmds.confirmDialog(t="Done", message='ShaderGroup Names Fixed.', icon="Done")
    else:
        cmds.confirmDialog(t="Oops! Nothing Selected", message='Oops! Nothing Selected.', icon="warning")