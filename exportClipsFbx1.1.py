import maya.cmds as cmds
import maya.mel as mm
import os.path

def closeButtonPush(*args):
    command = cmds.deleteUI(ClipWindow)

def exportButtonPush(*args):
    global ClipWindow, clipName, clipStart, clipEnd
    clipName = cmds.textField(clipName, q=True, text=True)
    clipStart = cmds.textField(clipStart, q=True, text=True)
    clipEnd = cmds.textField(clipEnd, q=True, text=True)
    command = exportAnimationClips(clipName, clipStart, clipEnd)

def exportAnimationClips(clipName, clipStart, clipEnd):
    currentScene = os.path.abspath(cmds.file(q=True, sn=True))
    pathFile, fileName = os.path.split(currentScene)
    fileName = fileName.split('.')
    pathFile = pathFile.replace("\\", "/")
    pathClip = pathFile.replace('scenes', 'clips/')
    cmds.playbackOptions(ast=clipStart, aet=clipEnd)

    fileName = (fileName[0] + '_' + clipName + '.fbx')
    exportedFile = (pathClip + fileName)

    rootSel = cmds.ls(sl=True)
    rootSelParts = rootSel[0].split('|')

    dupNode = cmds.duplicate(rootSel, inputConnections=True, name=rootSelParts[1], returnRootsOnly=True)
    cmds.parent(dupNode, w=True)
    dupNode = cmds.rename(dupNode, rootSelParts[1])
    jointHierarchy = cmds.select(dupNode, hierarchy=True)

    # clipStart, clipEnd = (0, 50)
    mm.eval('FBXExportBakeComplexStart -v ' + str(clipStart) + ';')
    mm.eval('FBXExportBakeComplexEnd -v ' + str(clipEnd) + ';')
    mm.eval('FBXExportBakeComplexAnimation -v true;')
    mm.eval('FBXExportInputConnections -v false;')
    commandExport = ("FBXExport -f " + '"' + str(exportedFile) + '"' + " -s;")
    print(commandExport)
    mm.eval(str(commandExport))
    cmds.delete(dupNode)

def createUI():
    if (cmds.window("ClipWindow", exists=True)):
        cmds.deleteUI("ClipWindow")
    cmds.window("ClipWindow", title="Export Clip", iconName='ExFBX', widthHeight=(200, 150))
    cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 100)])
    cmds.text(label='Clip Name')
    clipName = cmds.textField()
    cmds.text(label='Start Frame')
    clipStart = cmds.textField()
    cmds.text(label='End Frame')
    clipEnd = cmds.textField()
    cmds.button(label='Export FBX', command=exportButtonPush)
    cmds.button(label='Close', command=closeButtonPush)

    #    Attach commands to pass focus to the next field if the Enter
    #    key is pressed. Hitting just the Return key will keep focus
    #    in the current field.

    cmds.textField(clipName, edit=True, enterCommand=('cmds.setFocus(\"' + clipStart + '\")'))
    cmds.textField(clipStart, edit=True, enterCommand=('cmds.setFocus(\"' + clipEnd + '\")'))
    cmds.textField(clipEnd, edit=True, enterCommand=('cmds.setFocus(\"' + clipName + '\")'))

    cmds.showWindow(ClipWindow)