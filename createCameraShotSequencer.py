import maya.cmds as cmds

def create_shot_from_camera():
    sel = cmds.ls(selection=True)
    if not sel:
        cmds.error("Selecciona una cámara.")
    
    cam_transform = sel[0]

    # Obtener shape de cámara
    shapes = cmds.listRelatives(cam_transform, shapes=True, type="camera")
    if not shapes:
        cmds.error("El objeto seleccionado no es una cámara.")
    
    cam_shape = shapes[0]

    # Obtener curvas de animación conectadas
    anim_curves = cmds.listConnections(cam_transform, type="animCurve") or []
    anim_curves += cmds.listConnections(cam_shape, type="animCurve") or []

    if not anim_curves:
        cmds.error("La cámara no tiene animación.")

    # Calcular rango de animación real
    start_frames = []
    end_frames = []

    for curve in set(anim_curves):
        start = cmds.findKeyframe(curve, which="first")
        end = cmds.findKeyframe(curve, which="last")
        start_frames.append(start)
        end_frames.append(end)

    start_frame = min(start_frames)
    end_frame = max(end_frames)

    # Obtener nombre del shot desde el nombre de la cámara
    # sq0010_sh0500 -> sh0500
    shot_name = cam_transform.split("_")[-1]

    # Crear el shot en el Camera Sequencer
    shot = cmds.shot(
        shot_name,
        startTime=start_frame,
        endTime=end_frame,
        sequenceStartTime=start_frame,
        sequenceEndTime=end_frame,
        currentCamera=cam_shape
    )

    print("Shot creado:")
    print("Nombre:", shot_name)
    print("Frames:", start_frame, "-", end_frame)
    print("Cámara:", cam_transform)

# Ejecutar
create_shot_from_camera()