import maya.cmds as cmds
import maya.mel as mm
import os.path

def checkSettings(*args):
    global ipStatus, cam, cameras, UIwindow, mainLayout, renderResSelectMenu, width, heigth, tx, st, mb

    cameras = cmds.ls(type=('camera'), l=True)
    try:
        cmds.setAttr('defaultArnoldRenderOptions.autotx', False)
        cmds.setAttr('defaultArnoldRenderOptions.enable_swatch_render', False)
        cmds.renderThumbnailUpdate(False)
        cmds.setAttr('defaultArnoldRenderOptions.motion_blur_enable', True)
        cmds.setAttr('defaultArnoldDriver.halfPrecision', False)
        cmds.setAttr('defaultArnoldDriver.preserveLayerName', False)
        cmds.setAttr('defaultArnoldDriver.exrTiled', False)
        cmds.setAttr('defaultArnoldDriver.multipart', False)
        cmds.setAttr('defaultArnoldDriver.autocrop', False)
        cmds.setAttr('defaultArnoldDriver.append', False)
        cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
        cmds.setAttr('defaultArnoldRenderOptions.use_sample_clamp', True)
        cmds.setAttr('defaultArnoldRenderOptions.use_sample_clamp_AOVs', True)
        cmds.setAttr('defaultArnoldRenderOptions.AASampleClamp', 1.5)
        cmds.setAttr('defaultArnoldRenderOptions.indirectSampleClamp', 1.5)
    except:
        print("Some attributes are blocked and can not be set.")
    for cam in cameras:
        cmds.setAttr((cam + ".overscan"), 1)

def printNewMenuItem(item):
    global resX, resY, ipStatus
    if item == "Image Plane Resolution":
        if len(ipList) != 0:
            for ip in ipList:
                resX, resY = cmds.imagePlane(ip, q=True, imageSize = True )
                ipStatus = cmds.getAttr(ip + '.displayMode')
                if ipStatus > 0:
                    cmds.setAttr((ip + '.displayMode'), 2)
        print(item, resX, resY)
    if item == "Project Resolution":
        resX, resY = (4448, 1856)
        print(item, resX, resY)
    if item == "Custom Resolution":
        print(item, resX, resY)
    cmds.setAttr('defaultResolution.width', resX)
    cmds.setAttr('defaultResolution.height', resY)
    cmds.setAttr('defaultResolution.pixelAspect', 1.0)
def createUI():
    global mainLayout, renderResSelectMenu, ipList
    global ipStatus, resX, resY, cam, cameras, UIwindow, mainLayout, renderResSelectMenu, width, heigth, tx, st, mb

    st = cmds.playbackOptions(query=True, minTime=True)
    cmds.setAttr('defaultRenderGlobals.startFrame', st)
    et = cmds.playbackOptions(query=True, maxTime=True)
    cmds.setAttr('defaultRenderGlobals.endFrame', et)
    tx = cmds.getAttr('defaultArnoldRenderOptions.autotx')
    mb = cmds.getAttr('defaultArnoldRenderOptions.motion_blur_enable')
    ipList = cmds.ls(type='imagePlane')

    # check to see if window exists
    if cmds.window("UserInterface", exists=True):
        cmds.deleteUI("UserInterface")

    # create actual window
    UIwindow = cmds.window("UserInterface", title="Adjust camera resolution", w=250, h=150, mnb=False, mxb=False,
                           sizeable=False)

    mainLayout = cmds.columnLayout(w=250, h=150)
    cmds.optionMenu(w=250, label="Render Res Selection:", changeCommand = printNewMenuItem)
    cmds.menuItem(label="Image Plane Resolution")
    cmds.menuItem(label="Project Resolution")
    # cmds.menuItem(label="Custom Resolution")

    # cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 100)])
    # cmds.text(label='Width')
    # width = cmds.textField()
    # cmds.text(label='Heigth')
    # heigth = cmds.textField()
    # cmds.textField(width, edit=True, enterCommand=('cmds.setFocus(\"' + heigth + '\")'))
    # cmds.setParent('..')

    cmds.separator(visible=True)
    cmds.columnLayout(adjustableColumn=True, w=250, h=60)
    cmds.text(backgroundColor=[0, 1, 0], font='tinyBoldLabelFont', label=(
            'Frames range is ' + str(st) + '-' + str(et) + '\n' + ' AutoTX is ' + str(tx) + '\n' +
            ' Motion Blur ' + str(mb) + '\n' + 'ImagePlanes set to None '), width=250, height=50, enable=False,
              align='center')
    cmds.setParent('..')

    cmds.separator(visible=True)
    cmds.columnLayout(adjustableColumn=True, w=250, h=150)
    cmds.button(label="Apply", command=checkSettings)
    cmds.setParent('..')

    cmds.showWindow(UIwindow)  # shows window