from maya import cmds

class windowtest(object):
    
    def __init__(self):
        self.window = "Ello :3"
        self.title = "Ello :D"
        self.size = (400, 400)
        
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
            
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout(adjustableColumn = True)
        
        cmds.text("Hey, what sequence and shot do you have?")
        cmds.separator (height=20)
        self.sequenceNumber = cmds.intFieldGrp(label='Sequence Number: ')
        self.shotNumber = cmds.intFieldGrp(label='Shot Number: ')
        
        cmds.separator (height=20)
        self.setScene = cmds.button(label='Set Camera', command=self.cameraShortfilm)
        
        cmds.showWindow()
   
   
    def cameraShortfilm(self, *args):
        sequenceN = cmds.intFieldGrp(self.sequenceNumber, query=True, value=True)
        shotN = cmds.intFieldGrp(self.shotNumber, query=True, value=True)
               
        nomenclature = "sq" + "{:03d}".format(sequenceN[0]) + "_sh" + "{:03d}".format(shotN[0]) 
        nomenclature_control = str(nomenclature + "_ctr")
        
        if cmds.objExists(nomenclature) == False:
            new_camera = cmds.camera(n=nomenclature, dr=True, ovr=1.3)
            cmds.rename(new_camera[0], nomenclature)
            cmds.setAttr(str(nomenclature) + ".displayGateMaskOpacity", 1)
            cmds.setAttr(str(nomenclature) + ".displayGateMaskColor", 0, 0, 0)
        
            cmds.circle(name = nomenclature_control, r=1.5)
        
        
            cmds.parent(nomenclature, nomenclature_control)
            
        else:
            print("There is already a camera with this name on  the scene, dumbass")




my_window = windowtest()

