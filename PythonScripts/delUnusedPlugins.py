import maya.mel as mel
import maya.cmds as cmds
def delPlugs():
    old_pligins = cmds.unknownPlugin(query = True, list = True)
    if old_pligins is None:
        print(">>>>>>>>> No plugins <<<<<<<<<")
    else:
        for plugin in old_pligins:
            print(plugin)
            cmds.unknownPlugin(plugin, remove = True)