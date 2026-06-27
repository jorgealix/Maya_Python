import maya.cmds as cmds
import maya.mel as mel

global objects
objects = []
def exportToUE():
    ## Duplicate de asset estructure
    selected = cmds.ls(sl=True, long=True) or []
    if len(selected) == 0:
        # cmds.deleteUI("myWindow")
        cmds.error("No Asset selected")
        exit()
    for eachSel in selected:
        assetName = (eachSel.split("_"))
        assetName = (assetName[0].split("|"))[1]

        ## Still very crude. If anything else ends with capital SG in the scene this will mess things up.
        shaderGrps = cmds.ls("*SG")

        ## loop through the shader groups,
        ## select using hyperShade,
        ## assign the default lambert material,
        ## convert the selection to faces,
        ## reassign the material now to the faces hopefully creating a 'face set'
        clrSets = cmds.polyColorSet(query=True, allColorSets=True)
        if clrSets != 0:
            for set in clrSets:
                print(set)
                cmds.polyColorSet(delete=True, colorSet=set)
        for i in range(len(shaderGrps)):
            cmds.hyperShade(objects=shaderGrps[i])  # object selects objects from shadergroup or material
            objWithMaterial = cmds.ls(sl=True)  # store a list of the selected objects
            cmds.hyperShade(a="lambert1")  # assign lambert1 (a material that should always exist) to selection

            for object in objects:
                faces = cmds.polyListComponentConversion(tf=True)
                cmds.select(cl=True)  # clear selection
                for face in faces:  # loop through objects and add their faces to selection
                    cmds.select(face, add=1)
                cmds.hyperShade(a=shaderGrps[i])  # Assign the shader now to the selected faces
            cmds.sets(n=shaderGrps[i] + "_set")
        cmds.select(eachSel)
        ## cmds.polyUnite(ch=False, n=assetName)
        for i in range(len(shaderGrps)):
            cmds.select(shaderGrps[i] + "_set")
            # cmds.ls( selection=True )
            cmds.hyperShade(a=shaderGrps[i])
