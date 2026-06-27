# getting materials from object
import maya.cmds as cmds
import maya.mel as mel
import sys, os
import os.path
def check_selection():
    global colorFile, specularFile, selected_obj, shapeObj, shading_group, shaders, nodeColor, nodeSpecular
    global colorFilename, colorFileextension, nodeSpecular, specularFile, specularFilename, specularFileextension
    colorFile = specularFile = ''
    selected_obj = cmds.ls(selection=True)
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
        # get color base and specular from shaders
        nodeColor = cmds.listConnections((shader + '.baseColor'), type='file')
        nodeSpecular = cmds.listConnections((shader + '.specularRoughness'), type='file')
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
        ''' Crear Blinn shader for preview and reorder conections'''
        newShaderPreview = cmds.shadingNode('blinn', asShader= True, name = (shader + '_PRV'))
        if nodeColor:
            cmds.connectAttr((nodeColor[0] + '.outColor'), (newShaderPreview + '.color'))
        if nodeSpecular:
            cmds.connectAttr((nodeSpecular[0] + '.outColor'), (newShaderPreview + '.specularColor'))
        cmds.disconnectAttr((shader + '.outColor'), (shading_group[0] + '.surfaceShader'))
        cmds.connectAttr((shader + '.outColor'), (shading_group[0] + '.aiSurfaceShader'))
        cmds.connectAttr((newShaderPreview + '.outColor'), (shading_group[0] + '.surfaceShader'))
        mel.eval('generateAllUvTilePreviews;')