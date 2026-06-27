import os
import re
import maya.cmds as cmds
global nodeIP, nodeAbc, iPfileNmae, alembic_path, nodeAnim
# iPfileNmae = r'P:\PROYECTOS\DIN_DIM\VFX\DIM_B01\DIM_B01_074\DIM_B01_074_0010\PUBLISH\IMAGE_PLANE\PNG\IMP\NUKE_IPL_v002\DIM_B01_074_0010_IPL_v002.0981.png'.replace('\\','/')
def adjustToIp(*args):
    # Conform path and get patterns
    # Get IP  sequence file path
    nodeIP = cmds.ls(sl=True)
    iPfileNmae = cmds.getAttr(str(nodeIP[0]) + '.imageName')
    path, filename = os.path.split(iPfileNmae)
    filename_pattern = filename.split('.')
    K = '#'
    res = re.sub(r'\d', K, filename_pattern[1])
    filename_pattern = (filename_pattern[0],res,filename_pattern[2])
    filename_pattern = '.'.join(filename_pattern)
    newfolder_path = (path,filename_pattern)
    newfolder_path = '/'.join(newfolder_path)
    name_convention = r'^(\w+).(\d{4}).png$'
    pattern = re.compile(r'^(\w+).(\d{4}).png$')
    file_list = os.listdir(path)

    # Remove invalid files from the list of frames

    for f in file_list:
        if not re.match(name_convention, f):
            file_list.remove(f)

    # Adjust timeslider to length of IP

    first_file = file_list[0]
    last_file = file_list[-1]
    first_frame = int(re.search(r'^(\w+).(\d{4}).png$', first_file).group(2))
    last_frame = int(re.search(r'^(\w+).(\d{4}).png$', last_file).group(2))
    cmds.playbackOptions(minTime=first_frame, maxTime=last_frame, animationStartTime=first_frame, animationEndTime=last_frame)
    cmds.setAttr(defaultArnoldRenderOptions.autotx, 0)

def adjustToAbc(*args):
    nodeAbc = cmds.ls(sl=True)
    alembic_path = cmds.getAttr(str(nodeAbc[0]) + '.abc_File')
    alembic_start = int(cmds.getAttr(str(nodeAbc[0]) + '.startFrame'))
    alembic_end = int(cmds.getAttr(str(nodeAbc[0]) + '.endFrame'))
    cmds.playbackOptions(minTime=alembic_start, maxTime=alembic_end, animationStartTime=alembic_start, animationEndTime=alembic_end)
    cmds.setAttr(defaultArnoldRenderOptions.autotx, 0)

def adjustToAnimCrvs(*args):
    nodeAnim = cmds.ls(sl=True)
    # Buscar curvas de animación conectadas
    anim_curves = cmds.listConnections(nodeAnim, type="animCurve", source=True, destination=False) or []
    if not anim_curves:
        cmds.warning("El nodo no tiene curvas de animación.")
        return
    start_frames = []
    end_frames = []
    for curve in set(anim_curves):
        keys = cmds.keyframe(curve, query=True, timeChange=True)
        if keys:
            start_frames.append(min(keys))
            end_frames.append(max(keys))
    if not start_frames or not end_frames:
        cmds.warning("No se encontraron keyframes válidos.")
        return
    start = int(min(start_frames))
    end = int(max(end_frames))

    # Ajustar Time Slider
    cmds.playbackOptions(
        min=start,
        max=end,
        animationStartTime=start,
        animationEndTime=end
    )

    print("Time Slider ajustado de {} a {}".format(start, end))

def createUI():
    # Create the window
    window = cmds.window(title='TimeSlider Sincro', widthHeight=(350, 180))
    layoutSinc = cmds.columnLayout()
    button1 = cmds.button(label='Sincro with IP', width = 350, command = adjustToIp)
    cmds.separator(height=10)
    button2 = cmds.button(label='Sincro with Abc', width = 350, command = adjustToAbc)
    cmds.separator(height=10)
    button3 = cmds.button(label='Sincro with AnimCrvs', width = 350, command = adjustToAnimCrvs)
    cmds.separator(height=10)
    text1 = cmds.text(label=('Selecciona un nodo de Image Plane, Alembic u objeto animado' + '\n' + 'para sincronizar el Time Slider'), align='center', height = 50, width = 350)
    layoutWidth = cmds.layout(layoutSinc, query=True, width=True)
    fontSize = int(layoutWidth * 0.5)
    cmds.text(text1, edit=True, font='boldLabelFont', recomputeSize=True)
    cmds.showWindow(window)
