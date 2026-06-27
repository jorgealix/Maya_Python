import maya.cmds as cmds
import mtoa.aovs as aovs
def setUpAovs():
    aovList = ('ID','N','P','Pref','Z','diffuse','motionvector','sheen','specular','sss','ID_BW','ID_COMISURA_UNHAS','ID_PICO','ID_PIES_PICO_OJO','ID_TAG')
    #aovList = cmds.ls(type="aiAOV")
    #print(aovList)
    cmds.lockNode('initialShadingGroup', lock=False, lu=False)
    cmds.lockNode('initialParticleSE', lock=False, lu=False)
    for passe in aovList:
        print(passe)
        aovs.AOVInterface().addAOV(passe)
