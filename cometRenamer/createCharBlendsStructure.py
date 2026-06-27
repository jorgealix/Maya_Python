import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    cmds.group( em=True, name='blend_shapes_grp' )
