import maya.cmds as cmds
import os.path

def setProj():
    currentScene = os.path.abspath(cmds.file(q=True, sn=True))
    currentProj = os.path.split(currentScene)
    if currentProj[0]:
        print(currentProj[0].replace('\\','/'))
        currentProj = os.path.split(currentProj[0])
        cmds.workspace(str(currentProj[0]), openWorkspace=True )
    else:
        print("No scene directory exist, set project manually")