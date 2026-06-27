import hou
nodeFile = hou.node("/obj/water_sim/whitewater_sim_flatten/render")
houdiniFile = "P:/TUTORIALES/The Gnomon Workshop - Large-Scale Water FX in Houdini/RD_SpaceShip_sim_FX_h20_v005.hip"
for n in range(1173,1400, 1):
    print("Openning scene")
    hou.hipFile.load(houdiniFile, ignore_load_warnings=False)
    print("Start caching", n)
    hou.RopNode(nodeFile).cook(frame_range=(n,n), verbose=True, output_progress=True)