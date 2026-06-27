import maya.cmds as cmds
import os
import json
import math

def get_udim_from_uv(u, v):
    return 1001 + int(u) + int(v) * 10


def get_used_udims(mesh):

    uvs = cmds.polyEditUV(f"{mesh}.map[*]", query=True)

    udims = set()

    for i in range(0, len(uvs), 2):
        u = uvs[i]
        v = uvs[i + 1]

        udim = get_udim_from_uv(u, v)
        udims.add(udim)

    return sorted(udims)


def get_connected_meshes(file_node):

    meshes = set()

    connections = cmds.listConnections(file_node, type="shadingEngine") or []

    for sg in connections:
        shapes = cmds.sets(sg, query=True) or []

        for shape in shapes:
            if cmds.nodeType(shape) == "mesh":
                meshes.add(shape)

    return list(meshes)


def resolve_udim_path(path, udim):
    return path.replace("<UDIM>", str(udim))


def check_udims():

    report = {}

    file_nodes = cmds.ls(type="file")

    for file_node in file_nodes:

        path = cmds.getAttr(file_node + ".fileTextureName")

        if not path:
            continue

        if "<UDIM>" not in path:
            continue

        meshes = get_connected_meshes(file_node)

        used_udims = set()

        for mesh in meshes:
            used_udims.update(get_used_udims(mesh))

        missing = []

        for udim in used_udims:
            tex_path = resolve_udim_path(path, udim)

            if not os.path.exists(tex_path):
                missing.append(udim)

        if missing:
            report[file_node] = {
                "texture": path,
                "missing_udims": sorted(missing),
                "used_udims": sorted(used_udims)
            }

    # guardar JSON
    scene_path = cmds.file(q=True, sn=True)
    root_dir = os.path.dirname(scene_path) if scene_path else os.getcwd()

    reports_dir = os.path.join(root_dir, "_tx_reports")
    os.makedirs(reports_dir, exist_ok=True)

    json_path = os.path.join(reports_dir, "missing_udims_from_scene.json")

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(report, f, indent=4)

    cmds.confirmDialog(
        title="UDIM Check",
        message=f"""
Nodos con problemas: {len(report)}

Reporte:
{json_path}
""",
        button=["OK"]
    )


check_udims()