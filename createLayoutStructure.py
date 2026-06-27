import maya.cmds as cmds
def createlayout():
    # Set Resolution render and fps
    #cmds.setAttr("defaultResolution.width", 1920)
    #cmds.setAttr("defaultResolution.height", 1080)

    # Set the current options on load of maya (in case someone manually changed them it their settings)
    #cmds.currentUnit( time='film' )
    cmds.grid(size=200, spacing=100, divisions=10)
    #cmds.playbackOptions(min=0, max=500)
    #cmds.currentTime(0)
    #cmds.currentUnit( linear='cm' )

    # Following commands will set the options in the userPrefs
    # setting the fps
    cmds.optionVar (sv=("workingUnitTime", "film"))
    cmds.optionVar (sv=("workingUnitTimeDefault", "film"))

    # Setting the timeline durations and defaults
    #cmds.optionVar (fv=("playbackMax",500))
    #cmds.optionVar (fv=("playbackMaxDefault",500))
    #cmds.optionVar (fv=("playbackMaxRange",500))
    #cmds.optionVar (fv=("playbackMaxRangeDefault",500))
    #cmds.optionVar (fv=("playbackMin",0))
    #cmds.optionVar (fv=("playbackMinDefault",0))
    #cmds.optionVar (fv=("playbackMinRange",0))
    #cmds.optionVar (fv=("playbackMinRangeDefault",0))

    # Setting the grid settings
    cmds.optionVar (fv=("gridDivisions",10))
    cmds.optionVar (fv=("gridSize",200))
    cmds.optionVar (fv=("gridSpacing",100))

    # Setting the units
    cmds.optionVar (sv=("workingUnitLinear", "cm"))
    cmds.optionVar (sv=("workingUnitLinearDefault", "cm"))
    ###############################################################
    ###############################################################
    # Check if a scene node exist
    if cmds.objExists('scene_*'):
        cmds.select('scene_*')
        cmds.warning('A scene node exist in the scene')
    else:
        print ("ok")
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
                cmds.group( em=True, name='cams_grp' )
                cmds.group( em=True, name='loc_grp' )
                cmds.group( em=True, name='chars_grp' )
                cmds.group( em=True, name='props_grp' )
                cmds.group( em=True, name='crowds_grp' )
                cmds.group( em=True, name='lgts_grp' )
                cmds.group( em=True, name='fx_grp' )
                #cmds.group( 'cams', 'sets', 'chars', 'props','crowds','lights', 'fx', name='sq' + nSeq)
                cmds.group('cams_grp', 'loc_grp', 'chars_grp', 'props_grp', 'crowds_grp', 'lgts_grp', 'fx_grp', name = str(nSeq))
    # Create attributes for control cameras
    # cmds.addAttr( 'cams', shortName='ao', longName='AnimaticOpacity', defaultValue=0.5, minValue=0.0, maxValue=1, keyable=True )
    # cmds.addAttr( 'cams', shortName='mo', longName='MaskOpacity', defaultValue=1.0, minValue=0.0, maxValue=1.0, keyable=True )
    # cmds.addAttr( 'cams', shortName='o', longName='Overscan', defaultValue=1.4, minValue=0.0, maxValue=5.0,keyable=True  )
    # cmds.addAttr( 'cams', shortName='as', longName='AnimaticScale', defaultValue=1.36, minValue=0.0, maxValue=5.0, keyable=True  )
    # cmds.addAttr( 'cams', shortName='mc', longName='MaskColor', defaultValue=0.0, minValue=0.0, maxValue=1.0, keyable=True  )
    # cmds.addAttr( 'cams', shortName='de', longName='Depth', defaultValue=0.2, minValue=0.0, maxValue=1.0, keyable=True  )