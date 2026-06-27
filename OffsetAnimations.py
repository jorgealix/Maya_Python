###OFFSET ANIMATIONS
import maya.cmds as cmds
result = cmds.promptDialog(
                title='Rename Object',
                message='Offset',
                button=['OK', 'Cancel'],
                style='float',
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')

if result == 'OK':
        value = cmds.promptDialog(query=True, text=True)
        print (value)
cmds.select(all=True)
cmds.keyframe(edit=True,relative=True,timeChange=value)
cmds.select(clear=True)