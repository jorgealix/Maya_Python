# getting materials from object
import maya.cmds as cmds
import maya.mel as mel
import sys, os
import os.path
def check_selection():
    global colorFile, specularFile, selected_obj, shapeObj, shading_group, shaders, nodeColor, nodeSpecular, nodeOpacity
    global colorFilename, colorFileextension, nodeSpecular, specularFile, specularFilename, specularFileextension, normalFileextension
    colorFile = specularFile = ''
    selected_obj = cmds.ls(selection=True)
    if not selected_obj:
        print("Select an object")
    if len(selected_obj) == 1:
        shapeObj = cmds.listRelatives(selected_obj, shapes=True)
        if shapeObj[0]:
            shape_type = cmds.objectType(shapeObj[0])
            if "mesh" in shape_type:
                get_shaders()
            else:
                cmds.warning('Select the object to analize')
                cmds.confirmDialog(title='Confirm', message='Select a geometry object to analize', button=['Confirm'], backgroundColor=[1.0, 0.75, 0.25])
        else:
            cmds.warning('Select the object to analize')
            cmds.confirmDialog(title='Confirm', message='Select a geometry object to analize', button=['Confirm'], backgroundColor=[1.0, 0.75, 0.25])
    else:
        cmds.warning( 'Select the object to analize')
        cmds.confirmDialog( title='Confirm', message='Select just one geometry object to analize', button=['Confirm'], backgroundColor = [1.0,0.75,0.25])

def get_shaders():
    shading_group = cmds.listConnections(shapeObj, type ='shadingEngine')
    shaders = cmds.listConnections(str(shading_group[0]) + '.surfaceShader')
    for shader in shaders:
        print(shader, shading_group[0])
        # get color, specular, opacity and normal conections from shader
        nodeColor = cmds.listConnections((shader + '.baseColor'), type='file')
        nodeSpecular = cmds.listConnections((shader + '.specularRoughness'), type='file')
        nodeOpacity = cmds.listConnections((shader + '.opacity'), type='file')
        nodeNormal = cmds.listConnections((shader + '.normalCamera'), type='node')

        if nodeColor:
           colorFile = cmds.getAttr("%s.fileTextureName" % nodeColor[0])
           colorFilename, colorFileextension = os.path.splitext(colorFile)
           if '<u>' in colorFilename and '<v>' in colorFilename:
               colorFilename = colorFilename.replace('<u>', '0')
               colorFilename = colorFilename.replace('<v>', '0')
               print(colorFilename)
               for ext in ['.exr', '.png', '.tif', '.jpg']:
                   if os.path.isfile(colorFilename + ext) is True:
                        previsColorFile = (colorFilename + ext)
                        previsColorTxt = cmds.shadingNode('file', asTexture=True, name=(nodeColor + '_PRV'))
                        cmds.setAttr((previsColorTxt + '.fileTextureName'), previsColorTxt)
                        print(previsColorFile)

        if nodeSpecular:
           specularFile = cmds.getAttr("%s.fileTextureName" % nodeSpecular[0])
           specularFilename, specularFileextension = os.path.splitext(specularFile)
           if '<u>' in specularFilename and '<v>' in specularFilename:
               specularFilename = specularFilename.replace('<u>', '0')
               specularFilename = specularFilename.replace('<v>', '0')
               for ext in ['.exr', '.png', '.tif', '.jpg']:
                   if os.path.isfile(specularFilename + ext) is True:
                        previsSpeculaFile = (specularFilename + ext)
                        print(previsSpeculaFile)
                        
        if nodeOpacity:
           opacityFile = cmds.getAttr("%s.fileTextureName" % nodeOpacity[0])
           opacityFilename, opacityFileextension = os.path.splitext(opacityFile)
           if '<u>' in opacityFilename and '<v>' in opacityFilename:
               opacityFilename = opacityFilename.replace('<u>', '0')
               opacityFilename = opacityFilename.replace('<v>', '0')
               for ext in ['.exr', '.png', '.tif', '.jpg']:
                   if os.path.isfile(opacityFilename + ext) is True:
                        previsOpacityFile = (opacityFilename + ext)
                        print(previsOpacityFile)
        
        ''' Crear Usd Preview shader and conections'''
        newUsdShaderPreview = cmds.shadingNode('usdPreviewSurface', asShader= True, name = (shader + '_PRV'))
        if nodeColor:
            cmds.connectAttr((nodeColor[0] + '.outColor'), (newUsdShaderPreview + '.diffuseColor'))
        if nodeSpecular:
            cmds.connectAttr((nodeSpecular[0] + '.outAlpha'), (newUsdShaderPreview + '.roughness'))
        if nodeOpacity:
            cmds.connectAttr((nodeOpacity[0] + '.outAlpha'), (newUsdShaderPreview + '.opacity'))
        if nodeNormal:
            cmds.connectAttr((nodeNormal[0] + '.outValue'), (newUsdShaderPreview + '.normal'))
        print("UsdPreviewShader created for: ", shader, "==>Shader Group Connections uppdated.")

        '''Reorder Shader Group Connection'''
        cmds.disconnectAttr((shader + '.outColor'), (shading_group[0] + '.surfaceShader'))
        cmds.connectAttr((shader + '.outColor'), (shading_group[0] + '.aiSurfaceShader'))
        cmds.connectAttr((newUsdShaderPreview + '.outColor'), (shading_group[0] + '.surfaceShader'))
        mel.eval('generateAllUvTilePreviews;')

def createBBox():
    
    if selected_obj:
        bb = cmds.exactWorldBoundingBox(selected_obj[0])
        # bb = [xmin, ymin, zmin, xmax, ymax, zmax]
        x = (bb[0] + bb[3]) / 2.0
        y = (bb[1] + bb[4]) / 2.0
        z = (bb[2] + bb[5]) / 2.0
        w = bb[3] - bb[0]
        h = bb[4] - bb[1]
        d = bb[5] - bb[2]
        bbox = cmds.polyCube(width=w, height=h, depth=d, name=selected_obj[0] + "_BBOX")[0]
        cmds.move(x, y, z, bbox, absolute=True)
        print("Bounding box created:", bbox)
    else:
        print("First select the asset root.")