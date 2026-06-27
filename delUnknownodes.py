import maya.cmds as cmds
unknownNodes = cmds.ls(type = 'unknown')
for node in unknownNodes:
    print 'deleting: ' + node
    cmds.lockNode(node, lock = False)
    cmds.delete(node)

###UNLOCK NODE
import maya.cmds as cmds
import os
import pymel.core as pm

# Look for unknown nodes
sel = cmds.ls( sl=True, sn=True )
for i in sel:
    if cmds.lockNode(i, query = True, lock=False):
        print("Deletting : " + str(i))
        cmds.lockNode(i, lock=False)
        cmds.delete(i)