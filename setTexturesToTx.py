import maya.cmds as cmds
import maya.mel as mel
import os.path
allFileNodes = cmds.ls(type = "file")
for f in allFileNodes:
    getCurrentImagePath = cmds.getAttr("%s.fileTextureName"%f)
    extension = os.path.splitext(getCurrentImagePath)[1]
    cmds.setAttr("%s.aiAutoTx"%f, 0)
    print(f, extension)
    if extension is not ".tx":
        newPath = getCurrentImagePath.replace(extension,".tx")
        cmds.setAttr("%s.fileTextureName"%f,newPath, type = "string")
        cmds.setAttr("%s.colorSpace"%f, 'Utility - Raw', type='string')