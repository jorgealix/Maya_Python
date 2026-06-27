import maya.cmds as cmds
def create():
    #Set Resolution render and fps
    cmds.setAttr("defaultResolution.width", 1920)
    cmds.setAttr("defaultResolution.height", 1080)

    #set the current options on load of maya (incase someone manually changed them it their settings)
    cmds.currentUnit( time='film' )
    cmds.grid(size=200, spacing=100, divisions=10)
    cmds.playbackOptions(min=0, max=500)
    cmds.currentTime(0)
    cmds.currentUnit( linear='cm' )

    #following commands will set the options in the userPrefs
    #setting the fps
    cmds.optionVar (sv=("workingUnitTime", "film"))
    cmds.optionVar (sv=("workingUnitTimeDefault", "film"))

    #setting the timeline durations and defaults
    cmds.optionVar (fv=("playbackMax",500))
    cmds.optionVar (fv=("playbackMaxDefault",500))
    cmds.optionVar (fv=("playbackMaxRange",500))
    cmds.optionVar (fv=("playbackMaxRangeDefault",500))
    cmds.optionVar (fv=("playbackMin",0))
    cmds.optionVar (fv=("playbackMinDefault",0))
    cmds.optionVar (fv=("playbackMinRange",0))
    cmds.optionVar (fv=("playbackMinRangeDefault",0))

    #setting the grid settings
    cmds.optionVar (fv=("gridDivisions",10))
    cmds.optionVar (fv=("gridSize",200))
    cmds.optionVar (fv=("gridSpacing",100))

    #setting the units
    cmds.optionVar (sv=("workingUnitLinear", "cm"))
    cmds.optionVar (sv=("workingUnitLinearDefault", "cm"))
    ###############################################################
    ###############################################################
    # Check if a scene node exist
    if cmds.objExists('scene_*'):
        cmds.select('scene_*')
        cmds.warning( 'A scene node exist in the scene')
    else:
        print "ok"
        # Introduce the number for sequence
        result = cmds.promptDialog(
            title='Sequence Number',
            message='Enter Sequence Number:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
        if result == 'OK':
            nSeq = cmds.promptDialog(query=True, text=True)
            if nSeq == '':
                 cmds.warning( 'Introduce a sequence number')
            else:
                digToAdd = 4 - len(nSeq)
                nSeq = str("0" * digToAdd) + str(nSeq)
                # create an empty group node with no children
                cmds.group( em=True, name='cam_grp' )
                cmds.group( em=True, name='set_grp' )
                cmds.group( em=True, name='chars grp' )
                cmds.group( em=True, name='abc_refs_grp' )
                cmds.group( em=True, name='props_grp' )
                cmds.group( em=True, name='crowds_grp' )
                cmds.group( em=True, name='lights_grp' )
                cmds.group( em=True, name='fx_grp' )
                cmds.group( 'cam_grp', 'set_grp', 'chars_grp', 'abc_refs_grp', 'props_grp','crowds_grp','lights_grp', 'fx_grp', name='scene_sq' + nSeq + '_grp')
