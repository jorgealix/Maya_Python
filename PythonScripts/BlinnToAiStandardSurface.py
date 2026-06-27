import maya.cmds as cmds


def convert_blinn_to_aiStandardSurface():
    blinns = cmds.ls(type='blinn')

    for blinn in blinns:
        new_shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=blinn + "_ai")

        # Conexión de color difuso
        color_conn = cmds.listConnections(blinn + '.color', plugs=True, source=True, destination=False)
        if color_conn:
            cmds.connectAttr(color_conn[0], new_shader + '.baseColor', force=True)
        else:
            color_val = cmds.getAttr(blinn + '.color')[0]
            cmds.setAttr(new_shader + '.baseColor', *color_val, type='double3')

        # Conexión de color especular
        spec_conn = cmds.listConnections(blinn + '.specularColor', plugs=True, source=True, destination=False)
        if spec_conn:
            cmds.connectAttr(spec_conn[0], new_shader + '.specularColor', force=True)
        else:
            spec_val = cmds.getAttr(blinn + '.specularColor')[0]
            cmds.setAttr(new_shader + '.specularColor', *spec_val, type='double3')

        # Roughness (aproximado desde eccentricity y specularRollOff)
        # NOTA: esto es un mapeo arbitrario, ya que no hay equivalencia exacta
        eccentricity = cmds.getAttr(blinn + '.eccentricity')
        rolloff = cmds.getAttr(blinn + '.specularRollOff')
        # Invertimos y escalamos para mapear a roughness
        roughness = 1.0 - (eccentricity * rolloff)
        cmds.setAttr(new_shader + '.specularRoughness', roughness)

        # Conexión de bump
        bump_conn = cmds.listConnections(blinn, type='bump2d')
        if bump_conn:
            for bump in bump_conn:
                bump_out = cmds.listConnections(bump + '.outNormal', plugs=True)
                if bump_out and blinn in bump_out[0]:
                    cmds.connectAttr(bump + '.outNormal', new_shader + '.normalCamera', force=True)

        # Transparencia (opcional, si quieres mapearla también)
        trans_conn = cmds.listConnections(blinn + '.transparency', plugs=True, source=True, destination=False)
        if trans_conn:
            print(f"⚠️ {blinn} tiene transparencia conectada. Revísala manualmente.")
        else:
            trans_val = cmds.getAttr(blinn + '.transparency')[0]
            opacity_val = [1 - t for t in trans_val]
            cmds.setAttr(new_shader + '.opacity', *opacity_val, type='double3')

        # Reasignar a shading group
        shading_groups = cmds.listConnections(blinn, type='shadingEngine')
        if shading_groups:
            for sg in shading_groups:
                cmds.connectAttr(new_shader + '.outColor', sg + '.surfaceShader', force=True)

        print(f"✅ Convertido: {blinn} → {new_shader}")


convert_blinn_to_aiStandardSurface()
