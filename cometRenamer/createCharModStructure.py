import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    cmds.group( em=True, name='geo_grp' )
    cmds.group( em=True, name='blend_shapes_grp' )
    cmds.group( em=True, name='hair_grp' )
    cmds.group( 'geo_grp','blend_shapes_grp','hair_grp', name = 'char_grp' )
