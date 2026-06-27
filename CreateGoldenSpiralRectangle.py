import maya.cmds as cmds
phi = 1.7777
print(phi)
rect = cmds.polyPlane(w=phi, h=1, sx=1, sy=1, name="goldenRect")[0]
cmds.makeIdentity(rect, apply=True)
cmds.xform(rect, ws=True, t=[0, 0, 0])

import maya.cmds as cmds
import math

phi = 1.7777
b = math.log(phi) / (math.pi / 2)
a = 0.1  # escala inicial

num_points = 300
theta_max = 4 * math.pi  # 2 vueltas completas
points = []

for i in range(num_points):
    theta = i * (theta_max / num_points)
    r = a * math.exp(b * theta)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    points.append((x, y, 0))

cmds.curve(p=points, d=3, name="goldenSpiral")

bbox = cmds.exactWorldBoundingBox("goldenSpiral")
width = bbox[3] - bbox[0]
height = bbox[4] - bbox[1]
scale = 1.0 / max(width / phi, height / 1.0)
cmds.scale(scale, scale, scale, "goldenSpiral")
