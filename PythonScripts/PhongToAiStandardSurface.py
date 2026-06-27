import maya.cmds as cmds


def convert_phong_to_aiStandardSurface():
    phong_shaders = cmds.ls(type='phong')

    for phong in phong_shaders:
        new_shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=phong + "_ai")

        # Conexión: Color difuso
        color_conn = cmds.listConnections(phong + '.color', plugs=True, source=True, destination=False)
        if color_conn:
            cmds.connectAttr(color_conn[0], new_shader + '.baseColor', force=True)
        else:
            color_val = cmds.getAttr(phong + '.color')[0]
            cmds.setAttr(new_shader + '.baseColor', *color_val, type='double3')

        # Conexión: Specular
        spec_conn = cmds.listConnections(phong + '.specularColor', plugs=True, source=True, destination=False)
        if spec_conn:
            cmds.connectAttr(spec_conn[0], new_shader + '.specularColor', force=True)
        else:
            spec_val = cmds.getAttr(phong + '.specularColor')[0]
            cmds.setAttr(new_shader + '.specularColor', *spec_val, type='double3')

        # Conexión: Bump
        bump_conn = cmds.listConnections(phong, type='bump2d')
        if bump_conn:
            for bump in bump_conn:
                bump_out = cmds.listConnections(bump + '.outNormal', plugs=True)
                if bump_out and phong in bump_out[0]:
                    cmds.connectAttr(bump + '.outNormal', new_shader + '.normalCamera', force=True)

        # Asignar nuevo shader a los objetos
        shading_groups = cmds.listConnections(phong, type='shadingEngine')
        if shading_groups:
            for sg in shading_groups:
                cmds.connectAttr(new_shader + '.outColor', sg + '.surfaceShader', force=True)

        print(f"Convertido: {phong} -> {new_shader}")


convert_phong_to_aiStandardSurface()
