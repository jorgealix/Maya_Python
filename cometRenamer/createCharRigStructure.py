import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    cmds.group( em=True, name='rig_grp' )
    cmds.group( em=True, name='cloth_grp' )
    cmds.group( em=True, name='fx_grp' )
    cmds.group( 'rig_grp','cloth_grp','fx_grp', name = 'char_grp' )
