import maya.cmds as cmds

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
    size = [bbox[3] - bbox[0],  # X
            bbox[4] - bbox[1],  # Y
            bbox[5] - bbox[2]]  # Z
    return size

def replace_with_aiStandIn_instances(standin_name):
    selected_objs = cmds.ls(selection=True, long=True)

    if not selected_objs:
        cmds.warning("No hay objetos seleccionados.")
        return

    if not cmds.objExists(standin_name):
        cmds.error(f"No se encontró el aiStandIn '{standin_name}' en la escena.")
        return

    # Obtener tamaño del bounding box del stand-in original
    standin_bbox_size = get_bbox_size(standin_name)
    if any(s == 0 for s in standin_bbox_size):
        cmds.warning(f"El bounding box del stand-in '{standin_name}' tiene dimensiones cero.")
        return

    base_name = standin_name + "_instance"
    instances = []

    for obj in selected_objs:
        pos = cmds.xform(obj, query=True, worldSpace=True, rp=True)
        rot = cmds.xform(obj, query=True, worldSpace=True, rotation=True)

        # Bounding box del objeto original
        obj_bbox_size = get_bbox_size(obj)

        # Calcular factor de escala por eje
        scale_factors = [obj_bbox_size[i] / standin_bbox_size[i] if standin_bbox_size[i] != 0 else 1 for i in range(3)]

        # Obtener grupo padre
        parent = cmds.listRelatives(obj, parent=True, fullPath=True)

        # Crear instancia
        instance = cmds.instance(standin_name)[0]
        unique_name = get_unique_name(base_name)
        instance = cmds.rename(instance, unique_name)

        cmds.xform(instance, worldSpace=True, translation=pos)
        cmds.xform(instance, worldSpace=True, rotation=rot)
        cmds.setAttr(f"{instance}.scaleX", scale_factors[0])
        cmds.setAttr(f"{instance}.scaleY", scale_factors[1])
        cmds.setAttr(f"{instance}.scaleZ", scale_factors[2])

        if parent:
            instance = cmds.parent(instance, parent[0])[0]

        # cmds.delete(obj)

        instances.append(instance)

    print(f"✅ Sustituidos {len(instances)} objetos por instancias de '{standin_name}', con escala ajustada según bounding box.")

# USO:
replace_with_aiStandIn_instances("hierbas3_std")
