import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds
scene_path = "P:/PROYECTOS/DIN_DIM/VFX/DIM_B01/DIM_B01_128/DIM_B01_128_0230/STEPS/LAY/MAYA/scenes/DIM_B01_128_0230_LAY_scene_v009.ma"
cmds.file(new=True, force=True)
cmds.file(scene_path, i=True, force=True)
frame_rate = cmds.currentUnit(query=True, time=True)
start_frame = cmds.playbackOptions(query=True, minTime=True)
end_frame = cmds.playbackOptions(query=True, maxTime=True)

print("Frame Rate:", frame_rate)
print("Frame Range:", start_frame, "-", end_frame)
maya.standalone.uninitialize()