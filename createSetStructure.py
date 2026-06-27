import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    cmds.group( em=True, name='ground_walls_C_001_grp' )
    cmds.group( em=True, name='set_dressing_C_001_grp' )
    cmds.group( 'ground_walls_C_001_grp', 'set_dressing_C_001_grp', name = 'geo_C_001_grp' )
    cmds.group( em=True, name='fx_C_001_grp' )
    cmds.group( 'geo_C_001_grp', 'fx_C_001_grp', name = 'set_grp' )
