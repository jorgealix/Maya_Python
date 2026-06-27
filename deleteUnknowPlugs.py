import maya.cmds as cmds
import maya.mel as mm
def createPropStructure():
    oldplugins = cmds.unknownPlugin(q=True, list=True)
    print(oldplugins)
    for plugin in oldplugins:
        cmds.unknownPlugin(plugin, remove=True)