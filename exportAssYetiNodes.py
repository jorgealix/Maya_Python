import maya.cmds as cmds

start = int(cmds.playbackOptions(q=True, min=True))
end   = int(cmds.playbackOptions(q=True, max=True))
cmds.select("main_groom", "undercut_groom", "eyebrows_groom")
for f in range(start, end + 1):
    cmds.currentTime(f, edit=True)

    ass_path = f"D:/Jorge_Medina/MayaTests/maxGroom/cacheAss/maxHair_isolated_cached.{f:04d}.ass"

    cmds.arnoldExportAss(
        f=ass_path,
        s=True,
        boundingBox=True,
        mask=8,
        lightLinks=0,
        shadowLinks=0,
        expandProcedurals=True,
        fullPath=True
    )
