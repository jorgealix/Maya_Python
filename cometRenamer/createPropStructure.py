import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    cmds.group( em=True, name='geo_C_001_grp' )
    cmds.group( em=True, name='rig_C_001_grp' )
    cmds.group( em=True, name='fx_C_001_grp' )
    cmds.group( 'geo_C_001_grp', 'rig_C_001_grp', 'fx_C_001_grp', name = 'prop_grp' )
