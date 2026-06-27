###BAKE EXPORT TO COMP

import maya.cmds as cmds
import os
selCam = cmds.ls( sl=True, sn=True )

if (len(selCam) == 1 and "Cam" in str(selCam)):
    ###Creacion de la nueva camara copiando los atributos de la de MatchMove
    selCamName = str(selCam[0])
    selCamShape = cmds.listRelatives(selCamName, shapes=True)
    targetCamName = selCamName + "_TO_COMP"
    cam = cmds.camera(n=targetCamName);
    cmds.copyAttr(selCamShape,cam[1],inConnections=True,values=True, oc=True, ksc=True);
    
    ####Parent Constraint antes de hacer un bake
    cmds.parentConstraint( selCam , cam[0], n="temporalConstraint");
    
    ####Bake de camara
    inframe = cmds.playbackOptions(query=True, ast=True);
    outframe = cmds.playbackOptions(query=True, aet=True);
    cmds.bakeResults(cam[0], t=(inframe,outframe));
    cmds.delete("temporalConstraint");


    ####Seleccion de locatorToComp e inicio del proceso de exportado
    cmds.select(cl=True)
    cmds.select(cam[0], add=True)
    cmds.select("locatorToComp", add=True)


    ###Obtencion de rutas y nombres
    filePathBase = cmds.file(q=True, sn=True)
    filePath = os.path.dirname(filePathBase)
    fileBase = os.path.basename(filePathBase)
    fileNameBase = os.path.splitext(fileBase)[0]
    fileName = str(cam[0])

    save_name = '"' + filePath + "/" + fileName + ".abc" + '"'
    root = " -root " + "locatorToComp " + "-root " + str(cam[0])


    ###Exportado
    command = "-frameRange " + str(int(inframe)) + " " + str(int(outframe)) + root + " -file " + str(save_name) 
    cmds.AbcExport ( j = command )
    print "Alembic exportado en " + save_name
    
    
else:
    if (len(selCam)>1):
        cmds.confirmDialog( title='Errorrrr', message='Selecciona SOLO UNA camara... ', button=['Si,segnor!'], defaultButton='Si,segnor!', cancelButton='Si,segnor!', dismissString='Si,segnor!' )
        print "Selecciona SOLO UNA camara... ";
    else:
        cmds.confirmDialog( title='Errorrrr', message='Selecciona una camara... ', button=['Si,segnor!'], defaultButton='Si,segnor!', cancelButton='Si,segnor!', dismissString='Si,segnor!' )
        print "Selecciona una camara... ";