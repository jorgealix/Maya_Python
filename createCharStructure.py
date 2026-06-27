import maya.cmds as cmds
def create():
    # Create an empty group node with the prop structure
    charStr = cmds.ls('geo', 'basemesh')
    if charStr:
        cmds.confirmDialog(title='Warning', message="Char structure already exist!", icon="information", button=['OK'])
    else:
        cmds.group( em=True, name='basemesh' )
        cmds.group('basemesh', name='geo')
        cmds.group( em=True, name='blend_shapes' )
        cmds.group( em=True, name='rig' )

        cmds.group(em=True, name='cloth_colliders')


        cmds.group(em=True, name='hair_colliders')
        cmds.group(em=True, name='hair_curves')
        cmds.group(em=True, name='hair_groom')

        cmds.group( em=True, name='fx' )

        cmds.group('hair_colliders', 'hair_curves', 'hair_groom', name='hair')
        cmds.group('cloth_colliders', name='cloth')
        cmds.group('geo', ' blend_shapes','rig', 'cloth', 'hair', 'fx', name='asset_char')

