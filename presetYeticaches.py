import maya.cmds as cmds
import os
# Preset the Yeti node selected for exporting caches
# based on the shot settings
def presetYeti():
    global nodeName
    current_project_path = cmds.workspace(q=True, rd=True)
    normalized_path = os.path.normpath(current_project_path)
    path_components = normalized_path.split(os.sep)
    selection = cmds.ls(selection=True)
    for sel in selection:
        if ':' in sel:
            scene, nodeName = sel.split(':')
        else:
            nodeName = sel
        print(nodeName)
        cacheYetiFolder = (current_project_path + 'cache/yeti/')

        # Create Yeti folder if not exist
        if not os.path.exists(str(cacheYetiFolder)):
            # Create a new directory because it does not exist
            os.makedirs(str(cacheYetiFolder))

        filecacheYetiFolder = (cacheYetiFolder + str(path_components[6]) + '_' + nodeName + '.%04d.fur')
        startframe = cmds.playbackOptions(query=True, minTime=True)
        endframe = cmds.playbackOptions(query=True, maxTime=True)
        print("Current Project Path: ", current_project_path)
        print(filecacheYetiFolder)
        print(nodeName + 'Shape.' + 'cacheFileName')
        cmds.setAttr((sel + 'Shape.' + 'fileMode'), 0)
        cmds.setAttr((sel + 'Shape.' + 'cacheFileName'), filecacheYetiFolder.replace('/', '\\'), type="string")
        cmds.setAttr((sel + 'Shape.' + 'outputCacheFileName'), filecacheYetiFolder.replace('/', '\\'), type="string")
        cmds.setAttr((sel + 'Shape.' + 'outputCacheFrameRangeStart'), startframe)
        cmds.setAttr((sel + 'Shape.' + 'outputCacheFrameRangeEnd'), endframe)
        cmds.setAttr((sel + 'Shape.' + 'outputCacheNumberOfSamples'), 3)
        cmds.setAttr((sel + 'Shape.' + 'imageSearchPath'), "P:/PROYECTOS/DIN_DIM/VFX/ASSETS/Character/DIM_DindimCG/STEPS/GRM/MAYA/sourceimages/groom_MASK/", type="string")
        cmds.setAttr("defaultArnoldRenderOptions.autotx", 0)