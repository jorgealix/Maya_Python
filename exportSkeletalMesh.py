import maya.cmds as cmds
import maya.mel as mm
import os.path

def missingWarning():
    if len(skComponnents) != 2:
        cmds.warning( "!!Select a Root Joint and a Mesh to export the Skeletal Mesh¡¡" )
        cmds.confirmDialog(title='Miising Objects', message="!!Select a Root Joint and a Mesh to export the Skeletal Mesh¡¡")

def exportSkeletalMesh(clipName, clipStart, clipEnd):
    global skComponnents
    currentScene = os.path.abspath(cmds.file(q=True, sn=True))
    pathFile, fileName = os.path.split(currentScene)
    fileName = fileName.split('.')
    pathFile = pathFile.replace("\\", "/")
    pathClip = pathFile.replace('scenes', 'data/')
    cmds.playbackOptions(ast=clipStart, aet=clipEnd)

    fileName = (fileName[0] + '_' + clipName + '.fbx')
    exportedFile = (pathClip + fileName)
    newComps = []
    skComponnents = cmds.ls(sl=True)
    print(len(skComponnents))
    if len(skComponnents) != 2:
        missingWarning()
        print("!!Select a Root Joint and a mesh to export de Skeletal Mesh¡¡")
    else:
        for comp in skComponnents:
            ##dupComp = cmds.duplicate(comp, inputConnections=True, name=comp, returnRootsOnly=True)
            ##dupComp = cmds.parent(dupComp, w=True)
            rootNode = cmds.listRelatives( comp, allParents=True )
            dupComp = cmds.parent(comp, w=True)
            #dupComp = cmds.rename(dupComp[0],dupComp[0][:-1])
            newComps.append(dupComp)
        print( newComps)
        cmds.select(newComps[0],newComps[1] )
        # clipStart, clipEnd = (0, 50)
        mm.eval('FBXExportSkins  -v true;')
        mm.eval('FBXExportShapes -v true;')
        mm.eval('FBXExportAnimationOnly -v false;')
        mm.eval('FBXExportSkeletonDefinitions -v false;')
        mm.eval('FBXExportSmoothingGroups -v true;')
        mm.eval('FBXExportSmoothMesh -v true;')
        mm.eval('FBXExportBakeComplexStart -v 0;')
        mm.eval('FBXExportBakeComplexEnd -v 0;')
        mm.eval('FBXExportBakeComplexAnimation -v true;')
        mm.eval('FBXExportIncludeChildren -v true;')
        mm.eval('FBXExportInputConnections -v false;')
        commandExport = ("FBXExport -f " + '"' + str(exportedFile) + '"' + " -s;")
        print(commandExport)
        mm.eval(str(commandExport))
        #cmds.delete(newComps)
        cmds.parent(skComponnents,rootNode)