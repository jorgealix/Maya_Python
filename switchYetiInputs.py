import maya.cmds as cmds
import maya.mel as mel
global selected, ns, inputSel, nameref, nodename, mainFur, mainFeather

def adjustYeti():
    global configfurYeti, configfeatherYeti, melconfigfurYeti, melconfigfeatherYeti
    mel.eval ('global string $melConfigfurYeti = "";')
    mel.eval ('global string $melConfigfeatherYeti = "";')
    selected = cmds.ls( sl=True, sn=True )
    if (len(selected) > 0):
        ns = cmds.ls(selected[0], showNamespace=True)[0]
        if cmds.attributeQuery("CacheUsed", node=ns, exists=True):
            inputSel = cmds.getAttr(selected[0] + ".CacheUsed")
            print(ns, inputSel)
            # check if is in a reference
            print('check if is in a reference')
            if ":" in ns:
                nameref, nodename = ns.split(":")
                nameref =(nameref + ":")
                mainFur = (nameref + "mainFur_YETI")
                mainFeather = (nameref + "mainFeather_YETI")
                print("It is a reference",nameref, nodename, mainFur, mainFeather )
            else:
                nameref = ""
                nodename = selected[0]
                mainFur = "mainFur_YETI"
                mainFeather = "mainFeather_YETI"
                print("Is not a reference", nodename)
            # check cache type
            print('check cache type')
            if inputSel == 0:
                cmds.setAttr((nameref + "Cuerpo_assembly_geo.visibility"), 0)
                cmds.setAttr((nameref + "Cuerpo_thin_geo.visibility"), 1)
            elif inputSel == 1:
                cmds.setAttr((nameref + "Cuerpo_assembly_geo.visibility"), 1)
                cmds.setAttr((nameref + "Cuerpo_thin_geo.visibility"), 0)
            configfurYeti = ('pgYetiGraph -node "switch_fur" -param "inputselection" -setParamValueScalar ' + str(inputSel) + ' ' + mainFur + ';')
            configfeatherYeti = ('pgYetiGraph -node "switch_feather" -param "inputselection" -setParamValueScalar ' + str(inputSel) + ' ' + mainFeather + ';')
            print(configfurYeti)
            print(configfeatherYeti)
            mel.eval ('$melConfigfurYeti = python("configfurYeti");')
            mel.eval ('eval $melConfigfurYeti')
            mel.eval ('$melConfigfeatherYeti = python("configfeatherYeti");')
            mel.eval ('eval $melConfigfeatherYeti')
        else:
            print("Select the hair group node")
    else:
        print("Select at least the hair group node")
