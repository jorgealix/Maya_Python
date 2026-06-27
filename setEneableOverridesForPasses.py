import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.cmds as cmds
def setenable():
    aovList = cmds.ls(type = "aiAOV")
    print(aovList)
    cmds.lockNode('initialShadingGroup', lock=False, lu=False)
    cmds.lockNode('initialParticleSE', lock=False, lu=False)
    for passe in aovList:
        print(passe)
        visibleLayer = renderSetup.instance().getVisibleRenderLayer()
        col = visibleLayer.renderSettingsCollectionInstance()
        ov = col.createAbsoluteOverride(passe,'enabled')
        ov.setAttrValue(1)