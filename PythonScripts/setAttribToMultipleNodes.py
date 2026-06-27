import maya.cmds as cmds
assList = cmds.ls(selection = True)
for ass in assList:
    cmds.setAttr((ass + ".overrideEnabled") , 1)
    cmds.setAttr((ass + ".overrideLevelOfDetail") , 1)