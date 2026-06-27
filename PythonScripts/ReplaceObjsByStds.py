import maya.cmds as cmds
import random

def get_unique_name(base_name):
    if not cmds.objExists(base_name):
        return base_name
    i = 1
    while True:
        new_name = f"{base_name}{i}"
        if not cmds.objExists(new_name):
            return new_name
        i += 1

def get_bbox_size(obj):
    bbox = cmds.exactWorldBoundingBox(obj)
    size = [bbox[3] - bbox[0], bbox[4] - bbox[1], bbox[5] - bbox[2]]
    return size

def replace_with_aiStandIn_instances(standin_name):
    selected_objs = cmds.ls(selection=True, long=True)
    if not selected_objs:
        cmds.warning("No hay objetos seleccionados.")
        return
    if not cmds.objExists(standin_name):
        cmds.error(f"No se encontró el aiStandIn '{standin_name}' en la escena.")
        return

    standin_bbox_size = get_bbox_size(standin_name)
    if any(s == 0 for s in standin_bbox_size):
        cmds.warning(f"El bounding box del stand-in '{standin_name}' tiene dimensiones cero.")
        return

    base_name = standin_name + "_instance"
    instances = []

    for obj in selected_objs:
        pos = cmds.xform(obj, query=True, worldSpace=True, rp=True)
        orig_rot = cmds.xform(obj, query=True, worldSpace=True, rotation=True)

        # Añadir rotación aleatoria en Y (0 a 360 grados)
        random_y = random.uniform(0, 360)
        new_rot = [orig_rot[0], random_y, orig_rot[2]]

        obj_bbox_size = get_bbox_size(obj)
        scale_factors = [obj_bbox_size[i] / standin_bbox_size[i] if standin_bbox_size[i] != 0 else 1 for i in range(3)]

        parent = cmds.listRelatives(obj, parent=True, fullPath=True)

        instance = cmds.instance(standin_name)[0]
        unique_name = get_unique_name(base_name)
        instance = cmds.rename(instance, unique_name)

        shapes = cmds.listRelatives(instance, shapes=True, fullPath=False)
        if shapes:
            shape_name = f"{unique_name}Shape"
            cmds.rename(shapes[0], shape_name)

        cmds.xform(instance, worldSpace=True, translation=pos)
        cmds.xform(instance, worldSpace=True, rotation=new_rot)
        cmds.setAttr(f"{instance}.scaleX", scale_factors[0])
        cmds.setAttr(f"{instance}.scaleY", scale_factors[1])
        cmds.setAttr(f"{instance}.scaleZ", scale_factors[2])

        if parent:
            instance = cmds.parent(instance, parent[0])[0]

        # cmds.delete(obj)

        instances.append(instance)

    print(f"✅ Sustituidos {len(instances)} objetos por instancias de '{standin_name}' con rotación aleatoria en Y y nombres de shape correctos.")

# USO
replace_with_aiStandIn_instances("hierbas3_std")
