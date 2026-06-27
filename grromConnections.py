import maya.cmds as cmds
## Load for source groom and alembic anim files
groomFile = "W:/01_PRODUCTIONS/029_OGGLIES2/Assets/Character/max/groom/og2_character_max_groom.ma"
abcFile = "P:/Jorge_Medina/MayaTests/maxGroom/max_head_cycle.abc"
cmds.file(
    groomFile,
    i=True,
    ignoreVersion=True,
    mergeNamespacesOnClash=True,
    rpr=":",
    options="v=0;",
    pr=True,
    importFrameRate=True,
    importTimeRange="override")
cmds.AbcImport(
    abcFile,
    mode="import")

cmds.currentTime(1)
cmds.playbackOptions(min=1, max=41)   
## Hide hair objects 
cmds.setAttr("blendshapes_C_001_GRUP.visibility", 0)
cmds.setAttr("mainHairProxy_C_001_DMSH.visibility", 0)
cmds.setAttr("undercutHairProxy_C_001_DMSH.visibility", 0)
cmds.setAttr("head_C_001_DMSH.visibility", 0)
cmds.setAttr("eyebrowProxy_C_001_GRUP.visibility", 0)

# Set up deformers
cmds.blendShape(["body_C_001_DMSH", "bodyScalp_C_001_DMSH"], n="scalpTest_blend", before=0, origin="world", tc=0, w=[0,1])
pWrap = cmds.proximityWrap("curves_grp")
cmds.proximityWrap(pWrap, edit=True, addDrivers=["mainHairProxy_C_001_DMSH"])
cmds.setAttr("proximityWrap1.falloffRamp[1].falloffRamp_FloatValue", 1)
cmds.setAttr("proximityWrap1.drivers[0].driverWrapMode", 1)
cmds.setAttr("proximityWrap1.drivers[0].driverOverrideSmoothInfluences", 1)
cmds.setAttr("proximityWrap1.drivers[0].driverSmoothInfluences",3)

## set up for .grms and params adjust
cmds.setAttr(
    "main_groomShape.cacheFileName", 
    r"W:\01_PRODUCTIONS\029_OGGLIES2\Assets\Character\max\groom\v010\og2_character_max_groom_main_groomShape_v010.grm".replace("\\","/"),
    type="string")
cmds.setAttr("main_groomShape.fileMode", 1)
cmds.setAttr("main_groomShape.overrideCacheWithInputs", 1)
cmds.setAttr(
    "undercut_groomShape.cacheFileName", 
    r"W:\01_PRODUCTIONS\029_OGGLIES2\Assets\Character\max\groom\v010\og2_character_max_groom_undercut_groomShape_v010.grm".replace("\\","/"),
    type="string")
cmds.setAttr("undercut_groomShape.fileMode", 1)
cmds.setAttr("undercut_groomShape.overrideCacheWithInputs", 1)
cmds.setAttr(
    "eyebrows_groomShape.cacheFileName", 
    r"W:\01_PRODUCTIONS\029_OGGLIES2\Assets\Character\max\groom\v010\og2_character_max_groom_eyebrows_groomShape_v010.grm".replace("\\","/"),
    type="string")
cmds.setAttr("eyebrows_groomShape.fileMode", 1)
cmds.setAttr("eyebrows_groomShape.overrideCacheWithInputs", 1)

cmds.setAttr("main_groomShape.yetiVariableF_useGuides", 1)
cmds.setAttr("undercut_groomShape.yetiVariableF_useGuides", 1)

cmds.setAttr("main_groomShape.overrideCacheWithInputs", 1)
cmds.setAttr("undercut_groomShape.overrideCacheWithInputs", 1)
cmds.setAttr("eyebrows_groomShape.overrideCacheWithInputs", 1)



