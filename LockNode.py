###LOCK NODE
import maya.cmds as cmds
import os
import pymel.core as pm

sel = cmds.ls( sl=True, sn=True )
for i in sel:
    
    pm.lockNode(i)