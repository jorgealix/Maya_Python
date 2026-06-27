# List all attributes and values
import maya.cmds as cmds
sel = cmds.ls(selection = True)
print(sel[0])
attributes = cmds.listAttr(sel[0], write = True)
print(sel[0], attributes)
for attr in attributes:
    try:
        value = cmds.getAttr(sel[0] + '.' + attr)
        print(attr, '=', value)
    except:
        print(attr, 'has no values')