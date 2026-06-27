import mtoa.aovs as aovs
import maya.cmds as cmds
# Create AOVs for render and set then in the correct config
def setUpRenderAovs():
    cmds.setAttr('defaultArnoldDriver.exrTiled', 0)
    cmds.setAttr('defaultArnoldDriver.halfPrecision', 1)
    currentAOVs = cmds.ls(type='aiAOV')
    print('AOVs in the scene:', currentAOVs)
    # Layers elegidos para un render estandar
    dpsAOVsdict = {'N': ['vector', 'exr'],
                   'P': ['vector', 'exr'],
                   'Pref': ['rgb', 'exr'],
                   'RGBA': ['rgba', '<erx>'],
                   'Z': ['float', 'exr'],
                   'albedo': ['rgb', '<erx>'],
                   'coat': ['rgb', '<erx>'],
                   'denoise_albedo': ['rgb', '<erx>'],
                   'diffuse_direct': ['rgb', '<erx>'],
                   'diffuse_indirect': ['rgb', '<erx>'],
                   'emission': ['rgb', '<erx>'],
                   'sheen': ['rgb', '<erx>'],
                   'specular': ['rgb', '<erx>'],
                   'sss': ['rgb', '<erx>'],
                   'transmission': ['rgb', '<erx>'],
                   'crypto_asset': ['rgb', '<erx>'],
                   'crypto_material': ['rgb', '<erx>'],
                   'crypto_object': ['rgb', '<erx>'],
                   'motionvector': ['rgb', '<erx>']}
    # create a aiAOVDriver for exr 32 bit
    driver_node = cmds.shadingNode('aiAOVDriver', asUtility=True)
    cmds.setAttr(f"{driver_node}.aiTranslator", "exr", type="string")
    cmds.setAttr(f"{driver_node}.tiled", False)
    cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", True)
    cmds.setAttr("defaultArnoldRenderOptions.autotx", False)
    cmds.setAttr('defaultRenderGlobals.imageFilePrefix', "<Scene>/<RenderLayer>/<RenderPass>/<Scene>_<RenderLayer>_<RenderPass>", type = "string")
    # create the AOVs and override some connections
    for key, values in dpsAOVsdict.items():
        data, driver = values
        print("aiAOV_" + key)
        # Create AOVs if not exist and override some connections
        if ("aiAOV_" + key) not in currentAOVs:
            # print(f"{driver_node}.message, aiAOV_" + key + ".outputs[0].driver")
            aovs.AOVInterface().addAOV(key, data)
            if driver is "exr":
                cmds.connectAttr((driver_node + ".message"), ("aiAOV_" + key + ".outputs[0].driver"), force=True)
            if key is "RGBA":
                cmds.setAttr("aiAOV_RGBA.lightGroups", True)