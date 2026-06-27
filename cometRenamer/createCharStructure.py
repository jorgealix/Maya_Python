import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    #cmds.group( em=True, name='geo' )
    #cmds.group( em=True, name='blend_shapes' )
    cmds.group( em=True, name='rig' )
    cmds.group( em=True, name='cloth' )
    #cmds.group( em=True, name='hair' )
    cmds.group( em=True, name='fx' )
    cmds.group( 'rig','cloth','fx', name = 'char' )
