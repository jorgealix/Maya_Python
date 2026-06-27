import maya.cmds as cmds
import os.path
def setProj():
    selection = cmds.ls(sl=True)
    if len(selection) != 1:
        cmds.warning( "!!Select a Root node from asset¡¡" )
        cmds.confirmDialog(title='Miising selection', message="!!Select a Root node from asset¡¡")
    else:
        currentScene = os.path.abspath(cmds.file(q=True, sn=True))
        currentProj = os.path.split(currentScene)
        if 'scenes' in currentProj[0]:
            usdfile = currentProj[0]+'\\usd\\'+currentProj[1].replace('.ma','.usd')
        else:
            usdfile = currentProj[0] + '\\usd\\' + currentProj[1].replace('.ma', '.usd')
        cmds.mayaUSDExport(file=usdfile,
                selection=True,
                exportUVs=True,
                exportSkels='none',
                exportSkin='none',
                exportBlendShapes=False,
                exportDisplayColor=False,
                exportColorSets=True,
                exportComponentTags=True,
                defaultMeshScheme='catmullClark',
                frameRange=[0,0],
                eulerFilter=False,
                staticSingleSample=False,
                frameStride=1,
                defaultUSDFormat='usda',
                parentScope='geo',
                shadingMode='useRegistry',
                convertMaterialsTo=['UsdPreviewSurface'],
                exportRelativeTextures='automatic',
                exportInstances=True,
                exportVisibility=True,
                mergeTransformAndShape=True,
                stripNamespaces=True,
                worldspace=False,
                jobContext=['None'],
                excludeExportTypes=['Cameras'])
        print('Export usd file: ',usdfile)