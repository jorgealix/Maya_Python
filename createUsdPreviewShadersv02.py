import maya.cmds as cmds
import maya.mel as mel
import sys, os
import os.path
# getting materials from object
def check_selection():
    global colorFile, specularFile, selected_obj, shapeObj, shading_group, shaders, nodeColor, nodeSpecular, nodeOpacity, nodeMetalness, metalnessFile, metalnessFilename
    global colorFilename, colorFileextension, nodeSpecular, specularFile, specularFilename, specularFileextension, normalFileextension, metalnessFileextension
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

# getting shaders connections from object
def get_shaders():
    shading_group = cmds.listConnections(shapeObj, type ='shadingEngine')
    shaders = cmds.listConnections(str(shading_group[0]) + '.surfaceShader')
    for shader in shaders:
        print(shader, shading_group[0])
        # get color, specular, opacity and normal conections from shader
        nodeColor = cmds.listConnections((shader + '.baseColor'), type='file')
        nodeMetalness = cmds.listConnections((shader + '.metalness'), type='file')
        nodeSpecular = cmds.listConnections((shader + '.specularRoughness'), type='file')
        nodeOpacity = cmds.listConnections((shader + '.opacity'), type='file')
        nodeNormal = cmds.listConnections((shader + '.normalCamera'), type='node')
    
        ## Create Usd Preview shader and connections
        newUsdShaderPreview = cmds.shadingNode('usdPreviewSurface', asShader= True, name = (shader + '_PRV'))
        if nodeColor:
            cmds.connectAttr((nodeColor[0] + '.outColor'), (newUsdShaderPreview + '.diffuseColor'))
        if nodeMetalness:
            cmds.connectAttr((nodeMetalness[0] + '.outAlpha'), (newUsdShaderPreview + '.metallic'))
        if nodeSpecular:
            cmds.connectAttr((nodeSpecular[0] + '.outAlpha'), (newUsdShaderPreview + '.roughness'))
        if nodeOpacity:
            cmds.connectAttr((nodeOpacity[0] + '.outAlpha'), (newUsdShaderPreview + '.opacity'))
        if nodeNormal:
            cmds.connectAttr((nodeNormal[0] + '.outValue'), (newUsdShaderPreview + '.normal'))

        ## Reorder Shader Group Connection
        cmds.disconnectAttr((shader + '.outColor'), (shading_group[0] + '.surfaceShader'))
        cmds.connectAttr((shader + '.outColor'), (shading_group[0] + '.aiSurfaceShader'))
        cmds.connectAttr((newUsdShaderPreview + '.outColor'), (shading_group[0] + '.surfaceShader'))
        mel.eval('generateAllUvTilePreviews;')