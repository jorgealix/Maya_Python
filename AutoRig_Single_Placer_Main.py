import maya.cmds as cmds
def autoRigSimple():
    #Calculate volumes
    bBoxGrp = cmds.exactWorldBoundingBox('geo')
    bBoxPivot = cmds.objectCenter('geo', gl=True)
    rPlacer = abs(bBoxGrp[0]-bBoxGrp[3])/1.2
    rMain = abs(bBoxGrp[0]-bBoxGrp[3])/1.6
    #Create Nodes
    placerCrv = cmds.circle( n='Placer', ch=False, nr=(0, 1, 0), c = (bBoxPivot[0],0,bBoxPivot[2]), r=rPlacer,  )
    mainCrv = cmds.circle( n='Main', ch=False, nr=(0, 1, 0), c = bBoxPivot, r=rMain,  )
    dsysNode = cmds.group( em=True, n='Deformation_System' )
    root = cmds.joint( n='Root')
    cmds.setAttr(root + '.visibility', 0)
    cmds.setAttr(placerCrv[0] + '.overrideEnabled', 1)
    cmds.setAttr(placerCrv[0] + '.overrideColor', 17)
    cmds.setAttr(placerCrv[0] + '.sx', ch=False, k=False)
    cmds.setAttr(placerCrv[0] + '.sy', ch=False, k=False)
    cmds.setAttr(placerCrv[0] + '.sz', ch=False, k=False)
    cmds.setAttr(mainCrv[0] + '.overrideEnabled', 1)
    cmds.setAttr(mainCrv[0] + '.overrideColor', 18)
    cmds.parent(mainCrv,placerCrv)
    cmds.parent(dsysNode,mainCrv)
    #Check if node groups exists
    if cmds.objExists('rig'):
      cmds.parent(placerCrv,rigNode)
    else:
      rigNode = cmds.group( em=True, n='rig' )
      cmds.parent(placerCrv,'rig')
      
    if cmds.objExists('prop'):
      cmds.parent(rigNode,'prop')
    else:
      charNode = cmds.group( em=True, n='prop' )
      cmds.parent(rigNode,charNode)
      cmds.parent('geo',charNode)
    #Skining
    cmds.select('Root')  
    cmds.select( 'geo', hi=True, add=True )
    cmds.bindSkin(ta=True)