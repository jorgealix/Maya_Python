import maya.cmds as cmds
import maya.mel
import sys
import os
def exportFat():
    list = cmds.listConnections('scene_CFX:Cuerpo_thin_geoShape')
    for l in list:
        if cmds.objectType(l) == 'AlembicNode':
            alembic_path = cmds.getAttr(str(l) + '.abc_File')
            path, filename = os.path.split(alembic_path)
            #path = path.replace('PUBLISH/GEO', 'STEPS')
            filename = filename.replace('scene', 'ZivaFatBody')
            alembic_start = int(cmds.getAttr(str(l) + '.startFrame'))
            alembic_end = int(cmds.getAttr(str(l) + '.endFrame'))
            root = "-root |scene_CFX:DINDIM|scene_CFX:blend_shapes|scene_CFX:fat_geo"
            save_name = path + "/" + filename
            command = ("-frameRange" + " " + str(alembic_start) + " " + str(alembic_end) + " " + "-uvWrite -worldSpace -eulerFilter -dataFormat ogawa " + str(root) + " -file " + str(save_name))
            cmds.AbcExport(j=command)
            print(save_name)