import maya.cmds as cmds

def asignar_lambert_individual():
    seleccion = cmds.ls(selection=True, long=False)

    if not seleccion:
        cmds.warning("No hay objetos seleccionados.")
        return

    for obj in seleccion:
        nombre_shader = f"M_{obj}"

        # Crear shader Lambert
        if cmds.objExists(nombre_shader):
            cmds.warning(f"El shader '{nombre_shader}' ya existe. Se omitirá este objeto.")
            continue

        shader = cmds.shadingNode('lambert', asShader=True, name=nombre_shader)

        # Crear shading group y conectar
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre_shader + "SG")
        cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader', force=True)

        # Asignar el shading group al objeto
        cmds.sets(obj, edit=True, forceElement=shading_group)

    print("¡Shaders asignados correctamente!")

# Ejecutar la función