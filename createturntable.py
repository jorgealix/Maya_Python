import maya.cmds as cmds
import os
import os.path
import maya.mel as mel

'''En esta funcion chequeo que la estructura en la escena y del propia escena sea la correcta,
es decir que contenga los nulls geo, basemesh debajo del nombre del asset'''
global rootNode  # variable que contiene el path de el nodo principal |gato|geo
global rootNodes  # contiene la lista de objetos en el root de la esecna
global minKeyframe, maxKeyframe
global basename
global set_driven = []
mel.eval('global float $MAX;')

def checkCams():
    global cameras  # variable para las camaras de la escena
    global obj
    cameras = cmds.ls(type="camera")
    if 'camMainShape' in cameras:
        obj = 'camMain'
    else:
        ## Create camera turntable
        obj = cmds.camera()
        obj = cmds.rename(obj[0], "turnCam")
        cmds.group(obj, name='rotGrp')
    cmds.setAttr((obj + "Shape.displayFilmGate"), 1)
    cmds.setAttr((obj + "Shape.displayGateMaskOpacity"), 1)
    cmds.setAttr((obj + "Shape.displayGateMaskColor"), 0,0,0, type="double3")
    cmds.setAttr((obj + "Shape.displayResolution"), 1)
    cmds.setAttr((obj + "Shape.overscan"), 1)

def create_playblast():
    keyframes = []
    # Checking Root Structure
    currentScene = os.path.abspath(cmds.file(q=True, sn=True))
    basename = os.path.splitext(os.path.basename(currentScene))[0]
    rootNodes = cmds.ls(type="transform", l=True)  # variable con la lista de objetos de la escena
    minKeyframe = 0
    maxKeyframe = 240
    mel.eval('$MAX = 120;') #python("maxKeyframe");')

    # Check for animations
    anim = False
    #anim_curves = []
    anim_curves = cmds.ls(type=["animCurveUU", "animCurveUA", "animCurveUL", "animCurveUT"])
    
    for node in rootNodes:
        # Loop through all the animated objects and get their animation curves
        curves = cmds.keyframe(node, q=True, name=True)
        print(curves)
        if curves:
            anim_curves.extend(curves)
            anim = True

            # Get a list of all the keyframes from the animation curves
            for curve in anim_curves:
                print(curve)
                keyframes.extend(cmds.keyframe(curve, q=True, timeChange=True))

            # Remove any duplicate keyframes
            keyframes = list(set(keyframes))

            # Sort the keyframes in ascending order
            keyframes.sort()

    ## Reset HUDs
    cmds.headsUpDisplay('HUDCameraName', rem = True)
    cmds.headsUpDisplay(rp=(7, 0))
    cmds.headsUpDisplay('HUDCurrentRate', rem = True)
    cmds.headsUpDisplay(rp=(8, 0))
    cmds.headsUpDisplay('HUDFocalLength', rem = True)
    cmds.headsUpDisplay(rp=(9, 0))
    cmds.headsUpDisplay('HUDPolyTriangles', rem = True)
    cmds.headsUpDisplay(rp=(0, 0))
    cmds.headsUpDisplay('HUDTimeCode', rem = True)
    cmds.headsUpDisplay(rp=(6, 0))

    ## Set up HUDs
    cmds.headsUpDisplay('HUDCameraName', s=7, b=0, ba='center', dw=50, pre='cameraNames')
    cmds.headsUpDisplay('HUDCurrentRate', s=8, b=0, ba='right', dw=50, pre='currentFrame')
    cmds.headsUpDisplay('HUDFocalLength', s=9, b=0, ba='center', dw=50, pre='focalLength')
    cmds.headsUpDisplay('HUDPolyTriangles', l='Triangles:', s=0, b=0, ba='center', dw=50, pre='polyTriangles')
    cmds.headsUpDisplay('HUDTimeCode', s=6, b=0, ba='center', dw=50, pre='sceneTimecode')
    cmds.grid(toggle=0)

    ## Configure interface
    if anim:
        minKeyframe = min(keyframes)
        maxKeyframe = max(keyframes)
        cmds.playbackOptions(animationStartTime=minKeyframe, animationEndTime=maxKeyframe, minTime=minKeyframe, maxTime=maxKeyframe)
        # cmds.setAttr((obj + '.rotate'), -15, 0, 0, type="double3")
        # cmds.setAttr((obj + 'Shape.panZoomEnabled'), 1)
        # cmds.xform('rotGrp', ws=True, rp=[0, 0, 0])
        # cmds.setAttr((obj + 'Shape.zoom'), 0.3)
        #cmds.expression(s='rotGrp.rotateY = 45')
        # cmds.viewFit(obj, allObjects= True, f=1)
        # cmds.setAttr((obj + 'Shape.nearClipPlane'), 1)
        # cmds.setAttr((obj + 'Shape.farClipPlane'), (cmds.getAttr(obj + 'Shape.centerOfInterest') * 2))
    else:
        cmds.playbackOptions(animationStartTime=0, animationEndTime=maxKeyframe, minTime=0, maxTime=maxKeyframe)
        cmds.setAttr((obj + '.rotate'), -15, 45, 0, type="double3")
        cmds.setAttr((obj + 'Shape.panZoomEnabled'), 0)
        cmds.xform('rotGrp', ws=True, rp=[0, 0, 0])
        cmds.setAttr((obj + 'Shape.zoom'), 0.3)
        cmds.expression(s='rotGrp.rotateY = frame * (360/$MAX)')
        cmds.viewFit(obj, allObjects= True, f=1)
        cmds.setAttr((obj + 'Shape.nearClipPlane'), 1)
        cmds.setAttr((obj + 'Shape.farClipPlane'), (cmds.getAttr(obj + 'Shape.centerOfInterest') * 2))

    cmds.lookThru(obj)

    ## Process avi
    projectDirectory = cmds.workspace(q=True, rd=True)

    # playblast  -format qt
    # -filename "movies/bm2_chrout_chr_gato_out_rigging_thinhigh_default_none_out.mov"
    # -sequenceTime 0
    # -clearCache 1
    # -viewer 1
    # -showOrnaments 1
    # -fp 4
    # -percent 100
    # -compression "H.264"
    # -quality 100;
    cmds.playblast(format='qt',
                   filename=(projectDirectory + "/movies/" + basename),
                   startTime=int(minKeyframe),
                   endTime=int(maxKeyframe),
                   width=cmds.getAttr("defaultResolution.width"),
                   height =cmds.getAttr("defaultResolution.height"),
                   offScreen=1,
                   sequenceTime=0,
                   clearCache=1,
                   viewer=1,
                   showOrnaments=1,
                   fp=4,
                   percent=100,
                   compression='H.264',
                   quality=100,
                   fo=1)
    cmds.delete('rotGrp')
    print(minKeyframe, maxKeyframe)
    print(projectDirectory + "/movies/" + basename + ".avi")
    ## Revert HUDs
    cmds.headsUpDisplay('HUDFocalLength', rem=True)
    cmds.headsUpDisplay('HUDCameraName', rem=True)
    cmds.headsUpDisplay('HUDCurrentRate', rem=False)
    cmds.headsUpDisplay('HUDPolyTriangles', rem=True)
    cmds.headsUpDisplay('HUDTimeCode', rem=False)
    ## Reset HUDs
    cmds.headsUpDisplay(rp=(7, 0))
    cmds.headsUpDisplay(rp=(8, 0))
    cmds.headsUpDisplay(rp=(9, 0))
    cmds.headsUpDisplay(rp=(0, 0))
    cmds.headsUpDisplay(rp=(6, 0))
    cmds.grid(toggle=1)

checkCams()
create_playblast()