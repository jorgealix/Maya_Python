## Testear en una escean que de error

import maya.cmds as cmds
refs = cmds.ls(type="reference")
for r in refs:
    print(r)
    if cmds.referenceQuery( r,filename=True ) == '' or cmds.referenceQuery( r,filename=True ) == None:
        cmds.lockNode(r, lock=False)
        cmds.delete(r)