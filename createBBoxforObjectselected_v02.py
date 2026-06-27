import maya.cmds as cmds
def createBBox():
    sel = cmds.ls(selection=True)
    if sel:
        bb = cmds.exactWorldBoundingBox(sel[0])
        # bb = [xmin, ymin, zmin, xmax, ymax, zmax]
        x = (bb[0] + bb[3]) / 2.0
        y = (bb[1] + bb[4]) / 2.0
        z = (bb[2] + bb[5]) / 2.0
        w = bb[3] - bb[0]
        h = bb[4] - bb[1]
        d = bb[5] - bb[2]
        bbox = cmds.polyCube(width=w, height=h, depth=d, name=sel[0] + "_BBOX")[0]
        cmds.move(x, y, z, bbox, absolute=True)
        print("Bounding box creado:", bbox)
    else:
        print("Selecciona un objeto primero.")