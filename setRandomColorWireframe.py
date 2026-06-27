import maya.cmds as cmds
import random
pieceList = cmds.ls(selection = True)
for piece in pieceList:
    print(piece, random.randint(0, 16))
    cmds.setAttr((piece + "Shape.overrideEnabled"), 1)
    cmds.setAttr((piece + "Shape.overrideColor"), random.uniform(0, 31))