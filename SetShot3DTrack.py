
###SET SHOT FROM 3D MATCH MOVE

import maya.cmds as cmds
import pymel.core as pm
import os
selCam = cmds.ls( sl=True, sn=True )

if (len(selCam) == 1 and "Cam" in str(selCam)):
    ###Creacion de la nueva camara copiando los atributos de la de MatchMove
    selCamName = str(selCam[0])
    selCamShape = cmds.listRelatives(selCamName, shapes=True)
    cmds.setAttr(selCamShape[0] + ".filmFit", 3)
    OffsetString = selCamShape[0] + "_horizontalFilmOffset"
    try:
        cmds.delete(selCamShape[0] + "_horizontalFilmOffset")
        cmds.delete(selCamShape[0] + "_verticalFilmOffset")
    except:
        print ("No Retime")
    filePath = cmds.file(q=True, sn=True)
    fileBase = os.path.basename(filePath)
    fileName = os.path.splitext(fileBase)[0]

    targetCamName = "_" + fileName + "_RENDER"
    cam = cmds.camera(n=targetCamName);
    cmds.copyAttr(selCamShape,cam[1],inConnections=True,values=True, oc=True, ksc=True);
    NewShutter = cmds.getAttr("locatorFromComp.rotateX")
    cmds.setAttr(str(cam[1]) + ".shutterAngle", NewShutter)
    

    

    ####Parent Constraint antes de hacer un bake
    cmds.parentConstraint( selCam , cam[0], n="temporalConstraint");
    

    ####Bake de camara
    inframe = cmds.playbackOptions(query=True, ast=True);
    outframe = cmds.playbackOptions(query=True, aet=True);
    cmds.bakeResults(cam[0], t=(inframe,outframe));
    cmds.delete("temporalConstraint");
    
    
    ####Creacion de atributos para reencuadre
    cmds.select(cam[0])
    cmds.addAttr( shortName='Reenc_SF', longName='Reencuadre_ScaleFactor', at="float", k=True, defaultValue=1.0 )
    cmds.addAttr( shortName='Reenc_S', longName='Reencuadre_Scale', at="float", k=True, defaultValue=1.0 )
    cmds.addAttr( shortName='Reenc_X', longName='Reencuadre_X', at="float", k=True, defaultValue=0.0 )
    cmds.addAttr( shortName='Reenc_Y', longName='Reencuadre_Y', at="float", k=True, defaultValue=0.0 )
    

    ####Expresiones linkando los atributos de locatorFromComp con la info de reencuadre del copion
    locFromCompScaleFactor = str(cam[0]) + ".Reenc_SF = locatorFromComp.scaleX"
    locFromCompScale = str(cam[0]) + ".Reenc_S = locatorFromComp.translateZ"
    locFromCompTranslateX = str(cam[0]) + ".Reenc_X = locatorFromComp.translateX"
    locFromCompTranslateY = str(cam[0]) + ".Reenc_Y = locatorFromComp.translateY"

    cmds.expression(o=cam[0], s=locFromCompScaleFactor, n="locFromCompScaleFactor")
    cmds.expression(o=cam[0], s=locFromCompScale, n="locFromCompScale")
    cmds.expression(o=cam[0], s=locFromCompTranslateX, n="locFromCompTranslateX")
    cmds.expression(o=cam[0], s=locFromCompTranslateY, n="locFromCompTranslateY")
    

    ###Bake de la info de reencuadre del copion
    cmds.bakeResults(str(cam[0]) + ".Reencuadre_ScaleFactor", t=(inframe,outframe));
    cmds.bakeResults(str(cam[0]) + ".Reencuadre_Scale", t=(inframe,outframe));
    cmds.bakeResults(str(cam[0]) + ".Reencuadre_X", t=(inframe,outframe));
    cmds.bakeResults(str(cam[0]) + ".Reencuadre_Y", t=(inframe,outframe));


    ####Expresiones dentro de los atributos de camara para convertir de pixeles a las unidades de reencuadre de Maya
    ReencuadreScaleExpression = str(cam[1]) + ".postScale = (" + str(cam[0]) + ".Reencuadre_Scale-1) * " + str(cam[0]) + ".Reencuadre_ScaleFactor + (" + str(cam[0]) + ".Reencuadre_ScaleFactor)"
    ReencuadreXExpression = str(cam[1]) + ".horizontalFilmOffset = -((" + str(cam[0])+ ".Reencuadre_X/defaultResolution.width) * " + str(cam[1]) + ".horizontalFilmAperture)/(" + str(cam[0]) + ".Reencuadre_ScaleFactor/(defaultResolution.width/locatorFromComp.scaleY))"
    ReencuadreYExpression = str(cam[1]) + ".verticalFilmOffset = -(" + str(cam[1]) + ".horizontalFilmAperture/defaultResolution.width * (" + str(cam[0]) + ".Reencuadre_Y/2))/(" + str(cam[0]) + ".Reencuadre_ScaleFactor/(defaultResolution.width/locatorFromComp.scaleY))"

    cmds.expression(o=cam[1], s=ReencuadreScaleExpression, n="ReencuadreScaleExpression")
    cmds.expression(o=cam[1], s=ReencuadreXExpression, n="ReencuadreXExpression")
    cmds.expression(o=cam[1], s=ReencuadreYExpression, n="ReencuadreYExpression")
    

    ####Creacion del nuevo Image Plane
    SetImageplane = cmds.imagePlane( name="OVERSCAN_Plane", camera=selCamShape[0] )
    fitString = str(SetImageplane[0]) + ".fit"
    sequenceString = str(SetImageplane[0]) + ".useFrameExtension"
    depthString = str(SetImageplane[0]) + ".depth"
    cmds.setAttr(fitString, 4)
    cmds.setAttr(sequenceString, 1)
    cmds.setAttr(depthString, 10000.0)
    ImagePLaneXExpression = str(SetImageplane[0]) + ".sizeX = " + cam[1] + ".horizontalFilmAperture*1.3"
    ImagePlaneYExpression = str(SetImageplane[0]) + ".sizeY = " + cam[1] + ".verticalFilmAperture*1.3"

    
    cmds.expression(o=SetImageplane[0], s=ImagePLaneXExpression, n="ImagePLaneXExpression")
    cmds.expression(o=SetImageplane[0], s=ImagePlaneYExpression, n="ImagePlaneYExpression")


    

    ####Creacion de Locator con Info de vuelta para Compo
    locToComp = cmds.spaceLocator(n="locatorToComp");
    locToCompScaleFactor = str(locToComp[0]) + ".scaleX = " + str(cam[0]) + ".Reenc_SF"
    locToCompScale = str(locToComp[0]) + ".translateZ = " + str(cam[0]) + ".Reenc_S"
    locToCompTranslateX = str(locToComp[0]) + ".translateX = " + str(cam[0]) + ".Reenc_X"
    locToCompTranslateY = str(locToComp[0]) + ".translateY = " + str(cam[0]) + ".Reenc_Y"
    locToCompCropX = str(locToComp[0]) + ".scaleY = " + "defaultResolution.width"
    locToCompCropY = str(locToComp[0]) + ".scaleZ = " + "defaultResolution.height"
    
    cmds.expression(o=locToComp[0], s=locToCompScaleFactor, n="locToCompScaleFactor")
    cmds.expression(o=locToComp[0], s=locToCompScale, n="locToCompScale")
    cmds.expression(o=locToComp[0], s=locToCompTranslateX, n="locToCompTranslateX")
    cmds.expression(o=locToComp[0], s=locToCompTranslateY, n="locToCompTranslateY")
    cmds.expression(o=locToComp[0], s=locToCompCropX, n="locToCompCropX")
    cmds.expression(o=locToComp[0], s=locToCompCropY, n="locToCompCropY")
    

    ####Cambio de los settings de Resolucion
    cropWidth = cmds.getAttr('locatorFromComp.scaleY')
    cropHeight = cmds.getAttr('locatorFromComp.scaleZ')
    cmds.setAttr("defaultResolution.width", cropWidth)
    cmds.setAttr("defaultResolution.height", cropHeight)
    cmds.setAttr("defaultResolution.deviceAspectRatio" , ((cropWidth/cropHeight)*2))
    cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 0)
    cmds.setAttr("defaultResolution.pixelAspect", 2.0)

    ###Cambio de la camara de Render Settings
    cmds.setAttr("frontShape.renderable", False)
    cmds.setAttr("perspShape.renderable", False)
    cmds.setAttr("sideShape.renderable", False)
    cmds.setAttr("topShape.renderable", False)
    cmds.setAttr(selCamName + ".renderable", False)
    cmds.setAttr(str(cam[0]) + ".renderable", True)
    
    ###Configurar nuevo Rango con Retime
    NewStart = cmds.getAttr('locatorFromCompTime.translateX')
    NewEnd = cmds.getAttr('locatorFromCompTime.translateY')
    cmds.setAttr("defaultRenderGlobals.startFrame", NewStart)
    cmds.setAttr("defaultRenderGlobals.endFrame", NewEnd)
    cmds.playbackOptions(ast=NewStart)
    cmds.playbackOptions(aet=NewEnd)
    


    #### Cambiar a Resolution Gate en el Viewer
    cmds.setAttr(str(cam[0]) + ".displayResolution", 1)
    cmds.setAttr(str(cam[0]) + ".displayFilmGate", 0)
    cmds.setAttr(str(cam[0]) + ".overscan", 1.3)
    if "RETIME" in selCamName:
        cmds.setAttr(selCamName + ".displayResolution", 1)
        cmds.setAttr(selCamName + ".displayFilmGate", 0)
        cmds.setAttr(selCamName + ".overscan", 1.3)



    #### Mover Locators a grupo
    cmds.parent( locToComp, 'NUKEDATA' )


    ###LOCK de atributos
    AttributesCam = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX', '.scaleY', '.scaleZ', '.shearXY', '.shearXZ', '.shearYZ', '.rotateOrder', '.rotateAxisX', '.rotateAxisY', '.rotateAxisZ', '.inheritsTransform']
    AttributesCamShape = ['.horizontalFilmAperture', '.verticalFilmAperture', '.focalLength', '.lensSqueezeRatio', '.fStop', '.focusDistance', '.shutterAngle', '.centerOfInterest', '.motionBlurOverride', '.filmFit', '.filmFitOffset', '.horizontalFilmOffset', '.verticalFilmOffset', '.shakeEnabled', '.horizontalShake', '.verticalShake', '.shakeOverscanEnabled', '.preScale', '.postScale', '.filmTranslateH', '.filmTranslateV', '.horizontalRollPivot', '.verticalRollPivot', '.filmRollValue', '.filmRollOrder', '.postScale','.cameraScale']

    for i in AttributesCam:
        selCamAttributeName = selCamName + i
        RenderAttributeName = cam[0] + i
        LocatorFromCompAttributeName = "locatorFromComp" + i
        LocatorFromCompTimeAttributeName = "locatorFromCompTime" + i
        LocatorToCompAttributeName = str(locToComp[0]) + i
        cmds.setAttr(selCamAttributeName, lock=1)
        cmds.setAttr(RenderAttributeName, lock=1)
        cmds.setAttr(LocatorFromCompAttributeName, lock=1)
        cmds.setAttr(LocatorFromCompTimeAttributeName, lock=1)
        cmds.setAttr(LocatorToCompAttributeName, lock=1)

    for i in AttributesCamShape:
        selCamAttributeName = selCamName + i
        RenderAttributeName = cam[1] + i
        cmds.setAttr(selCamAttributeName, lock=1)
        cmds.setAttr(RenderAttributeName, lock=1)
        
    cmds.parent( cam[0], 'Cameras' )
    pm.lockNode(selCamName)
    pm.lockNode("locatorFromComp")
    pm.lockNode(locToComp)
    pm.lockNode("locatorFromCompTime")
    pm.lockNode(cam)

    ###Creacion de capa de animacion
    cmds.select(clear=True)
    cmds.select(cam)
    cmds.animLayer("Reencuadre", aso=True)
    BaseAnim = cmds.animLayer(query=True, root=True, lock=True)
    cmds.animLayer(BaseAnim, edit=True, lock=True)
    cmds.setKeyframe(cam[0] + ".Reencuadre_X", value=cmds.getAttr("locatorFromComp.translateX", time=1001), time=1001, animLayer="Reencuadre")
    cmds.setKeyframe(cam[0] + ".Reencuadre_Y", value=cmds.getAttr("locatorFromComp.translateY", time=1001), time=1001, animLayer="Reencuadre")
    cmds.setKeyframe(cam[0] + ".Reencuadre_Scale", value=cmds.getAttr("locatorFromComp.translateZ", time=1001), time=1001, animLayer="Reencuadre")
    
    
    ###Hide camara
    cmds.select(clear=True)
    cmds.select(selCamName)
    cmds.hide()
    
    ### MotionBlur Settings
    cmds.select(clear=True)
    cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1)
    cmds.setAttr("defaultArnoldRenderOptions.range_type", 0)
    shutterArnold = "defaultArnoldRenderOptions.motion_frames = locatorFromComp.rotateZ;"
    cmds.expression("defaultArnoldRenderOptions", s=shutterArnold, n="shutterArnold")
    
    
    


    

else:
    if (len(selCam)>1):
        cmds.confirmDialog( title='Errorrrr', message='Selecciona SOLO UNA camara... ', button=['Si,segnor!'], defaultButton='Si,segnor!', cancelButton='Si,segnor!', dismissString='Si,segnor!' )
        print ("Selecciona SOLO UNA camara... ");
    else:
        cmds.confirmDialog( title='Errorrrr', message='Selecciona una camara... ', button=['Si,segnor!'], defaultButton='Si,segnor!', cancelButton='Si,segnor!', dismissString='Si,segnor!' )
        print ("Selecciona una camara... ");