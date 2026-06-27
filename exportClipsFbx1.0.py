import maya.cmds as cmds
import maya.mel as mm
import os.path
def exportAnimationClips(clipName, clipStart, clipEnd):
    currentScene = os.path.abspath(cmds.file(q=True, sn=True))
    pathFile, fileName  = os.path.split(currentScene)
    fileName = fileName.split('.')
    pathFile = pathFile.replace("\\","/")
    pathClip = pathFile.replace('scenes', 'clips/')
    cmds.playbackOptions(ast = clipStart, aet = clipEnd )

    fileName = (fileName[0] + '_' + clipName + '.fbx')
    exportedFile = (pathClip + fileName)

    rootSel = cmds.ls(sl = True)
    rootSelParts = rootSel[0].split('|')

    dupNode = cmds.duplicate(rootSel, inputConnections=True, name=rootSelParts[1], returnRootsOnly=True)
    cmds.parent(dupNode, w = True)
    dupNode = cmds.rename(dupNode, rootSelParts[1])
    jointHierarchy = cmds.select(dupNode, hierarchy = True)

    #clipStart, clipEnd = (0, 50)
    mm.eval('FBXExportBakeComplexStart -v ' + str(clipStart) + ';')
    mm.eval('FBXExportBakeComplexEnd -v ' + str(clipEnd) + ';')
    mm.eval('FBXExportBakeComplexAnimation -v true;')
    mm.eval('FBXExportInputConnections -v false;')
    commandExport = ("FBXExport -f "  + '"' +  str(exportedFile) + '"' + " -s;")
    print(commandExport)
    mm.eval(str(commandExport))
    cmds.delete(dupNode)

exportAnimationClips("testJorge", 0, 50)