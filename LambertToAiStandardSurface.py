import maya.cmds as cmds


def convert_lambert_to_aiStandardSurface():
    lamberts = cmds.ls(type='lambert')

    for lambert in lamberts:
        if lambert == "lambert1":  # Saltar el lambert por defecto
            continue

        new_shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=lambert + "_ai")

        # Color
        color_conn = cmds.listConnections(lambert + '.color', plugs=True, source=True, destination=False)
        if color_conn:
            cmds.connectAttr(color_conn[0], new_shader + '.baseColor', force=True)
        else:
            color_val = cmds.getAttr(lambert + '.color')[0]
            cmds.setAttr(new_shader + '.baseColor', *color_val, type='double3')

        # Transparencia (invertida → aiStandardSurface.opacity)
        trans_conn = cmds.listConnections(lambert + '.transparency', plugs=True, source=True, destination=False)
        if trans_conn:
            # No se puede conectar directamente porque hay que invertirlo
            print(f"⚠️ {lambert} tiene transparencia conectada. Revísalo manualmente.")
        else:
            trans_val = cmds.getAttr(lambert + '.transparency')[0]
            opacity_val = [1 - t for t in trans_val]
            cmds.setAttr(new_shader + '.opacity', *opacity_val, type='double3')

        # Bump
        bump_conn = cmds.listConnections(lambert, type='bump2d')
        if bump_conn:
            for bump in bump_conn:
                bump_out = cmds.listConnections(bump + '.outNormal', plugs=True)
                if bump_out and lambert in bump_out[0]:
                    cmds.connectAttr(bump + '.outNormal', new_shader + '.normalCamera', force=True)

        # Reasignar shader a los objetos
        shading_groups = cmds.listConnections(lambert, type='shadingEngine')
        if shading_groups:
            for sg in shading_groups:
                cmds.connectAttr(new_shader + '.outColor', sg + '.surfaceShader', force=True)

        print(f"Convertido: {lambert} -> {new_shader}")


convert_lambert_to_aiStandardSurface()
