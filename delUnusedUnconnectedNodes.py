import maya.cmds as cmds

def delete_unused_nodes():
    # Get all nodes in the scene
    all_nodes = cmds.ls()
    # List all nodes with no incoming or outgoing connections
    unused_nodes = [node for node in all_nodes if not (cmds.listConnections(node, source=False, destination=False) or [])]
    # Delete the unused nodes
    if unused_nodes:
        cmds.delete(unused_nodes)
        print(f"Deleted {len(unused_nodes)} unused nodes.")
    else:
        print("No unused nodes found.")