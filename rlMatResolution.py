import maya.cmds as cmds
import maya.mel as mel
import os

layer_name = "overrideRL"
model_group = "model_grp"
texturePath = r"P:\Jorge_Medina\LIBRERIA\mipmapResolutionChecker_dgruwier\dgruwier_mipmapResolutionChecker.tx"


def create_checker_material():
    """Crea un aiUtility con un aiImage conectado al color y devuelve (shader, shadingGroup)."""

    # Crear aiUtility
    shader = cmds.shadingNode("aiUtility", asShader=True, name="mipmapChecker_aiUtility")
    cmds.setAttr(shader + ".shadeMode", 2)  # modo flat (útil para checker debug)

    # Crear aiImage
    img = cmds.shadingNode("aiImage", asTexture=True, name="mipmapChecker_aiImage")
    cmds.setAttr(img + ".filename", texturePath, type="string")

    # Conectar aiImage → aiUtility.color
    cmds.connectAttr(img + ".outColor", shader + ".color", f=True)

    # Shading group
    sg = cmds.sets(renderable=True, noSurfaceShader=True,
                   empty=True, name=shader + "SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", f=True)

    print("Material creado correctamente:")
    print("  Shader:", shader)
    print("  ShadingGroup:", sg)
    print("  Textura cargada:", texturePath)

    return shader, sg

def create_render_layer_with_override(layer_name, model_group):
    """Crea un Render Setup layer y aplica Material Override al grupo indicado."""

    if not cmds.objExists(model_group):
        cmds.error("El nodo '{}' no existe en la escena.".format(model_group))

    # Crear material
    shader, shading_group = create_checker_material()

    print("\n--- Creando Render Setup ---\n")

    # INTENTAR API DE RENDER SETUP (2026)
    try:
        from maya.app.renderSetup.model import renderSetup
        
        # Obtener la instancia global del sistema de Render Setup
        rs = renderSetup.instance()

        # Crear un Render Layer nuevo
        layer = rs.createRenderLayer(layer_name)
        print(layer.name())
        # Layer
        layer = rs.getRenderLayer(layer_name)
        
        if not layer.name():
            layer = rs.createRenderLayer(layer_name)
            print("Render Setup layer creado:", layer_name)
        else:
            print("Render Setup layer ya existía:", layer_name)

        # Crear una collection dentro del layer
        collection_name = "modelGrp_Collection"
        #collection_name = rs.getCollection(collection_name)
        collection = layer.createCollection(collection_name)
        print("Collection creada:", collection_name)
        
        # Asignar el grupo model_grp a la collection ---
        selector = collection.getSelector()
        selector.setPattern("model_grp")   # nombre exacto del grupo
        
        print("Collection", collection_name, "ahora incluye:", selector.getPattern())


        # Material Override
        print("Creando Material Override…")
        import maya.app.renderSetup.model.override as override
        
        mat_override = collection.createMaterialOverride("_MaterialOverride")
        mat_override.setMaterial(shader)
        collection.addOverride(mat_override)

        print("✔ Material Override aplicado correctamente.")
        print("Shader usado:", shader)
        return

    except Exception as e:
        print("⚠ No se pudo usar Render Setup API. Error:")
        print(e)
        print("Usando fallback legacy render layer…")

    # ------------------- FALLBACK LEGACY -------------------
    # Si Render Setup falla (dependiendo del build), usamos render layer antiguo

    if not cmds.objExists(layer_name):
        cmds.createRenderLayer(name=layer_name, noRecurse=True)
        print("Legacy render layer creado:", layer_name)

    # Asignar shadingGroup directamente
    cmds.sets(model_group, e=True, forceElement=shading_group)

    print("✔ Material asignado en fallback (legacy render layer).")
    print("Proceso completado.")