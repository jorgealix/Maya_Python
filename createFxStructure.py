import maya.cmds as cmds
def create():
    fxStr = cmds.ls('fx')
    if fxStr:
        cmds.confirmDialog(title='Warning', message="FX structure already exist!", icon="information", button=['OK'])
    else:
        # Create an empty group node with the prop structure
        cmds.group(em=True, name='fx')
        cmds.group( em=True, name='geo', parent='fx' )
        cmds.group( em=True, name='particles', parent='fx'  )
        cmds.group( em=True, name='fields', parent='fx'  )
        cmds.group( em=True, name='volumes', parent='fx'  )
