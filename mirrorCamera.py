import maya.mel as mel
import maya.cmds as cmds
import os
def mirroringrcam():
    startframe = cmds.playbackOptions(query=True, minTime=True)
    endframe = cmds.playbackOptions(query=True, maxTime=True)
    current_project_path = cmds.workspace(q=True, rd=True)
    normalized_path = os.path.normpath(current_project_path)
    path_components = normalized_path.split(os.sep)
    cam = cmds.ls(selection=True)
    rootSceneNode = cmds.listRelatives(  allParents=True )
    cmds.setAttr((rootSceneNode[0] + '.scaleX'), -1 )
    mirrorCam = cmds.duplicate(cam[0], name = (cam[0].replace('_camMain', 'mirror_camMain')), returnRootsOnly = True)
    cmds.parent(mirrorCam, world = True)
    constraint = cmds.parentConstraint( cam, mirrorCam )
    cmds.setAttr((str(mirrorCam[0]) + '.scaleZ'), 1 )
    cmds.setAttr((str(constraint[0]) + '.target[0].targetOffsetRotateX'), 180 )
    cmds.bakeResults( cam[0],
                            time = (startframe,endframe),
                            sampleBy=1,
                            simulation = True,
                            attribute = ["tx","ty","tz","rx","ry","rz"], hi="below" )
    camgroup = cmds.group(mirrorCam, name = 'mirror_cam')
    cmds.rename(cam[0], cam[0].replace('camMain', 'old' ))
    cmds.rename(mirrorCam[0], mirrorCam[0].replace('mirror_camMain', '_camMain'))
    cmds.parent(camgroup, rootSceneNode[0])