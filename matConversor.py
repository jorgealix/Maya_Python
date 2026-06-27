import maya.mel as mel
import maya.cmds as cmds
import re
# Create a dictioney with materials and shding groups
# usdos en la escena
def list_scene_materials():
    """
    list all materials used by geometry in the scene
    """
    scene_materials=[]
    all_sgs=cmds.ls(type='shadingEngine')
    dict_mat_sg = {}
    for sg in all_sgs:
        # if an sg has 'sets' members, it is used in the scene
        if cmds.sets(sg, q=True):
            materials = cmds.listConnections('{}.surfaceShader'.format(sg))
            additional_items = {sg:materials[0]}
            if materials:
                scene_materials.extend(materials)
                dict_mat_sg.update(additional_items)
                connected_nodes = cmds.listConnections(materials[0], source=True, destination=True)

        print(connected_nodes)
    return list(set(scene_materials))
list_scene_materials()