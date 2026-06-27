import maya.cmds as cmds
def create():
    locStr = cmds.ls('geo', 'basemesh')
    if locStr:
        cmds.confirmDialog(title='Warning', message="Loc structure already exist!", icon="information", button=['OK'])
    else:
        # Create an empty group node with the prop structure
        cmds.group( em=True, name='ground_n_walls' )
        cmds.group( em=True, name='set_dressing' )
        cmds.group( 'ground_n_walls', 'set_dressing', name = 'geo' )
        cmds.group( em=True, name='fx' )
        cmds.group( 'geo', 'fx', name = 'asset_loc' )
