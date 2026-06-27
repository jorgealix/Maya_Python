import maya.cmds as cmds

def cleanRigScene():
    global nam, lis, ntype, connections
    lis = cmds.ls()
    for i in lis:
        connections = cmds.listConnections(i)

        if connections is None:
            ntype = cmds.nodeType(i)

            if ntype in ["transform", "joint"]:
                print("Node "+ str(i) + " has a transform.")

            elif ntype in ["script",
                "objectSet",
                "groupId",
                "polyUnite",
                "shapeEditorManager",
                "nodeGraphEditorInfo",
                "gameFbxExporter",
                "poseInterpolatorManager"]:
                print("Node " + str(i)+ "  does not have a transform.")
                cmds.delete(i)
            else:
                print("Node "+ str(i) + " is OK!.")

    #nam = cmds.namespaceInfo(":", listOnlyNamespaces=True)
    # for a in nam:
    #     cmds.namespace(removeNamespace = a, deleteNamespaceContent = True)
    #     print("Namespace  "+ str(a) + " has been deleted.")
    # Set root namespace
    cmds.namespace(setNamespace=':')

    # Collect all namespaces except for the Maya built ins.
    all_namespaces = [x for x in cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True) if
                      x != "UI" and x != "shared"]

    if all_namespaces:
        # Sort by hierarchy, deepest first.
        all_namespaces.sort(key=len, reverse=True)
        for namespace in all_namespaces:
            # When a deep namespace is removed, it also removes the root.
            # So check here to see if these still exist.
            if cmds.namespace(exists=namespace) is True:
                cmds.namespace(removeNamespace=namespace, mergeNamespaceWithRoot=True)