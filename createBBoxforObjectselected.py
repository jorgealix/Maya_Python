# Crea una geometría a modo de bounding box del objeto
import maya.cmds as cmds

def create_bbox_from_object(obj_name):
    # Get the bounding box of the object
    bbox = cmds.xform(obj_name, q=True, bb=True)

    # Extract the dimensions of the bounding box
    width = bbox[3] - bbox[0]
    height = bbox[4] - bbox[1]
    depth = bbox[5] - bbox[2]

    # Create a cube (bounding box) with the same dimensions
    bbox_cube = cmds.polyCube(width=width, height=height, depth=depth)[0]

    # Move the bbox_cube to the center of the original object
    cmds.xform(bbox_cube, translation=[(bbox[0] + bbox[3]) / 2, (bbox[1] + bbox[4]) / 2, (bbox[2] + bbox[5]) / 2])
    cmds.rename(bbox_cube, ("low_" + obj_name))
    return bbox_cube

# Example usage
selection_list = cmds.ls(selection=True)
for sel in selection_list:
    bbox_geometry = create_bbox_from_object(sel)