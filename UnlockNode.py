###UNLOCK NODE
import maya.cmds as cmds
import os
import pymel.core as pm

# Look for unknown nodes
sel = cmds.ls( sl=True, sn=True )
for i in sel:
    cmds.lockNode(i, lock=False)
    cmds.delete(i)


lis = cmds.ls()
for i in lis:
    connections = cmds.listConnections(i)

    if connections is None:
        ntype = cmds.nodeType(i)
        # print(i,connections, ntype)
        if ntype in ["transform", "joint"]:
            print("Node " + str(i) + " has a transform.")

        elif ntype in ["script",
                       "objectSet",
                       "groupId",
                       "polyUnite",
                       "shapeEditorManager",
                       "nodeGraphEditorInfo",
                       "gameFbxExporter",
                       "poseInterpolatorManager"]:
            print("Node " + str(i) + "  does not have a transform.")
            cmds.delete(i)
        else:
            print("Node " + str(i) + " is OK!.")

# cmds.namespace(setNamespace=':')
# namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)

nam = cmds.namespaceInfo(":", listOnlyNamespaces=True)
for a in nam:
    print(a)
    cmds.namespace(removeNamespace=a, deleteNamespaceContent=True)