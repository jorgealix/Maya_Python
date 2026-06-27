import maya.cmds as cmds
import maya.mel as mel
import sys, os, math
#import os.path
# Creamos las listas de atributos y diccionarios
usdShAttr = ('clearcoat',
            'clearcoatRoughness',
            'diffuseColor',
            'displacement',
            'emissiveColor',
            'ior',
            'metallic',
            'normal',
            'occlusion',
            'opacity',
            'opacityThreshold',
            'roughness',
            'specularColor',
            'useSpecularWorkflow')
lambertShAttrDict = {'diffuseColor': 'color',
                    'emissiveColor': 'incandescence',
                    'ior': 'refractiveIndex',
                    'metallic': 'diffuse',
                    'normal': 'normalCamera',
                    'occlusion': 'ambientColor',
                    'opacity': 'transparency',
                    'opacityThreshold': 'translucence'}
phongShAttrDict = {'diffuseColor': 'color',
                    'emissiveColor': 'incandescence',
                    'ior': 'refractiveIndex',
                    'metallic': 'diffuse',
                    'normal': 'normalCamera',
                    'occlusion': 'ambientColor',
                    'opacity': 'transparency',
                    'OpacityThreshold': 'translucence',
                    'roughness':'reflectionSpecularity',
                    'specularColor':'specularColor'}
blinnShAttrDict = {'diffuseColor': 'color',
                    'emissiveColor': 'incandescence',
                    'ior': 'refractiveIndex',
                    'metallic': 'diffuse',
                    'normal': 'normalCamera',
                    'opacity': 'transparency',
                    'OpacityThreshold': 'translucence',
                    'roughness':'reflectionSpecularity',
                    'specularColor':'specularColor'}
aiShAttrDict = {'clearcoat':'coat',
                'clearcoatRoughness':'coatRoughness',
                'diffuseColor': 'baseColor',
                'emissiveColor': 'emissionColor',
                'ior': 'specularIOR',
                'metallic': 'metalness',
                'normal': 'normalCamera',
                'opacity': 'opacity',
                'opacityThreshold': 'transmission',
                'roughness':'specularRoughness',
                'specularColor':'specularColor'}

def is_shading_engine(node):
    # Check if the node is a shading engine
    return cmds.nodeType(node) in ["aiStandardSurface", "lambert", "phong", "blinn"]

def checkSelSh():
    # Check the selection
    global selected_node
    selected_node = cmds.ls(selection=True)
    # Check selection
    if selected_node:
        if is_shading_engine(selected_node[0]):
            if cmds.nodeType(selected_node[0]) == "aiStandardSurface":
                aiToUsd()
            if cmds.nodeType(selected_node[0]) == "lambert":
                lambertToUsd()
            if cmds.nodeType(selected_node[0]) == "phong":
                phongToUsd()
            if cmds.nodeType(selected_node[0]) == "blinn":
                blinToUsd()
        else:
            print(f"{selected_node[0]} is not a shading engine. Select a valid shading engine")
            cmds.confirmDialog(t="Oops! is not a shading engine.",
                               message='Oops! Only valid shading engines: aiStandardSurface, lambert, phong, blinn',
                               icon="warning")
    else:
        cmds.confirmDialog(t="Oops! Nothing Selected.",
                           message='Oops! Please, select a Shading Engine',
                           icon="warning")
        print("Select a node.")

def aiToUsd():
    # Create usdShader and switch new connections
    global usdSh, attr, nodeConnected, attrValue, attrType, lengthAttr, attrUsdType, normalized_value
    usdSh = cmds.shadingNode('usdPreviewSurface', asShader=True, name=(f'{selected_node[0]}_usdPw'))
    cmds.setAttr((f'{usdSh}.useSpecularWorkflow'), True)
    cmds.setAttr((f'{usdSh}.roughness'), 0.001)
    cmds.connectAttr((usdSh + '.outColor'), f'{selected_node[0]}SG.surfaceShader', force=True)
    cmds.connectAttr((f'{selected_node[0]}.outColor'), f'{selected_node[0]}SG.aiSurfaceShader', force=True)
    # Connect textures to usdShader or assign values
    for attr in usdShAttr:
        if attr in aiShAttrDict:
            # Buscamos en el diccionario que correspondencia hay con los attributos soportados
            nodeConnected = cmds.listConnections(f"{selected_node[0]}.{aiShAttrDict.get(attr)}", source=True,
                                                 destination=False, plugs=True)
            if not nodeConnected is None:
                # y los conectamos al nuevo usdShader
                cmds.connectAttr(nodeConnected[0], (f'{usdSh}.{attr}'), force=True)
            else:
                # si no tiene mapa le copiamos el valor del atributo equivalente
                checkInterpolation()
                print(selected_node[0] + '.' + aiShAttrDict.get(attr) + ' is ' + str(cmds.getAttr(
                    selected_node[0] + '.' + aiShAttrDict.get(
                        attr))))
                attrValue = cmds.getAttr(selected_node[0] + '.' + aiShAttrDict.get(attr))
                attrType = cmds.getAttr(selected_node[0] + '.' + aiShAttrDict.get(attr), type=True)
                attrUsdType = cmds.getAttr((f'{usdSh}.{attr}'), type=True)
                if attrType == 'float3':
                    lengthAttr = math.sqrt(sum(math.pow(v, 2) for v in attrValue[0]))
                    lengthAttr = (lengthAttr - 0) / 1.7320508075688772
                    print(lengthAttr)
                #print(attr, str(attrUsdType), type(attrValue), str(attrType))
                # Si el tipo de valor es diferente lo convertimos

                if attrUsdType == 'float' and attrType == 'float':
                    print(attrType, attrUsdType, 'both are float')
                    try:
                        cmds.setAttr((f'{usdSh}.{attr}'), lerp(minLerp, maxLerp, attrValue))
                    except:
                        cmds.setAttr((f'{usdSh}.{attr}'), lerp(minLerp, maxLerp, clamp(attrValue, 0.001, 1)))

                elif attrUsdType == 'float' and attrType == 'float3':
                    print(attrType, attrUsdType, 'destination is float')
                    try:
                        cmds.setAttr((f'{usdSh}.{attr}'), lerp(minLerp, maxLerp, lengthAttr))
                    except:
                        cmds.setAttr((f'{usdSh}.{attr}'), lerp(minLerp, maxLerp, clamp(lengthAttr, 0.001, 1)))

                elif attrUsdType == 'float3' and attrType == 'float3':
                    print(attrType, attrUsdType, 'both are float3')
                    try:
                        cmds.setAttr((f'{usdSh}.{attr}'),
                                     lerp(minLerp, maxLerp, clamp(attrValue[0][0]),0, 1),
                                     lerp(minLerp, maxLerp, clamp(attrValue[0][1]),0, 1),
                                     lerp(minLerp, maxLerp, clamp(attrValue[0][2]),0, 1),
                                     type=attrType)
                    except:
                        cmds.setAttr((f'{usdSh}.{attr}'),
                                    lerp(minLerp, maxLerp, clamp(attrValue[0][0], 0.001, 1)),
                                    lerp(minLerp, maxLerp, clamp(attrValue[0][1], 0.001, 1)),
                                    lerp(minLerp, maxLerp, clamp(attrValue[0][2], 0.001, 1)),
                                    type=attrType)
def checkInterpolation():
    global maxLerp, minLerp
    minLerp = 0
    maxLerp = 1
    if attr == 'emissiveColor':
        minLerp = 1
        maxLerp = 0
    elif attr == 'opacity':
        minLerp = 1
        maxLerp = 0
    elif attr == 'opacityThreshold ':
        minLerp = 1
        maxLerp = 0
    print('range lerp', minLerp, maxLerp)

def lambertToUsd():
    # Create usdShader and switch new connections
    global usdSh, attr, nodeConnected, attrValue, attrType, lengthAttr
    usdSh = cmds.shadingNode('usdPreviewSurface', asShader = True, name = (f'{selected_node[0]}_usdPw'))
    cmds.setAttr((f'{usdSh}.useSpecularWorkflow'), True)
    cmds.setAttr((f'{usdSh}.roughness'), 0.001)
    cmds.connectAttr((usdSh + '.outColor'), f'{selected_node[0]}SG.surfaceShader', force = True)
    cmds.connectAttr((f'{selected_node[0]}.outColor'), f'{selected_node[0]}SG.aiSurfaceShader', force = True)
    # Connect textures to usdShader or assign values
    for attr in usdShAttr:
        if attr in lambertShAttrDict:
            # Buscamos en el diccionario que correspondencia hay con los attributos soportados y los conectamos al nuevo usdShader
            nodeConnected = cmds.listConnections(f"{selected_node[0]}.{lambertShAttrDict.get(attr)}", source=True, destination=False, plugs=True)
            if not nodeConnected is None:
                cmds.connectAttr(nodeConnected[0], (f'{usdSh}.{attr}'), force = True)
            else:
                print(selected_node[0] + '.' + lambertShAttrDict.get(attr) + ' is ' + str(cmds.getAttr(selected_node[0] + '.' + lambertShAttrDict.get(attr)))) # + str(cmds.getAttr(selected_node[0] + lambertShAttrDict.get(attr))))
                attrValue = cmds.getAttr(selected_node[0] + '.' + lambertShAttrDict.get(attr))
                attrType = cmds.getAttr(selected_node[0] + '.' + lambertShAttrDict.get(attr), type =True)
                print( type(attrValue), str(attrType))
                if attrType == 'float':
                    cmds.setAttr((f'{usdSh}.{attr}'), attrValue)
                if attrType == 'float3':
                    try:
                        cmds.setAttr((f'{usdSh}.{attr}'), attrValue[0][0], attrValue[0][1], attrValue[0][2], type = attrType)
                    except:
                        lengthAttr = math.sqrt(sum(math.pow(v, 2) for v in attrValue[0]))
                        cmds.setAttr((f'{usdSh}.{attr}'), lengthAttr)
                        if attr == 'occlusion':
                            cmds.setAttr((f'{usdSh}.occlusion'), (lerp(1, 0, lengthAttr)))
                            print('oclussion')
                        if attr == 'opacity':
                            cmds.setAttr((f'{usdSh}.opacity'), (lerp(1, 0, lengthAttr)))
                            print('opacity')
            #print(f'{selected_node[0]}.{attr}" is {nodeConnected[0]}')

def lerp(a, b, t):
    # Linear interpolation formula
    return (a + t * (b - a))
def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n
def phongToUsd():
    # Create usdShader and switch new connections
    global usdSh, attr, nodeConnected
    usdSh = cmds.shadingNode('usdPreviewSurface', asShader = True, name = (f'{selected_node[0]}_usdPw'))
    cmds.connectAttr((usdSh + '.outColor'), f'{selected_node[0]}SG.surfaceShader', force = True)
    cmds.connectAttr((f'{selected_node[0]}.outColor'), f'{selected_node[0]}SG.aiSurfaceShader', force = True)
    # Connect textures to usdShader or assign values
    for attr in usdShAttr:
        if attr in phongShAttrDict:
            # Buscamos en el diccionario que correspondencia hay con los attributos soportados y los conectamos al nuevo usdShader
            nodeConnected = cmds.listConnections(f"{selected_node[0]}.{phongShAttrDict.get(attr)}", source=True, destination=False, plugs=True)
            if not nodeConnected is None:
                cmds.connectAttr(nodeConnected[0], (f'{usdSh}.{attr}'), force = True)
                #print(f'{selected_node[0]}.{attr}" is {nodeConnected[0]}')
def blinnToUsd():
    # Create usdShader and switch new connections
    global usdSh, attr, nodeConnected
    usdSh = cmds.shadingNode('usdPreviewSurface', asShader = True, name = (f'{selected_node[0]}_usdPw'))
    cmds.connectAttr((usdSh + '.outColor'), f'{selected_node[0]}SG.surfaceShader', force = True)
    cmds.connectAttr((f'{selected_node[0]}.outColor'), f'{selected_node[0]}SG.aiSurfaceShader', force = True)
    # Connect textures to usdShader or assign values
    for attr in usdShAttr:
        if attr in blinnShAttrDict:
            # Buscamos en el diccionario que correspondencia hay con los attributos soportados y los conectamos al nuevo usdShader
            nodeConnected = cmds.listConnections(f"{selected_node[0]}.{blinnShAttrDict.get(attr)}", source=True, destination=False, plugs=True)
            if not nodeConnected is None:
                cmds.connectAttr(nodeConnected[0], (f'{usdSh}.{attr}'), force = True)
                #print(f'{selected_node[0]}.{attr}" is {nodeConnected[0]}')

