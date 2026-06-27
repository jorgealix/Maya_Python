import maya.cmds as cmds
#Get camera shot clip atrributes
camSel = cmds.ls( sl=True )
#print camSel
if len(camSel) == 1:
    camSelShape = cmds.listRelatives(camSel)
    clp = cmds.listConnections( camSelShape, d=True )
    #Get attribs from clip
    getAst = cmds.getAttr(str(clp[0]) + '.startFrame')
    getAet = cmds.getAttr(str(clp[0]) + '.endFrame')
    #Set up the Maya GUI to compose the shot 
    cmds.playbackOptions( ast = getAst , aet = getAet, min = getAst , max = getAet )
    cmds.lookThru( 'perspView', camSelShape[0])
    cmds.currentTime(getAst)
else:
    print "Select only one camera"