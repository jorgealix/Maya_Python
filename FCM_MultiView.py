import maya.cmds as cmds
import maya.mel as mel
import sys
import decimal
import os
import maya.OpenMaya as om
import maya.OpenMayaUI as omUI
import subprocess

#----------------------------
nameTool = 'FCM_MultiView'
version = 'v1.1'
#----------------------------
'''
Log:
v1.1:
    - now supports up axis Z
    - now when you change from the layouts Front/Back/Right 
    to the first 4th, it keeps the same camera position instead 
    of center the view based on the original selection.
    
'''
#==========#==========#==========#==========#==========#
#                   S E T T I N G S 
#==========#==========#==========#==========#==========#

# Show prompt windows settings:
skip_mesh_if_is_too_far_status = 1
Maya_2022_AO_ground_status = 1
# Sliders value 
Mesh_ScaleV_Default = 0.00032
CtrlShape_ScaleV_Default = 0.04
# height for MV in units
Height_Default = 200
# Sliders max value
meshScale_MaxValue = 0.00070
ctrlScale_MaxValue = 0.1
# AO ground
AO_ScaleV_Default = 15
# Max tolerance distance in X and Z for meshes 
# (this is to avoid include elements from visual pickers or BG)
treshold_far_away = 400
progress_bar_active = 1
# The way the non-skinned meshes are managed with the tool, Skin or constraint
driven_method = 'skin'
overscan = 0
# type of object that will include the filter_only_allowed_objs()
allowed_objs = ['mesh', 'nurbsSurface']
# Is used for put the cam really far from the center for present layouts 
far_away = -5000
#----------------------------
# Analize if Up axis is Y or Z
if cmds.upAxis( q=1, axis=1 ) == 'y':
    up_axis_setting = 0
if cmds.upAxis( q=1, axis=1 ) == 'z':    
    up_axis_setting = -90
#----------------------------
# Setting window
width_windows = 315
width_buttons_create = width_windows/1.4
width_buttons_delete = width_windows/6.5  
width_radio = 60
fontType = 'boldLabelFont'
#----------------------------
# links
linktree_link = 'https://linktr.ee/FranCerchiara'
documentation_link = 'https://docs.google.com/document/d/1MMmk7f7qpMbXWnTgwvf1KVuAhUijOzNesmE1HK3KE5c/edit?usp=sharing'
overview_video = 'https://youtu.be/cTehI13oiQs'

#==========#==========#==========#==========#==========#
#             D E C L A R I N G  N A M E S 
#==========#==========#==========#==========#==========#

#----------------------------
# Cam
camMV = 'Cam_MV_1'
cam_name_grp = 'Cam_MV_Group'
# master ctrl
master_ctrl_group = 'Master_Ctrl_Group'
ctrl_master = 'Ctrl_Master'
# group for groups
group_for_groups = 'MV_Group'
# Mesh
Mesh_Mv = '_Mesh_MV'
# Joints
joint_Mv = '_Jnt_MV'
joints_group_name = 'Joints_Group_Main'
joints_group_name_2 = 'Joints_Group_1'
# Groups
Mesh_Mv_Group = 'Meshes_MV_Group'
Ctrl_Mv_Group = 'Ctrl_MV_Group'
# Ctrls
Ctrl_Mv = 'Ctrl_MV'
Offset_Mv = 'Offset_MV'
Offset_2_Mv = 'Offset_2_MV'
# locators
All_Loc_World= 'All_Loc_World'
# Shelf
nameShelf = 'MV'
# Selection sets
Orig_Sel = 'Orig_Sel'
All_Ctrls = 'All_Ctrls'
All_Offset_Ctrls = 'All_Offset_Ctrls'
All_NurbsCircle = 'All_NurbsCircle'
All_Group_Ctrls = 'All_Group_Ctrls'
object_set = 'Object_set'
# BG and AO
BG_Color_name = 'BG_Color'
AO_Ground_name = 'AO_Ground_1'
Grp_AO_Ground_name = 'Grp_AO_Ground'
# saved_cam
saved_cam = 'Saved_cam'
#----------------------------
axis = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.translate', '.rotate', '.scale']
#----------------------------
# Types of driven
mesh_skin = 'Meshes_Skin'
mesh_others = 'Meshes_Others'
# all togheter
all_driven_meshes = [mesh_skin, mesh_others]
#----------------------------
# Auto adjust height
height_group = 'Auto_Adj_Height_Group'
#==========#==========#==========#==========#
#               M E S S A G E S 
#==========#==========#==========#==========#
SelEmpty = 'Please select at least one mesh'
noMeshes = 'No visible meshes in the scene'
BG_ColorCreated = 'BG Color created and only visible in MultiView Cam'
WIPMessage = "cmds.warning('WIP! Sorry')"
nameToolNoExists = nameTool + " system doesn't exists"
LayoutSaved = 'Layout saved'
all_vis_mesh_selectable = 'All visible meshes are now selectables'
Maya_2022_AO_ground_msg = 'AO Ground is not supported on Maya 2022 yet'
skip_meshes_msg = 'Some meshes are too far from the center of the world\nIf you want to include them, please select all the meshes manually'
dont_show_again_msg = "Ok, but don't show this again"
viewport_HD_msg = 'Turn on AA, AO and display texture'

#==========#==========#==========#==========#
#               A N N O T A T I O N S
#==========#==========#==========#==========#
create_MV_Ann = "Create MultiView system, if you don't have anything select it will automatically select all visible meshes"
breakField = '\nPRO TIP: Ctrl + Left/Right click on the numberal field will break the limit of the slider, same if you manually type a higher number'
update_MV_Ann = 'Rebuild the MultiView system but keeping your current layout, BG color and AO Ground'
while_anim_Ann = 'Layouts recommend for use while animating'
for_presenting_Ann = 'Layouts recommend for presenting'
save_to_shelf_Ann = 'Save all your current layout to shelf, even BG Color and AO Ground\nNo need to open the GUI to run the button created\n\nPRO TIP: If you double click the button that creates it will delete all the system'
BG_Color_Ann = 'Background color'
AO_Ground_Ann = 'Ambient Oclusion ground, to show the contacts with the ground'
AO_radio_Ann = 'Control the radio of the AO Ground' 
Mesh_Scale_Ann = 'Scale meshes independently from the ctrls' + breakField
Ctrl_Scale_Ann = 'Scale controls independently from the meshes' + breakField
Delete_Multiview_Ann = 'Delete everything related to ' + nameTool
#==========#==========#==========#==========#
#            F U N C T I O N S
#==========#==========#==========#==========#


def GUI():
    # if I want to keep working with all functions locally just keep this var empty
    if cmds.window (nameTool, exists=True):
        cmds.deleteUI (nameTool)        
    # Window template
    nameToolTitle = nameTool.replace("_", " ")
    window = cmds.window (nameTool, title=nameToolTitle+' '+version, s=True, menuBar=True)
    # Layout
    cmds.columnLayout( columnAttach=('both', 20), rowSpacing=5, columnWidth=width_windows, )
    # File
    cmds.menu( label='File')
    #cmds.menuItem( label='Save Layout to File', c=WIPMessage )
    cmds.menuItem( label='Save Layout to Shelf', c= imp_or_loc+'save_to_shelf()', ann=save_to_shelf_Ann)
    #cmds.menuItem( label='Load File', c=WIPMessage )
    cmds.menu( label='Bonus tools' )
    # turntable
    cmds.menuItem( subMenu=True, label='Turntable' )
    cmds.menuItem( label='Create', c=imp_or_loc+'create_turntable()' )
    cmds.menuItem( label='Delete', c=imp_or_loc+'delete_turntable()' )
    cmds.setParent( '..', menu=True )
    # viewport HD
    cmds.menuItem( l='Viewport HD', c=imp_or_loc+'viewport_HD()', ann=viewport_HD_msg)   
    # unlock all vis meshes
    #cmds.menuItem( l='select all visible meshes', c=imp_or_loc+'s()')   
    # unlock all vis meshes
    cmds.menuItem( l='Unlock all visible meshes', c=imp_or_loc+'unlock_all_vis_meshes()')   
    # Help
    cmds.menu( label='Help' )
    cmds.menuItem( l='Documentation', c="cmds.launch(web = '%s')" % (documentation_link) )
    cmds.menuItem( l='Overview video', c="cmds.launch(web = '%s')" % (overview_video) )
    cmds.menuItem( l='Contact', c=imp_or_loc+"contact_window()")

    if __name__ == '__main__':
        # DEV
        cmds.menu( label='DEV')
        # print object sel len
        cmds.menuItem( l='Print and select all visible meshes', c= 'select_all_vis_meshes_dev()')
        cmds.menuItem( l='Print objectSet lenght', c= "print ( len(cmds.ls(type='objectSet')) ) ")
        cmds.menuItem( l='Print type of node', c= "give_me_type_node()")
        cmds.menuItem( l='print distance X and Z', c= "print_distance_X_Z()")

    # Create Multiview
    cmds.separator(style='none') 
    cmds.rowLayout(nc=2)
    # Create MV
    cmds.button(l='Create MultiView',w=width_buttons_create, c= imp_or_loc+'create_4_MV()', ann=create_MV_Ann)
    cmds.button(l='Update', w= width_buttons_delete, c= imp_or_loc+ 'update_MV()', ann=update_MV_Ann)
    #width_buttons_delete
    cmds.setParent('..')
    #------------------------------
    # Layouts
    collection2 = cmds.radioCollection("Layout_Radio")
    #cmds.text(l='Multiview + Persp: ', font=fontType)    
    #
    cmds.gridLayout(nc=4, cellWidthHeight=(70, 23), ann = while_anim_Ann) 
    cmds.radioButton( 'layout1', label='Layout 1', onCommand= imp_or_loc+'change_layouts()') 
    cmds.radioButton( 'layout2', label='Layout 2', onCommand= imp_or_loc+'change_layouts()')
    cmds.radioButton( 'layout3', label='Layout 3', onCommand= imp_or_loc+'change_layouts()')
    cmds.radioButton( 'layout4', label='Layout 4', onCommand= imp_or_loc+'change_layouts()')
    cmds.setParent('..')
    #
    #cmds.text(l='Only Multiview: ', font=fontType)       
    cmds.rowColumnLayout(nc=4, ann = for_presenting_Ann)  
    cmds.text(l='Orthographic:   ', font=fontType)         
    cmds.radioButton( 'layout5', label='Front', w=width_radio, onCommand= imp_or_loc+'change_layouts()')
    cmds.radioButton( 'layout6', label='Back', w=width_radio, onCommand= imp_or_loc+'change_layouts()')
    cmds.radioButton( 'layout7', label='Right', w=width_radio, onCommand= imp_or_loc+'change_layouts()')
    cmds.setParent('..')
    #
    cmds.rowColumnLayout(nc=4, ann = for_presenting_Ann)  
    cmds.text(l='Perspective:      ', font=fontType)        
    cmds.radioButton( 'layout9', label='Front', w=width_radio,  onCommand= imp_or_loc+'change_layouts()')
    cmds.radioButton( 'layout10', label='Back', w=width_radio, onCommand= imp_or_loc+'change_layouts()')
    cmds.radioButton( 'layout11', label='Right', w=width_radio, onCommand= imp_or_loc+'change_layouts()')
    cmds.setParent('..')
    # Set layout 1 as default
    cmds.radioButton( 'layout1', e=1, sl=1)
    cmds.separator()
    #------------------------------
    # Ctrl Scale
    cmds.text(l='Mesh Scale', ann=Mesh_Scale_Ann)
    cmds.floatSliderGrp('Mesh_Scale', field=1, precision=5, ann=Mesh_Scale_Ann)
    pop_up_save_by_default()
    # Ctrl Shape Scale
    cmds.text(l='Ctrl Scale', ann=Ctrl_Scale_Ann)
    cmds.rowLayout(nc=2)
    pop_up_save_by_default()
    # Slider
    cmds.floatSliderGrp('Ctrl_Scale', field=1, w=210, precision=3, ann= Ctrl_Scale_Ann)
    # # # Checkbox vis Ctrl # # #
    # Checkbox visibility
    cmds.checkBox('visCtrls', label='Vis Ctrls', v=1,
    onc = imp_or_loc+'show_hide_ctrls(value = 1)', ofc= imp_or_loc+'show_hide_ctrls(value = 0)' )
    cmds.setParent('..')
    cmds.separator()
    # # # Create BG Color # # # 
    # Setting colors
    colors = [0.27, 0.7, 0.4], [0.27, 0.51, 0.7], [0.65, 0.45, 0.7]
    numb_colors = len(colors)
    cmds.rowLayout(nc= numb_colors )
    for item in colors:
        cmds.button(l='', w=width_windows/(numb_colors+0.45), bgc=[item[0], item[1], item[2]], c=  imp_or_loc + 'create_BG_color(BGcolor = %s)' % (item), ann=BG_Color_Ann )
    cmds.setParent('..')
    #---
    cmds.rowLayout(nc=2)
    cmds.button(l='Custom BG Color', w=width_buttons_create, c=imp_or_loc+'BG_color_choose_adv()', ann=BG_Color_Ann )
    cmds.button(l='Delete', w=width_buttons_delete, c=imp_or_loc+'delete_BG_color()')
    cmds.setParent('..')
    cmds.separator()
    # AO Ground # width_buttons_create=
    # Create
    cmds.rowLayout('AO_Create', nc=2, visible=1)
    cmds.button('createAO', l='Create AO Ground', w= width_buttons_create, c= imp_or_loc+'create_AO()', ann=AO_Ground_Ann)
    cmds.button('deleteAO', l='Delete', w=width_buttons_delete, c= imp_or_loc+'delete_AO()')            
    cmds.setParent('..')
    # Slider
    cmds.rowLayout('AO_Slider', nc=3, visible=1)
    pop_up_save_by_default()
    cmds.text(l='Radio')
    cmds.floatSliderGrp('AO_Groud_Slider', w= width_buttons_create/1.15, field=1, minValue=1, maxValue = AO_ScaleV_Default*2, ann=AO_radio_Ann,
    fieldMaxValue=100, fieldMinValue=0)
    cmds.button('deleteAO', l='Delete', w=width_buttons_delete, c= imp_or_loc+'delete_AO()')            
    cmds.setParent('..')
    #
    if cmds.objExists(AO_Ground_name):

        cmds.rowLayout('AO_Create', e=1, visible=0)
        cmds.rowLayout('AO_Slider', e=1, visible=1)
    else:
        cmds.rowLayout('AO_Create', e=1, visible=1)
        cmds.rowLayout('AO_Slider', e=1, visible=0)
    # Delete
    cmds.separator()
    cmds.button(l='Delete All MultiView', c= imp_or_loc+'delete_system()', ann=Delete_Multiview_Ann)
    cmds.separator(style='none')    
    # Show 
    cmds.showWindow( window )
    cmds.window( window, e=1, h=1, w=1 )
    # Connect sliders
    connect_sliders()
    #-----------------------------------------------------------
    # # # Check functions # # #
    # Check visibility state of Ctrls
    try:
        if cmds.objExists (nameTool):
            if cmds.getAttr(cmds.sets(All_Ctrls, q=1 )[0]+'.visibility'):
                cmds.checkBox('visCtrls', e=1, v=1)
            else:
                cmds.checkBox('visCtrls', e=1, v=0)
    except:
        pass
     #---------
    # check if 1.0 version exists on file
    if cmds.objExists(nameTool):
        if cmds.objExists(saved_cam) == 0:
            message = "You are using the version v1.1 but your file was made with the v1.0\nHopefully the rest of the updates won't force the user to recreate the MV"
            confirm = cmds.confirmDialog( title='Old version on file detected', message = message , 
            button= 'Create MultiView') 
            create_4_MV()
#-----------------------------------------------------------  
def create_MV():
    #
    number = '_1'
    was_cancelled = 0
    #--------------------------------------------
    # Check if selection is empty
    if cmds.ls(sl=True) == []:
        sel = select_all_vis_meshes()
        # skip object if the distance in X or Z is more than the threshold 
        sel = skip_mesh_if_is_too_far(s=sel)
    else:
        sel = cmds.ls(sl=True)
        sel = filter_only_allowed_objs(sel=sel)
    #--------------------------------------------
    # progress
    progress_start(title='Multi View progress', maxV=sel)
    #--------------------------------------------
    if sel:
        # # # Deal with every driven mesh diferently depending of the scenario # # #
        result = [] # this list is for later use to select all the meshMV togheter
        result_joints = []
        meshes_skin = []
        meshes_others = []
        result_joints_2 = []
        for item in sel:
            # CHECK SKIN
            try:
                checkSkin = (mel.eval('findRelatedSkinCluster '+item))
                if len( checkSkin ) > 1:
                    meshMV = cmds.duplicate (item, inputConnections=1, rc=1, n= item+Mesh_Mv) 
                    delete_objectSets(objsets=meshMV)
                    lock_unlock_all_attrs(i=meshMV[0], mode='unlock')
                    try:
                        cmds.connectAttr (item+".visibility", meshMV[0]+".visibility", f=1)
                    except:
                        pass
                    # add to list
                    result.append(meshMV[0])
                    meshes_skin.append(meshMV[0])
                    # update progress
                    progress_update(status_text= 'Duplicating %s' % (item) )
                    continue
            except:
                print_dev(msg='Error with %s driven mesh Skin' % (item))
            # CHECK OTHERS
            '''
            - Create a duplicate with input connection
            - Create a constraint with maintain offset off from orig mesh to joint
            - Now whatever the way that mesh is driven it covers the transform with the skin and also trhough nodes
            '''
            # duplicate with input connection
            meshMV = cmds.duplicate(item, inputConnections=1, rc=1, n=item+Mesh_Mv)
            delete_objectSets(objsets=meshMV)
            # if meshes has already locked attrs
            lock_unlock_all_attrs(i=meshMV[0], mode='unlock')
            break_connections(i=meshMV[0])
            try:
                cmds.connectAttr (item+".visibility", meshMV[0]+".visibility", f=1)
            except:
                pass
            # create joint with name as item
            cmds.select(cl=1)
            jnt = cmds.joint(n=item+joint_Mv, ch=0)
            # constraint parent and scale with mo 0
            cmds.parentConstraint(item, jnt, mo=0)
            cmds.scaleConstraint(item, jnt, mo=0)
            # skincluster method - (from joint to mesh mv)
            if driven_method == 'skin':
                try:
                    cmds.skinCluster( jnt, meshMV[0])
                except:
                    pass
            if driven_method == 'constraint':
                # Constriant method
                cmds.select(cl=1)
                jnt2 = cmds.joint(n=item+joint_Mv, ch=0)
                connect_attr(father=jnt, child=jnt2)
                cmds.parentConstraint(jnt2,meshMV[0], mo=0)
                cmds.scaleConstraint(jnt2, meshMV[0], mo=0)
                result_joints_2.append(jnt2)
            # to be able to group meshes in other folder and conpensate them in the same place
            lock_unlock_all_attrs(i=meshMV[0], mode='unlock')
            result.append(meshMV[0])
            meshes_others.append(meshMV[0])
            result_joints.append(jnt)
            # update progress
            progress_update(status_text= 'Duplicating %s' % (item) )
        #---------------------------------------------------------------------
        #print (was_cancelled )
        # lock all transfor of mv meshes 
        ### FIND HEIGHT AND ADJUST ###
        # create group with pivot on center of world
        groupMeshes = cmds.group(result, n=height_group)
        cmds.xform(groupMeshes, sp=(0,0,0), rp=(0,0,0))
        # get all vertex for each mesh
        result_vtx = []
        # progress
        #progress_start(title='Multi View progress', maxV=sel)
        for item in sel: 
            # progress
            #progress_update(status_text= 'Getting vertex %s' % (item) )
            try:
                nodeT = (cmds.nodeType(item))
                if nodeT:
                    if nodeT != 'objectSet':
                        # Get child from each group
                        child = cmds.listRelatives(item, allDescendents=1)
                        # Get vtxs
                        vertices = cmds.ls("{}.vtx[*]".format(child[0]), fl=True)
                        result_vtx.extend(vertices)
            except:
                print_dev(msg='Error with '+item+' getting vtxs')
        #---------------------------------------------------------------------
        # # #  Get Y position in WS # # #
        try:
            # progress
            progress_start(title='Multi View progress', maxV=result_vtx)
            height = []
            for vertex in result_vtx:
                #
                if cmds.upAxis( q=1, axis=1 ) == 'y':
                    axis = 1
                if cmds.upAxis( q=1, axis=1 ) == 'z':
                    axis = 2
                posVertex = cmds.xform(vertex, q=True, ws=True, t=True)[axis]
                height.append([posVertex])
                # progress update
                progress_update(status_text= 'Analizing vertexes %s' % (vertex) )
                if cmds.progressWindow( q=1, isCancelled=1 ):
                    was_cancelled = 1
                    break
            height.sort(); height = height[-1]
            # remove decimal
            height = round(height[0], 1)
            # Calculate diference (Using regla de 3 simple)
            value_scale = Height_Default/height 
            cmds.scale (value_scale, value_scale,value_scale, r=1 )
        except:
            print_dev(msg='Error with auto height')
        #---------------------------------------------------------------------
        # Create group for driven meshes
        if meshes_skin:
            cmds.group(meshes_skin, n = mesh_skin)
        if meshes_others:
            cmds.group(meshes_others, n = mesh_others)
        # joints group 2
        if driven_method == 'constraint':
            if result_joints_2:
                joints_group_2 = cmds.group(result_joints_2, n = joints_group_name_2)
                cmds.setAttr(joints_group_2+'.visibility', 0)
                cmds.parent(joints_group_2, groupMeshes, relative=1)
        # Create center of world for MV
        locWorld = cmds.spaceLocator()
        #-----------------------------
        cmds.setAttr(locWorld[0]+'.visibility',0)
        cmds.select(groupMeshes, locWorld[0])
        # group, ctrl and camera
        groupMeshMV = cmds.group(n= (Mesh_Mv_Group + number) )
        # create ctrl MV and rotate ctrl depending of up Axis
        ctrlMV = cmds.circle(n= (Ctrl_Mv + number), radius=30)
        if cmds.upAxis( q=1, axis=1 ) == 'y':
            cmds.setAttr (ctrlMV[1]+'.normalY', 200)
        if cmds.upAxis( q=1, axis=1 ) == 'z':
            cmds.setAttr (ctrlMV[1]+'.normalZ', 200)
        #
        ctrlMV_Offset = cmds.circle(nr=[0, 1, 0], n= (Offset_Mv + number), radius=30)
        cmds.parent(ctrlMV_Offset[0], ctrlMV[0])    
        ctrlMV_Offset_2 = cmds.circle(nr=[0, 1, 0], n= (Offset_2_Mv + number), radius=30)
        cmds.parent(ctrlMV_Offset_2[0], ctrlMV_Offset[0])    
        # group ctrl mv
        groupCtrlMV = cmds.group(ctrlMV, n= (Ctrl_Mv_Group + number) )
        cmds.setAttr(groupCtrlMV+'.translate', 0,0,0)
        cmds.setAttr(groupCtrlMV+'.rotate', 0,0,0)
        # Create Cam, but before: #
        camMV_local = cmds.camera(n= camMV[:-1])
        # Set camera attr
        cmds.setAttr (camMV_local[1] + ".focalLength", 500)
        #cmds.setAttr (camMV_local[1] + ".nearClipPlane", 1)
        cmds.setAttr (camMV_local[1] + ".farClipPlane", 9000000)        
        # Set overscan 
        if overscan == 1:
            cmds.setAttr ( camMV_local[1]+".displayResolution", 1)
            cmds.setAttr ( camMV_local[1]+".overscan", 1)
            cmds.setAttr ( camMV_local[1]+".displayGateMaskOpacity", 1)
            cmds.setAttr ( camMV_local[1]+".displayGateMaskColor", 0,0,0, type='float3' )
        cmds.setAttr ( camMV_local[1]+".filmFit", 3)
        # group for cam with pivot in center of world
        grpCam = cmds.group(camMV_local[0], n= cam_name_grp )
        cmds.xform(grpCam, sp=(0,0,0), rp=(0,0,0))
        # Create group for groups
        cmds.group( groupMeshMV ,  groupCtrlMV, n= (group_for_groups + number))
        # joints group
        joints_group = cmds.group(n=joints_group_name)
        cmds.setAttr(joints_group+'.visibility', 0)
        if result_joints:
            cmds.parent(result_joints, joints_group)
        # constraint parent and scale ctrl to group
        cmds.parentConstraint( (Ctrl_Mv + number), (Mesh_Mv_Group + number) , w=True, n='MV_ConstraintT')
        cmds.scaleConstraint( (Offset_2_Mv + number), (Mesh_Mv_Group + number) , w=True, n='MV_ConstraintS')
        # set Mesh_Mv_Group unselectable
        # Turn off vis for Offset
        cmds.setAttr ((Offset_Mv + number) + ".visibility", 0)
        scale_V = 1
        # Set Scale
        cmds.setAttr ((Offset_2_Mv + number) + ".scaleX", scale_V)
        cmds.setAttr ((Offset_2_Mv + number) + ".scaleY", scale_V)
        cmds.setAttr ((Offset_2_Mv + number) + ".scaleZ", scale_V)
        # Set rotation order to XYZ
        cmds.setAttr((Ctrl_Mv + number)+".rotateOrder", 0)
        #-------------------------------
        # Create Master Ctrl and group
        masterCtrlMV = cmds.circle(n=ctrl_master)
        groupCtrlMV_master = cmds.group(masterCtrlMV[0], n=master_ctrl_group)
        # scale
        cmds.setAttr (masterCtrlMV[1]+".radius", 0.030)
        # rotate
        cmds.setAttr (masterCtrlMV[1]+".normalY", 500)
        # change color
        cmds.setAttr (masterCtrlMV[0]+"Shape.overrideEnabled", 1)
        cmds.setAttr (masterCtrlMV[0]+"Shape.overrideColor", 22)
        # constraint
        cmds.parentConstraint (camMV, groupCtrlMV_master, mo=0)     
        # Constraint group ctrls to Ctrl master
        cmds.parentConstraint( masterCtrlMV, groupCtrlMV, mo=1)
        cmds.scaleConstraint( masterCtrlMV, groupCtrlMV, mo=1)
        #-------------------------------
        # create main group
        cmds.group(grpCam, group_for_groups+'*', joints_group, groupCtrlMV_master, n=nameTool)
        # create layer display and put main group
        cmds.createDisplayLayer (nameTool, name=nameTool+"_ly", number=1, nr=True)
        cmds.setAttr (nameTool+'_ly.color',18) 
        # Create sets for later use 
        put_in_set(setName = All_Ctrls, contentSet = (Ctrl_Mv + number) )
        put_in_set(setName = All_Offset_Ctrls, contentSet = ctrlMV_Offset )
        put_in_set(setName = All_NurbsCircle, contentSet = ctrlMV[1] )
        put_in_set(setName = All_Loc_World, contentSet = locWorld )
        put_in_set(setName = All_Group_Ctrls, contentSet = groupCtrlMV_master )
        put_in_set(setName = All_Group_Ctrls, contentSet = groupCtrlMV )
        put_in_set(setName = All_Ctrls, contentSet = masterCtrlMV[0] )
        put_in_set(setName = Orig_Sel, contentSet = sel )
        '''
        # Organize all driven meshes on groups
        for item in all_driven_meshes:
            grp_driven_meshes(result2 = result, driven_mesh = item, grp=[], name=item[:-10])
        '''
        # vis ctrls
        if cmds.checkBox('visCtrls', q=1, v=0):
            show_hide_ctrls(value = 1)
        else:
            show_hide_ctrls(value = 0)
        # lock attrs for orig sel
        meshes = meshes_skin + meshes_others
        
        for item in meshes:
            lock_unlock_all_attrs(i=item, mode='lock')
        
    #        
    progress_start(ends=1)
    # if progress bar was cancelled
    return was_cancelled 
#-----------------------------------------------------------
def connect_attr(father, child):
    try:
        cmds.connectAttr (father+".translate", child+".translate", f=1)
    except:
        pass
    try:
        cmds.connectAttr (father+".rotate", child+".rotate", f=1)
    except:
        pass
    try:
        cmds.connectAttr (father+".scale", child+".scale", f=1)
    except:
        pass
    try:
        cmds.connectAttr (father+".visibility", child+".visibility", f=1)
    except:
        pass
    '''
    individually
    for ax in axis:
        try:
            cmds.connectAttr (father+ax, child+ax, f=1)
        except:
            pass
    ''' 
#--------------------------------------------
'''
I am not using this one because is much more slower
'''
def connect_attr_ind(father, child):
    attrs = ['translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY','rotateZ',
            'scaleX','scaleY','scaleZ', 'visibility' ]
    for item in attrs:
        try:
            cmds.connectAttr (father+"."+item, child+"."+item, f=1)
            print (''),
        except:
            pass
#--------------------------------------------
def grp_driven_meshes(result2, driven_mesh, grp, name):
    '''
    This function is for organize all diferent types of driven mesh in groups
    '''
    for item in result2:
        # agroup driven meshes
        if driven_mesh[:-2] in item:
            grp.append(item)
    # create group if it has more than one item
    if len(grp) > 1:
        cmds.group(grp, n=name)
        cmds.select(cl=1)
#--------------------------------------------
def put_in_set(setName, contentSet):
    if cmds.objExists(setName):
        cmds.sets (contentSet, edit=True, forceElement=setName)
    else:
        cmds.sets( contentSet , n=setName)   
    # create master set and parent rest of sets 
    if cmds.objExists(nameTool+'_Set') == 0:
        cmds.sets( n=nameTool+'_Set', em=1)
    else:
        cmds.sets (setName, edit=True, forceElement=nameTool+'_Set')
#--------------------------------------------
def delete_system():
    # just in case
    cmds.progressWindow(endProgress=1)
    # remove posible meshes and joints outside the folder       
    meshes = cmds.ls('*'+Mesh_Mv+'*')
    joints = cmds.ls('*'+joint_Mv+'*')
    meshes_NS = cmds.ls('*:*'+Mesh_Mv+'*')
    meshes_NS_NS = cmds.ls('*:*:*'+Mesh_Mv+'*')
    joints_NS = cmds.ls('*:*'+joint_Mv+'*')
    shd = cmds.ls(BG_Color_name+'_Shading*')
    # Remove all this list
    removeThis = [nameTool+'_ly', shd, meshes, joints, meshes_NS, meshes_NS_NS, joints_NS, nameTool, camMV, nameTool+'_Set', All_Ctrls, All_NurbsCircle,
    All_Offset_Ctrls, Orig_Sel, nameTool+'_*', 'Group_Master_Ctrl']
    for item in removeThis:
        if item:
            try:
                cmds.delete(item)
            except:
                pass
    #----------------------------------
    delete_BG_color()
    delete_AO()
    #----------------------------------
    try:
        cmds.window (nameTool, e=1, h=2)
    except:
        pass
    #
    try:
        cmds.lookThru( 'persp' )
    except:
        pass
    # Print
    print (nameTool+' Deleted')
#--------------------------------------------
def change_layouts():
    if cmds.objExists(nameTool):
        #----------------
        # WHILE ANIM # 
        #----------------
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout1':
            save_cam_attrs()
            Layout_1()
            load_cam_attrs()
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout2':
            save_cam_attrs()
            Layout_2()
            load_cam_attrs()
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout3':
            save_cam_attrs()
            Layout_3()
            load_cam_attrs()
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout4':
            save_cam_attrs()
            Layout_4()
            load_cam_attrs()
        #----------------
        # PRESENT # 
        #----------------
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout5':
            save_cam_attrs()
            Layout_5()
            cmds.setAttr(saved_cam+".visibility", 0)
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout6':
            save_cam_attrs()
            Layout_6()
            cmds.setAttr(saved_cam+".visibility", 0)
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout7':
            save_cam_attrs()
            Layout_7()
            cmds.setAttr(saved_cam+".visibility", 0)
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout8':
            save_cam_attrs()
            Layout_8()
            cmds.setAttr(saved_cam+".visibility", 0)
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout9':
            save_cam_attrs()
            Layout_9()
            cmds.setAttr(saved_cam+".visibility", 0)
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout10':
            save_cam_attrs()
            Layout_10()
            cmds.setAttr(saved_cam+".visibility", 0)
        if cmds.radioCollection("Layout_Radio", q=True, select=True) == 'layout11':
            save_cam_attrs()
            Layout_11()
            cmds.setAttr(saved_cam+".visibility", 0)
        cmds.lookThru( camMV )
#--------------------------------------------
def create_4_MV():
    # curSel = cmds.ls(sl=1)
    # create progress window
    # save time
    start_0 = cmds.timerX()
    delete_system()
    was_cancelled = create_MV()
    if was_cancelled == 1:
        delete_system()
    else:
        # update progress
        if cmds.objExists(nameTool):
            # Duplicate with input connection and rename children
            numbers = '_2', '_3', '_4'
            # progress
            progress_start(title='Multi View progress', maxV=numbers)
            for number in numbers:
                # progress
                progress_update(status_text= 'Duplicating MV group')
                # dup special
                cmds.duplicate('MV_Group_1', ic=1, rc=1)
                # break connection and create constraints
                break_connections(i=Mesh_Mv_Group + number)
                cmds.parentConstraint('Offset_2_MV'+number, Mesh_Mv_Group + number )
                cmds.scaleConstraint('Offset_2_MV'+number, Mesh_Mv_Group + number )
            # saved cam
            tmp = cmds.group(empty=1, n=saved_cam)
            cmds.parent(tmp, nameTool)
            cmds.select(cl=1)
            # reorder groups outliner
            cmds.reorder (joints_group_name, b=1) 
            cmds.reorder (saved_cam, b=1) 
            cmds.reorder (master_ctrl_group, f=1)
             
            # final operations
            connect_sliders()
            change_layouts()
            set_settings_by_default()
            # center view
            cmds.viewFit(Orig_Sel, f= 0.5 )
            # print how much time the process has taken
            totalTime = cmds.timerX(startTime = start_0)
            totalTime = round(totalTime, 2)
            print ("Total time: ", totalTime),
            # end progress
            progress_start(ends=1)
        else:
            cmds.warning(SelEmpty)
    # back to sel
    #cmds.select(curSel)
#------------------------------------------------------------
def update_MV():
    if cmds.objExists(nameTool):
        # save current sel
        sel = cmds.ls(sl=1)
        #sel = filter_only_allowed_objs(sel=s)
        # Query current time and set it to 0
        #curTime = cmds.currentTime (q=1)
        #cmds.currentTime (0)
        # save most of attrs
        allArgs = save_attr()
        CtrlsMV_Trans = allArgs[0]
        CtrlsMV_Rot = allArgs[1]
        CtrlsMV_Scale = allArgs[2]
        cam_MV_Trans = allArgs[3]
        cam_MV_Rot = allArgs[4]
        lenseSetting = allArgs[5]
        nearClipSetting = allArgs[6]
        BGcolor= allArgs[7]
        savedAO_GroundInfo = allArgs[8]
        MeshScale = allArgs[9]
        CtrlScale = allArgs[10]
        turntable_check = allArgs[11]
        # # # #
        delete_system()
        if sel == []:
            sel = select_all_vis_meshes()
            sel = skip_mesh_if_is_too_far(s=sel)
            cmds.select(sel)
        # Turn on all references
        allReferences = cmds.ls(type='reference') 
        for item in allReferences:
            if item.endswith('RN'):
                try:
                    if cmds.referenceQuery(item, isLoaded=1) == 0:
                            cmds.file ( loadReference=item )
                except:
                    pass
        #
        create_4_MV()
        # Set BG color
        if len(BGcolor) > 0: 
            create_BG_color(BGcolor = BGcolor)
        # Set AO Ground
        if len(savedAO_GroundInfo) > 0:
            set_saved_AO(savedAO_GroundInfo[0])
        # go back to current time 
        #cmds.currentTime (curTime)
        # vis ctrls
        if cmds.checkBox('visCtrls', q=1, v=0):
            show_hide_ctrls(value = 1)
        else:
            show_hide_ctrls(value = 0)
        # set attrs
        set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale,
        cam_MV_Trans, cam_MV_Rot, lenseSetting, nearClipSetting, MeshScale, CtrlScale, turntable_check,
        BGcolor, savedAO_GroundInfo)
    else:
        cmds.warning(nameToolNoExists)
#--------------------------------------------
def connect_sliders():
    if cmds.objExists(nameTool):
        # Query sets
        allOffsetCtrls = cmds.sets(All_Offset_Ctrls, q=True)[:4]
        allNurbsCircle = cmds.sets(All_NurbsCircle, q=True)
        #----------------------------------
        # Disconnect ctrl scale
        for item in allNurbsCircle:
            conn = cmds.listConnections(item + '.radius' , source = 1 , p = 1)
            try:
                # sometimes there is more than 1 connection
                for itemconn in conn:
                    cmds.disconnectAttr(itemconn , item +'.radius' )
            except:
                pass
        #------------               
        # Disconnect mesh scale
        for item in allOffsetCtrls:
            conn = cmds.listConnections(item  , type='transform', source = 1 , p = 1)
            try:
                # sometimes there is more than 1 connection
                for itemconn in conn:
                    cmds.disconnectAttr(itemconn , item+itemconn[-7:] )
            except:
                pass
                #print_dev('failed connecting slider mesh with %s' % (item))
        #----------------------------------        
        # CTRL SCALE
        # center pivot of all offsets, you cannot do it after creating IDK why
        for item in allOffsetCtrls:
            cmds.select(item)
            cmds.CenterPivot()
        # Connect Offset_Ctrl to slider
        cmds.connectControl( "Mesh_Scale", (allOffsetCtrls[0]+'.scaleX'),
        (allOffsetCtrls[0]+'.scaleY'), (allOffsetCtrls[0]+'.scaleZ') )
        # Connect X, Y, Z local scale of all loc father and last loc to the first loc father
        try:
            for item in allOffsetCtrls:
                try:
                    cmds.connectAttr( (allOffsetCtrls[0]+'.scaleX'), (item +'.scaleX'), f=True)
                    cmds.connectAttr( (allOffsetCtrls[0]+'.scaleY'), (item +'.scaleY'), f=True)
                    cmds.connectAttr( (allOffsetCtrls[0]+'.scaleZ'), (item +'.scaleZ'), f=True)
                except:
                    # First time should  fail
                    pass
        except:
            pass
        #-----------------------------------------------------------
        # CTRL SHAPE SCALE
        # Connect NurbsCircle to slider
        cmds.connectControl( "Ctrl_Scale", (allNurbsCircle[0] + '.radius') )    
        # Connect X, Y, Z local scale of all loc father and last loc to the first loc father
        for item in allNurbsCircle:
            try:
                cmds.connectAttr( (allNurbsCircle[0]+'.radius'), (item +'.radius'), f=True)
            except:
                pass
        cmds.select(cl=True)
        # Connect scale X plane to slider
        if cmds.objExists(AO_Ground_name):
            planes = cmds.sets(AO_Ground_name[:-2], q=1)
            cmds.connectControl( 'AO_Groud_Slider', (planes[0]+'.scaleX'))
    # Set sliders to max value default setting
    cmds.floatSliderGrp('Mesh_Scale',e=1, maxValue=meshScale_MaxValue, fieldMaxValue=100)
    cmds.floatSliderGrp('Ctrl_Scale',e=1, maxValue=ctrlScale_MaxValue, fieldMaxValue=100)
    #
    print (''),
#-----------------------------------------------------------
def set_low_lense():
    cmds.setAttr (camMV[:-1]+"Shape*.focalLength", 40)
    cmds.setAttr (camMV[:-1]+"Shape*.nearClipPlane", 1)
#-----------------------------------------------------------
def set_high_lense():
    cmds.setAttr (camMV[:-1]+"Shape*.focalLength", 500)
    cmds.setAttr (camMV[:-1]+"Shape*.nearClipPlane", 30)
#-----------------------------------------------------------
def Layout_1():
    # Declaring Trans Rot Scale Ctrl MV
    CtrlsMV_Trans = [(-0.182, -0.205, -0.001), (-0.189, -0.382, 0.0), (0.193, -0.205, 0.0), (0.198, -0.382, -0.0), (0.005, 2.063, -39.816)]
    CtrlsMV_Rot = [(up_axis_setting+90, -0.0, 0.0), (up_axis_setting, 90.0, 0.0), (up_axis_setting, -0.0, 0.0), (up_axis_setting, -45.0, 0.0), (0.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.843, 0.843, 0.843), (0.843, 0.843, 0.843), (0.843, 0.843, 0.843), (0.843, 0.843, 0.843), (7.013, 7.013, 7.013)]
    # Declaring Cam position
    #cam_MV_Trans = (-6015.673, 2327.007, 8847.434)
    #cam_MV_Rot = (-11.738, -34.2, -0.0)
    # Set all attributes
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale)
    set_high_lense()
    #cmds.viewFit(Orig_Sel, f= 0.5 )
def Layout_2():
    # Declaring Trans Rot Scale Ctrl MV
    CtrlsMV_Trans = [(-0.182, -0.1819, 0.1039), (-0.189, -0.3347, 0.1932), (0.193, -0.1814, 0.1047), (0.198, -0.3347, 0.1932), (0.005, 2.0942, -39.816)]
    CtrlsMV_Rot = [(up_axis_setting, 45.0, 0.0), (up_axis_setting, 130.0, 0.0), (up_axis_setting, -45.0, 0.0), (up_axis_setting, -130.0, 0.0), (30.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.843, 0.843, 0.843), (0.843, 0.843, 0.843), (0.843, 0.843, 0.843), (0.843, 0.843, 0.843), (7.013, 7.013, 7.013)]
    # Declaring Cam position
    #cam_MV_Trans = (-6015.673, 2327.007, 8847.434)
    #cam_MV_Rot = (-11.738, -34.2, -0.0)
    # Set all attributes
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale )
    set_high_lense()
    #cmds.viewFit(Orig_Sel, f= 0.5 )
    
def Layout_3():
    # Declaring Trans Rot Scale Ctrl MV
    CtrlsMV_Trans = [(-0.26, 0.0, 0.0), (-0.106, 0.0, 0.0), (0.106, 0.0, 0.0), (0.26, 0.0, 0.0), (0.0, 0.677, -39.816)]
    CtrlsMV_Rot = [(up_axis_setting+90, -0.0, 0.0), (up_axis_setting, -0.0, 0.0), (up_axis_setting, 90.0, 0.0), (up_axis_setting, -45.0, 0.0), (0.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(1.923, 1.923, 1.923), (1.923, 1.923, 1.923), (1.923, 1.923, 1.923), (1.923, 1.923, 1.923), (3.648, 3.648, 3.648)]
    # Declaring Cam position
    #cam_MV_Trans = (-5830.499, 2310.544, 8600.299)
    #cam_MV_Rot = (-11.738, -34.2, -0.0)
    lenseSetting = 500.0
    # Set all attributes
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale)
    set_high_lense()
    #cmds.viewFit(Orig_Sel, f= 0.5 )

def Layout_4():
    CtrlsMV_Trans = [(0.017, 0.0, -0.0), (-0.0, 0.0, 0.017), (0.0, 0.0, -0.017), (-0.017, 0.0, 0.0), (-1.254, 0.674, -40.0)]
    CtrlsMV_Rot = [(up_axis_setting, 45.0, 0.0), (up_axis_setting, 0.0, 0.0), (up_axis_setting, 180.0, 0.0), (up_axis_setting, -45.0, 0.0), (30.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.364, 0.364, 0.364), (0.364, 0.364, 0.364), (0.364, 0.364, 0.364), (0.364, 0.364, 0.364), (10.377, 10.377, 10.377)]
    # Declaring Cam position
    #cam_MV_Trans = (-1988.647, 1461.545, 4467.467)
    #cam_MV_Rot = (-15.6, -24.0, 0.0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale)
    set_high_lense()
    #cmds.viewFit(Orig_Sel, f= 0.5 )

#---------------------------------------------------------
def Layout_5():
    CtrlsMV_Trans = [(0.017, 0.0, -0.0), (-0.0, 0.0, 0.017), (0.0, 0.0, -0.017), (-0.017, 0.0, 0.0), (0, 0, -40)]
    CtrlsMV_Rot = [(up_axis_setting, 45.0, 0.0), (up_axis_setting, 0.0, 0.0), (up_axis_setting, 180.0, 0.0), (up_axis_setting, -45.0, 0.0), (30, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (38, 38, 38)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_high_lense()
def Layout_6():
    CtrlsMV_Trans = [(0.017, 0.0, -0.0), (-0.0, 0.0, 0.017), (0.0, 0.0, -0.017), (-0.017, 0.0, 0.0), (0.0, 0.0, -40.0)]
    CtrlsMV_Rot = [(up_axis_setting, -130.0, 0.0), (up_axis_setting, -178.26, 0.0), (up_axis_setting, 0.0, 0.0), (up_axis_setting, 130.0, 0.0), (30.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (38.0, 38.0, 38.0)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_high_lense()
def Layout_7():
    CtrlsMV_Trans = [(0.0, 0.021, -0.003), (-0.019, -0.0, -0.0), (-0.0, -0.0, -0.0), (0.019, -0.0, 0.0), (0.0, -0.219, -40.0)]
    CtrlsMV_Rot = [(up_axis_setting, 90.0, -0.0), (up_axis_setting, -45.0, 0.0), (up_axis_setting, 0.0, -0.0), (up_axis_setting, 45.0, -0.0), (30.0, 0.0, -0.0)]
    CtrlsMV_Scale = [(0.229, 0.229, 0.229), (0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (38.0, 38.0, 38.0)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_high_lense()
def Layout_8():
    CtrlsMV_Trans = [(-0.267, 0.0, 0.0), (-0.098, 0.0, 0.0), (0.098, -0.0, -0.0), (0.263, -0.0, -0.0), (-0.052, -0.028, -40)]
    CtrlsMV_Rot = [(up_axis_setting, 0.0, 0.0), (up_axis_setting, 30.205, 0.0), (up_axis_setting, -23.436, 0.0), (up_axis_setting, -179.891, 0.0), (21.48, 0.0, 0.0)]
    CtrlsMV_Scale = [(1.923, 1.923, 1.923), (1.923, 1.923, 1.923), (1.923, 1.923, 1.923), (1.923, 1.923, 1.923), (4.725, 4.725, 4.725)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_high_lense()
#---------------------------------------------------------
def Layout_9():
    # Set variables
    CtrlsMV_Trans = [(0.019, 0, 0), (0, 0, 0.017), (0, 0.017, 0.025), (-0.019, 0, 0), (0,-2,-40) ]
    CtrlsMV_Rot = [(up_axis_setting, 34.0, 0), (up_axis_setting, 0, 0), (up_axis_setting-15, 180.0, 0), (up_axis_setting, -30.0, 0),  (10,0,0)]
    CtrlsMV_Scale = [(0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.175, 0.175, 0.175), (0.3, 0.3, 0.3), (515,515,515)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_low_lense()
def Layout_10():
    # Set pre saved rotation
    CtrlsMV_Trans = [(0.019, 0, 0), (0, 0, 0.017), (0, 0.017, 0.025), (-0.019, 0, 0), (0,-2,-40)]
    CtrlsMV_Rot = [(up_axis_setting, -140.0, 0.0), (up_axis_setting, -180.0, 0.0), (up_axis_setting+15, 0.0, 0.0), (up_axis_setting, 140.0, 0.0), (10.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.175, 0.175, 0.175), (0.3, 0.3, 0.3), (515,515,515)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_low_lense()
def Layout_11():
    # Declaring Trans Rot Scale Ctrl MV
    CtrlsMV_Trans = [(0.02, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.017, 0.003), (-0.02, 0.0, 0.0), (0.0, -2.0, -40.0)]
    CtrlsMV_Rot = [(up_axis_setting, 34.0, 0.0), (up_axis_setting, 0.0, 0.0), (up_axis_setting, 90.287, 0.0), (up_axis_setting, -30.0, 0.0), (10.0, 0.0, 0.0)]
    CtrlsMV_Scale = [(0.3, 0.3, 0.3), (0.3, 0.3, 0.3), (0.175, 0.175, 0.175), (0.3, 0.3, 0.3), (515.0, 515.0, 515.0)]
    # Declaring Cam position
    cam_MV_Trans = (far_away, far_away, far_away)
    cam_MV_Rot = (0, 0, 0)
    # Set attrs and lense
    set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot )
    set_low_lense()
#------------------------------------------------------------
def save_attr():
    if cmds.objExists(nameTool):
        allCtrlsMV = cmds.sets(All_Ctrls, q=1); allCtrlsMV = sorted(allCtrlsMV)
        # Save trans, rot and scale with loop
        CtrlsMV_Trans = []; CtrlsMV_Rot = []; CtrlsMV_Scale = []
        decNumber_set = 4
        for item in allCtrlsMV:
            # Trans
            temp = cmds.getAttr(item+'.translate')[0]
            temp2 = reduce_decimals(variable=temp, decNumber = decNumber_set)
            CtrlsMV_Trans.append(temp2)
            # Rot
            temp = cmds.getAttr(item+'.rotate')[0]
            temp2 = reduce_decimals(variable=temp, decNumber = decNumber_set)
            CtrlsMV_Rot.append(temp2)
            # Scale
            temp = cmds.getAttr(item+'.scale')[0]
            temp2 = reduce_decimals(variable=temp, decNumber = decNumber_set)
            CtrlsMV_Scale.append(temp2)
        # Save mesh scale (Taking just the first one of the set and just 1 axis is enough info)
        MeshScale = cmds.getAttr (cmds.sets(All_Offset_Ctrls, q=1)[0]+'.sx')
        MeshScale = round(MeshScale, 6)
        CtrlScale = cmds.getAttr (cmds.sets(All_NurbsCircle, q=1)[0]+'.r')
        CtrlScale = round(CtrlScale, 4)
        # Save Cam position
        # Trans
        cam_MV_Trans = cmds.getAttr(camMV+'.translate')[0]
        temp2 = reduce_decimals(variable=cam_MV_Trans, decNumber=3)
        cam_MV_Trans = temp2
        # Rot
        cam_MV_Rot = cmds.getAttr(camMV+'.rotate')[0]
        temp2 = reduce_decimals(variable=cam_MV_Rot, decNumber=3)
        cam_MV_Rot = temp2
        # Lense
        lenseSetting = cmds.getAttr(camMV+'.focalLength')
        # Camera clip
        nearClipSetting = cmds.getAttr(camMV+'.nearClipPlane')
        # save BG color
        if cmds.objExists(BG_Color_name):
            # save current BG color based on shading node
            ColorR = cmds.getAttr(BG_Color_name+'_Shading.colorR')
            ColorG = cmds.getAttr(BG_Color_name+'_Shading.colorG')
            ColorB = cmds.getAttr(BG_Color_name+'_Shading.colorB')
            BGcolor = ColorR, ColorG ,ColorB
            temp2 = reduce_decimals(variable=BGcolor, decNumber=3)
            BGcolor = temp2
        else:
            BGcolor = ''
        if cmds.objExists(AO_Ground_name):
            # Save info
            planesSet = cmds.sets(AO_Ground_name[:-2], q=1)
            savedAO_GroundInfo = cmds.getAttr(planesSet[0] + '.scale')[0]
            temp2 = reduce_decimals(variable=savedAO_GroundInfo, decNumber=3)
            savedAO_GroundInfo = temp2
        else:
            savedAO_GroundInfo = ''
        '''
        print (CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale,\
        cam_MV_Trans, cam_MV_Rot, lenseSetting, nearClipSetting,\
        BGcolor, savedAO_GroundInfo ),
        '''
        # Turntable 
        keys = cmds.keyframe( cam_name_grp, q=1)
        if keys:
            turntable_check = 'On'
        else:
            turntable_check = ''
        #
        return (CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale,\
        cam_MV_Trans, cam_MV_Rot, lenseSetting, nearClipSetting,\
        BGcolor, savedAO_GroundInfo, MeshScale, CtrlScale, turntable_check )
#------------------------------------------------------------
def set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale,
    cam_MV_Trans='', cam_MV_Rot='', lenseSetting='', nearClipSetting='', MeshScale='', CtrlScale='', turntable_check='',
    BGcolor='', savedAO_GroundInfo=''):
    #
    if cmds.objExists(nameTool):
        allCtrlsMV = cmds.sets(All_Ctrls, q=1)
        allCtrlsMV = sorted(allCtrlsMV)
        Value = 0
        for item in allCtrlsMV:
            # Set trans rot and scale 
            cmds.setAttr(item+'.translate', CtrlsMV_Trans[Value][0], CtrlsMV_Trans[Value][1], CtrlsMV_Trans[Value][2])
            cmds.setAttr(item+'.rotate', CtrlsMV_Rot[Value][0], CtrlsMV_Rot[Value][1], CtrlsMV_Rot[Value][2])
            cmds.setAttr(item+'.scale', CtrlsMV_Scale[Value][0], CtrlsMV_Scale[Value][1], CtrlsMV_Scale[Value][2])
            # Go to the next item list
            Value = Value + 1
            #print (item, Value)
        #
        if MeshScale:
            # Set scale for Meshes and Ctrls slider
            for item in cmds.sets(All_Offset_Ctrls, q=1):
                try:
                    cmds.setAttr(item+'.scale', MeshScale, MeshScale, MeshScale)
                except:
                    pass
        #
        if CtrlScale:
            for item in cmds.sets(All_NurbsCircle, q=1):
                try:
                    cmds.setAttr(item+'.r', CtrlScale)
                except:
                    pass
        # Set Camera trans, rot and lense
        try:
            if cam_MV_Trans == '':
                pass
            else:
                cmds.setAttr( camMV + ".translate", cam_MV_Trans[0], cam_MV_Trans[1], cam_MV_Trans[2])
                cmds.setAttr( camMV + ".rotate", cam_MV_Rot[0], cam_MV_Rot[1], cam_MV_Rot[2])
        except:
            pass
        try:
            cmds.setAttr( camMV + ".focalLength", lenseSetting )
        except:
            pass
        try:
            cmds.setAttr( camMV + ".nearClipPlane", nearClipSetting )
        except:
            pass
        # turntable
        if turntable_check == 'On':
            create_turntable()
#------------------------------------------------------------
def save_to_shelf():
    if cmds.objExists(nameTool):
        # save most of attrs
        allArgs = save_attr()
        CtrlsMV_Trans = allArgs[0]
        CtrlsMV_Rot = allArgs[1]
        CtrlsMV_Scale = allArgs[2]
        cam_MV_Trans = allArgs[3]
        cam_MV_Rot = allArgs[4]
        lenseSetting = allArgs[5]
        nearClipSetting = allArgs[6]
        BGcolor = allArgs[7]
        savedAO_GroundInfo = allArgs[8]
        MeshScale = allArgs[9]
        CtrlScale = allArgs[10]
        turntable_check = allArgs[11]
        sel = cmds.sets(Orig_Sel, q=1)
        # Check if BG Color exists
        if cmds.objExists(BG_Color_name):
            savedBG_Color = ('# Set BG Color\n' + imp_or_loc + 'create_BG_color ( BGcolor = '+str(BGcolor) +')\n' )
        else:
            savedBG_Color = ''
       # Check if AO Ground exists
        if cmds.objExists(AO_Ground_name):
            # Saving info to string
            savedAO_Ground = '# Set AO Ground\n' + imp_or_loc + 'set_saved_AO ( savedAO_GroundInfo = '+str(savedAO_GroundInfo[0])+' )\n'
        else:
            savedAO_Ground = ''
        # Turntable 
        if turntable_check == 'On':
            # Saving info to string
            savedTurntable = '# Set Turntable On\n' + imp_or_loc + 'create_turntable()\n\n'
        else:
            savedTurntable = '\n'
        # Code that goes inside the shelf
        shelfCodeString = (
        
        '# Import modules\n' +
        'import FCM_MultiView as MV\n\n' +

        '# Create MV\n' +
        imp_or_loc+'delete_system()\n'
        '# Original selection\n' +
        'sel = '+ str(sel) + '\n' +
        imp_or_loc+'clean_sel(sel); '+ imp_or_loc+'GUI(); '+imp_or_loc+'create_4_MV()\n\n' +
                
        '# Declaring Trans Rot Scale Ctrl MV\n' +
        'CtrlsMV_Trans = ' + str(CtrlsMV_Trans) + '\n' +
        'CtrlsMV_Rot = ' + str(CtrlsMV_Rot) + '\n' +
        'CtrlsMV_Scale = ' + str(CtrlsMV_Scale) + '\n' +
        '# Declaring Mesh and Ctrl scale sliders\n' +
        
        'MeshScale = ' + str(MeshScale) + '\n' +
        'CtrlScale = ' + str(CtrlScale) + '\n' +
        '# Declaring Cam position\n' +
        'cam_MV_Trans = ' + str(cam_MV_Trans) + '\n' + 
        'cam_MV_Rot = ' + str(cam_MV_Rot) + '\n' + 
        'lenseSetting = ' + str(lenseSetting) + '\n' + 
        'nearClipSetting = ' + str(nearClipSetting) + '\n\n' + 

        savedBG_Color +
        savedAO_Ground +
        savedTurntable +
        
        '# Set all attributes\n' +
        imp_or_loc+'set_attr(CtrlsMV_Trans, CtrlsMV_Rot, CtrlsMV_Scale, cam_MV_Trans, cam_MV_Rot, lenseSetting, nearClipSetting, MeshScale, CtrlScale )')
        # Doble click command
        dClickCmd = imp_or_loc+'delete_system()'
        
        # Create shelf button
        gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
        currentShelf = cmds.tabLayout(gShelfTopLevel, q=True, selectTab=True)
        cmds.setParent(currentShelf)
        cmds.shelfButton(ann='tes', imageOverlayLabel=nameShelf, image='pythonFamily.png', c=shelfCodeString, doubleClickCommand = dClickCmd, sourceType='python')
        # Print 
        print (LayoutSaved)
    else:
        cmds.warning(nameToolNoExists)
#------------------------------------------------------------
def clean_sel(sel):
    for item in sel:
        try:
            cmds.select(item, add=1)
        except:
            print_dev(msg='Error with clean sel')
 #------------------------------------------------------------
'''
def select_all_vis_meshes_based_on_viewport():
    # detect current  panel
    curPanel = cmds.getPanel (withFocus=1)
    # Get locs and nurbscurves
    nurbs_state = cmds.modelEditor( curPanel, q=1, nurbsCurves=1)
    locs_state = cmds.modelEditor( curPanel, q=1, locators=1)
    # Turn offf all objs
    cmds.modelEditor (curPanel, e=1, allObjects=0)
    # Turn on geo
    cmds.modelEditor (curPanel, e=1, polymeshes=1)
    # center view all
    #cmds.viewFit(f=0.5 )
    # select all visible objects in scene
    view = omUI.M3dView.active3dView()
    om.MGlobal.selectFromScreen( 0, 0, view.portWidth(), view.portHeight(),om.MGlobal.kReplaceList)
    # turn on nurbscurves and locators
    cmds.modelEditor (curPanel, e=1, nurbsCurves=nurbs_state)
    cmds.modelEditor (curPanel, e=1, locators=locs_state)
    meshes = cmds.ls(sl=1)
    cmds.select(d=1)
    return meshes
'''
#------------------------------------------------------------
def select_all_vis_meshes():
    shapes_and_shapesOrig = []
    # get all visible mesh shapes
    for obj in allowed_objs:
        temp = cmds.ls (v=1, type=obj, l=1)
        shapes_and_shapesOrig.extend(temp)
    if shapes_and_shapesOrig:
        # filter only polygon and nurbsurfaces
        shapes = cmds.filterExpand(shapes_and_shapesOrig, sm=[10, 12], fp=1 )
        # get transform from those
        tranform_meshes = cmds.listRelatives(shapes, p=1, f=1)
        # Remove dups
        tranform_meshes = list(dict.fromkeys(tranform_meshes))
        # save transform_meshes on result, but only works in this nasty way
        cmds.select(tranform_meshes)
        result = cmds.ls(sl=1, l=1)
        # remove items under some circunstances
        for mesh in tranform_meshes:
            # remove from the list if the mesh is hided trough layerDisplay
            if cmds.getAttr (mesh + '.overrideVisibility') == 0:
                result.remove(mesh)
            # remove from the list if the mesh is hided trough losVisibility
            if cmds.getAttr (mesh + '.lodVisibility') == 0:
                result.remove(mesh)
            # if isnot a transform remove it from list
            if cmds.objectType (mesh) != 'transform':
                result.remove(mesh)
        # order list
        result.sort()
        # remove long
        cmds.select(result)
        result = cmds.ls(sl=1)
        # clear sel
        cmds.select(cl=1)
        # return
        return result
    else:
        result = []
        return result
#-------------------------------------------- 
def filter_only_allowed_objs(sel):
    ''' Test
    s= cmds.ls(sl=1)
    sel = filter_only_allowed_objs(sel=s)
    cmds.select(sel)
    ''' 
    result = []
    #sel = cmds.ls(sl=1)
    for item in sel:
        # if item is already a mesh shape
        if cmds.objectType(item) == 'mesh':
            # get transform and put on list
            i2 = cmds.listRelatives(item, p=1, f=1)
            if i2:
                result.extend(i2)
        # 
        else:
            if cmds.objectType(item) == 'transform':
                # get shape
                i1 = cmds.listRelatives(item, s=1, f=1)
                if i1:
                    for obj in allowed_objs:
                        if cmds.objectType(i1[0]) == obj:
                            # get transform from shape
                            i2 = cmds.listRelatives(i1, p=1)
                            result.append(item)
    return result

#--------------------------------------------
def create_BG_color(BGcolor):
    if cmds.objExists(nameTool):
        if cmds.objExists(BG_Color_name):
            # Change color #
            cmds.setAttr( (cmds.ls(BG_Color_name+'_Shading')[0] + ".color"), BGcolor[0], BGcolor[1], BGcolor[2], type='double3')
        else:
            # Create BG #
            # Create sphere and reverse normal
            BG = cmds.polySphere(r=200000, n=BG_Color_name)
            cmds.setAttr(BG_Color_name+'.overrideEnabled', 1) 
            cmds.setAttr(BG_Color_name+'.overrideDisplayType', 2)
            cmds.setAttr ("BG_ColorShape.displaySmoothMesh", 2)
            cmds.ReversePolygonNormals()
            cmds.parent(BG, nameTool)
            # Make it unselectable
            # Create shader and apply it
            BGShader = cmds.shadingNode('lambert', asShader=True, n= BG_Color_name+'_Shading')
            cmds.select(BG)
            cmds.hyperShade( assign = BGShader )
            # Set color
            cmds.setAttr ( (BGShader + ".color"), BGcolor[0], BGcolor[1], BGcolor[2], type='double3')
            # constraint cam to BG
            cmds.parentConstraint(camMV, BG[0], mo=0)
            cmds.select(cl=True)
            # Print
            print (BG_ColorCreated),
    else:
        cmds.warning(nameToolNoExists)
#--------------------------------------------
def BG_color_choose_adv():
    if cmds.objExists(nameTool):
        result = cmds.colorEditor()
        buffer = result.split()
        try:
            if '1' == buffer[3]:
                values = cmds.colorEditor(query=True, rgb=True)
                BG_Color = values
            create_BG_color(BGcolor = BG_Color)
        except:
            pass
    else:
        cmds.warning(nameToolNoExists)
#--------------------------------------------
def delete_BG_color():
    if cmds.objExists(BG_Color_name):
        cmds.delete(BG_Color_name, BG_Color_name+'_Shading')
#--------------------------------------------
def create_AO():
    if cmds.objExists(nameTool):
        # ----------------------------------
        delete_AO()
        # Turn on AO Viewport 2.0
        try:
            cmds.setAttr ("hardwareRenderingGlobals.ssaoEnable", 1)
        except:
            print_dev(msg='Error with turning on AO')
        # Create Poly plane
        AOGround = cmds.polyPlane(w=20, h=20, sy=2, sx=2, n=AO_Ground_name)
        # up axis    
        if cmds.upAxis( q=1, axis=1 ) == 'z':
            cmds.setAttr(AOGround[0]+'.rotateX', 90)
        # create group
        grp = cmds.group(AOGround, n=Grp_AO_Ground_name)
        # put in set
        put_in_set(setName = AO_Ground_name[:-2], contentSet = AOGround[0] )
        # set scale by default
        cmds.setAttr(AOGround[0]+'.scale', AO_ScaleV_Default, AO_ScaleV_Default, AO_ScaleV_Default)
        cmds.parent(grp, nameTool)
        # Create shader and apply it
        AOGroundShader = cmds.shadingNode('lambert', asShader=True, n= AO_Ground_name+'Shading')
        cmds.select(AOGround)
        cmds.hyperShade(AOGround[0], assign = AOGroundShader )
        cmds.select(cl=True)
        # Set transparent
        cmds.setAttr ( (AOGroundShader + ".transparency"), 1, 1, 1, type='double3')
        # For now I'll do the create AO MV as default
        
        fathers = Mesh_Mv_Group+'_1', Mesh_Mv_Group+'_2', Mesh_Mv_Group+'_3', Mesh_Mv_Group+'_4'
        fathers = sorted(fathers)
        for item in fathers:
            temp = cmds.duplicate(AOGround[0], instanceLeaf=1)[0]
            # parent to Ctrl MV
            cmds.parent(temp, item, relative=True)
            put_in_set(setName = AO_Ground_name[:-2], contentSet = temp )
        #
        connect_AO()
        #--------------------
        # I am not good at maths so... Let's Maya make math for me
        # create empty group
        grp = cmds.group(empty=1)
        cmds.parent(grp, 'Meshes_MV_Group_1')
        # freeze
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        # now parent to height group
        cmds.parent(grp, height_group)
        # get fucking number
        scale_value = cmds.getAttr(grp+'.scaleX')
        cmds.delete(grp)
        cmds.setAttr(Grp_AO_Ground_name + '.scale', scale_value, scale_value, scale_value)
        #--------------------
        # For GUI
        cmds.rowLayout('AO_Create', e=1, visible=0)
        cmds.rowLayout('AO_Slider', e=1, visible=1)
    else:
        cmds.warning(nameToolNoExists)
    # check maya version
    if cmds.about(version=1) == '2022':
        # confirm dialog
        if Maya_2022_AO_ground_status == 1:
            confirm = confirm_dialog(message = Maya_2022_AO_ground_msg)
            if confirm == dont_show_again_msg:
                write_on_file(replace_this = 'Maya_2022_AO_gr'+'ound_status = 1',
                for_this='Maya_2022_AO_ground_status = 0')
#--------------------------------------------
def connect_AO():
    if cmds.objExists(AO_Ground_name):
        # Free mode
        # It will connect all AO planes for each MV
        planes = cmds.sets(AO_Ground_name[:-2], q=1)
        # Connect AO Ground
        for item in planes:
            try:
                cmds.connectAttr( (planes[0]+'.scaleX'), (item +'.scaleX'), f=True)
                cmds.connectAttr( (planes[0]+'.scaleY'), (item +'.scaleY'), f=True)
                cmds.connectAttr( (planes[0]+'.scaleZ'), (item +'.scaleZ'), f=True)
            except:
                pass
        cmds.connectAttr( (planes[0]+'.scaleX'), (planes[0] +'.scaleY'), f=True)
        cmds.connectAttr( (planes[0]+'.scaleX'), (planes[0] +'.scaleZ'), f=True)
        
        # Connect scale X plane to slider
        cmds.connectControl( 'AO_Groud_Slider', (planes[0]+'.scaleX'))
        cmds.select(cl=True)
        # Print empty line just to avoid confusing warning output information
        print (''),
#--------------------------------------------   
def set_saved_AO(savedAO_GroundInfo):
    create_AO()
    planes = cmds.sets(AO_Ground_name[:-2], q=1)
    for item in planes:
        try:
            cmds.setAttr(item + '.scaleX', savedAO_GroundInfo)
        except:
            print_dev(msg='Error with '+item+' setting saved AO\n')
#--------------------------------------------
def delete_AO():
    deleteThis = [cmds.ls(AO_Ground_name[:-1]+'*'), Grp_AO_Ground_name, AO_Ground_name, AO_Ground_name+'Shading']
    for item in deleteThis: 
        try:
            if item:
                cmds.delete(item)
        except:
            pass
    # For GUI
    cmds.rowLayout('AO_Create', e=1, visible=1)
    cmds.rowLayout('AO_Slider', e=1, visible=0)
    cmds.window( nameTool, e=1, h=1, w=1 )
#--------------------------------------------
def set_settings_by_default():
    # Scale mesh value by default
    allOffsetCtrls = cmds.sets(All_Offset_Ctrls, q=1)
    for item in allOffsetCtrls:
        try:
            cmds.setAttr(item+'.scale', Mesh_ScaleV_Default, Mesh_ScaleV_Default, Mesh_ScaleV_Default )
        except:
            pass
            #print ('Error with '+item+' setting mesh scale by default\n')
    if cmds.objExists(nameTool):
        try:
            for item in cmds.sets(All_NurbsCircle, q=1):
                cmds.setAttr (item+".radius", CtrlShape_ScaleV_Default) 
        except:
            pass
#-----------------------------------------------------------
def show_hide_ctrls(value):
    if cmds.objExists(nameTool):
        for item in cmds.sets(All_Ctrls, q=1 ):
            cmds.setAttr(item+'.visibility', value)
    else:
        cmds.warning(nameToolNoExists)
#-----------------------------------------------------------
def unlock_all_vis_meshes():
    # Query 
    shapesAndShapesOrig = cmds.ls (v=True, type='mesh')
    groups = cmds.ls(type='transform')
    groupsAndMeshes = groups + shapesAndShapesOrig
    displayLayers = cmds.ls(type='displayLayer', l=True)
    # For meshes
    #amount = len(groupsAndMeshes)
    #amount2 = len(displayLayers)
    #prg_win = cmds.progressWindow( title='Progress Bar', max=amount ) 
    for item in groupsAndMeshes:
        try:
            #cmds.progressWindow(e=1, step=1, st='Make selectable %s' )
            if cmds.getAttr (item + '.overrideDisplayType') == 2:
                cmds.setAttr (item + '.overrideDisplayType', 0)
        except:
            pass
    # For displayLayers
    displayLayers = cmds.ls(type='displayLayer', l=True) 
    for ld in displayLayers:
        try:
            cmds.setAttr(ld + '.displayType', 0)     
        except:
            pass
    #cmds.progressWindow('desg', endProgress=1)
    print (all_vis_mesh_selectable),
#-----------------------------------------------------------
def create_turntable():
    if cmds.objExists(nameTool):
        # save sel
        sel = cmds.ls(sl=1)
        # query time range
        startTime = cmds.playbackOptions (q=1, min=1)
        endTime = cmds.playbackOptions (q=1, max=1) + 1
        cmds.currentTime (startTime)
        # remove all keys
        cmds.cutKey(cam_name_grp, cl=1)
        # up axis
        if cmds.upAxis( q=1, axis=1 ) == 'y':
            axis = 'ry'
        if cmds.upAxis( q=1, axis=1 ) == 'z':
            axis = 'rz'
        # set keys
        cmds.setKeyframe(cam_name_grp, v=0, at= axis, ott= 'linear', itt= 'linear', time=startTime )
        cmds.setKeyframe(cam_name_grp, v=360, at= axis,  ott= 'linear', itt= 'linear', time=endTime)
        # back to sel
        cmds.select(sel)
def delete_turntable():
    cmds.cutKey(cam_name_grp, cl=1)
    cmds.setAttr(cam_name_grp+'.ry', 0)
#-----------------------------------------------------------
def pop_up_save_by_default():
    cmds.popupMenu()
    cmds.menuItem(l='Save by default', c=WIPMessage)
#-----------------------------------------------------------
def pop_up_BG_color():
    cmds.popupMenu("PopUp_BG_Color")
    cmds.menuItem(l="Delete BG Color", c= imp_or_loc+"delete_BG_color()")
#-----------------------------------------------------------
def confirm_dialog(message):
    confirm = cmds.confirmDialog( title='Confirm', message = message , 
    button= ['Ok', dont_show_again_msg]) 
    return confirm
#-----------------------------------------------------------
def write_on_file(replace_this, for_this):
    # Get script Folder
    usd = cmds.internalVar(usd=True)
    mayascripts = '%s/%s' % (usd.rsplit('/', 3)[0], 'scripts')
    nameTool_py = '/FCM_MultiView.py'
    # Read in the file
    with open(mayascripts + nameTool_py, 'r') as file :
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(replace_this, for_this)
    # Write the file out again
    with open(mayascripts + nameTool_py, 'w') as file:
      file.write(filedata)
    # reload tool
    import FCM_MultiView as MV; import imp
    imp.reload(MV)
#-----------------------------------------------------------
def reduce_decimals(variable, decNumber):
    temp0 = round(variable[0], decNumber)
    temp1 = round(variable[1], decNumber)
    temp2 = round(variable[2], decNumber)
    variable = (temp0, temp1, temp2)
    return variable
#-----------------------------------------------------------
def lock_unlock_all_attrs(i, mode):
    if mode == 'lock':
        value = 1
    if mode == 'unlock':
        value = 0
    for ax in axis:
        try:
            cmds.setAttr(i + ax, lock=value, k=1)
        except:
            print_dev(msg='Error lock or unlocking '+ i)
#-----------------------------------------------------------
def break_connections(i):
    # break connection
    for ax in axis:
        try:
            # get conn
            conn = cmds.listConnections(i + ax , source=1 , p=1)[0]
            # break conn
            cmds.disconnectAttr(conn, i + ax)
        except:
            pass
#-----------------------------------------------------------
def delete_objectSets(objsets):
    try:
        for item in objsets:
            nodeT = (cmds.nodeType(item))
            if nodeT:
                # object set
                if nodeT == 'objectSet':
                    cmds.delete(item)
                    continue
                # constraints
                if nodeT == 'parentConstraint':
                    cmds.delete(item)
                    continue
                if nodeT == 'scaleConstraint':
                    cmds.delete(item)
                    continue
                if nodeT == 'pointConstraint':
                    cmds.delete(item)
                    continue
                if nodeT == 'orientConstraint':
                    cmds.delete(item)
                    continue
                if nodeT == 'aimConstraint':
                    cmds.delete(item)
    except:
        print_dev('Error removing objectSet')
#----------------------------------------------------------- 
def delete_MV_selected():
    sel = cmds.ls(sl=1)
    if len(sel) == 1:
        # last numer
        numb = sel[0][-1:]
        cmds.delete(group_for_groups+'_'+numb)
    else:
        cmds.warning('Select the control of the MV you want to remove')
#-----------------------------------------------------------
def skip_mesh_if_is_too_far(s):
    # put list on result
    removed_meshes = []
    for item in s:
        transX = cmds.xform(item, q=1, ws=1, sp=1)[0]
        transZ = cmds.xform(item, q=1, ws=1, sp=1)[2]
        if transX > treshold_far_away:
            removed_meshes.append(item)
            continue
        if transX < -treshold_far_away:
            removed_meshes.append(item)
            continue
        if transZ > treshold_far_away:
            removed_meshes.append(item)
            continue
        if transZ < -treshold_far_away:
            removed_meshes.append(item)
            continue
    if removed_meshes:
        # remove items from orig sel
        for item in removed_meshes:
            s.remove(item)
        # confirm dialog
        if skip_mesh_if_is_too_far_status == 1:
            confirm = confirm_dialog(message = skip_meshes_msg)
            if confirm == dont_show_again_msg:
                write_on_file(replace_this = 'skip_mesh_if_is_'+'too_far_status = 1',
                for_this='skip_mesh_if_is_too_far_status = 0')
    return s
#-----------------------------------------------------------
def save_cam_attrs():
    if cmds.getAttr(saved_cam+'.visibility'):
        # save cam
        cam_trans = cmds.getAttr(camMV+'.translate')[0]
        cam_rotate = cmds.getAttr(camMV+'.rotate')[0]
        cmds.setAttr (saved_cam+'.translate', cam_trans[0], cam_trans[1], cam_trans[2], )
        cmds.setAttr (saved_cam+'.rotate', cam_rotate[0], cam_rotate[1], cam_rotate[2], )
    else:
        cmds.setAttr(saved_cam+'.visibility', 1)
def load_cam_attrs():
    cam_trans = cmds.getAttr(saved_cam+'.translate')[0]
    cam_rotate = cmds.getAttr(saved_cam+'.rotate')[0]
    cmds.setAttr (camMV+'.translate', cam_trans[0], cam_trans[1], cam_trans[2] )
    cmds.setAttr (camMV+'.rotate', cam_rotate[0], cam_rotate[1], cam_rotate[2] )
#-----------------------------------------------------------
def viewport_HD():
    # turn on viewport 2.0
    mel.eval('ActivateViewport20')
    # turn on SS
    try:
        cmds.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)
    except:
        pass
    # Turn on AO
    try:
        cmds.setAttr ("hardwareRenderingGlobals.ssaoEnable", 1)
    except:
        pass
    # Turn on display textures
    try:
        # detect current  panel
        curPanel = cmds.getPanel (withFocus=1)
        cmds.modelEditor (curPanel, e=1, displayTextures=1)
    except:
        pass
#-----------------------------------------------------------
def print_dev(msg, prt=''):
    if imp_or_loc == '':
        if prt == 'On':
            print(msg+'\n'),
        else:
            cmds.warning(msg)
#-----------------------------------------------------------
def print_distance_X_Z():
    sel = cmds.ls(sl=1)
    if sel:
        for item in sel:
            transX = cmds.xform(item, q=1, ws=1, sp=1)[0]
            transZ = cmds.xform(item, q=1, ws=1, sp=1)[2]
            print (transX, transZ)
#-----------------------------------------------------------
def select_all_vis_meshes_dev():
    sel = select_all_vis_meshes()
    cmds.select(sel)
    for item in sel:
        print (item)
#-----------------------------------------------------------
def give_me_type_node():
    selection = cmds.ls(sl=True)
    for obj in selection:
        objType = cmds.objectType (obj)
        print (str(obj) + " " + str(objType) + "\n" ),
#-----------------------------------------------------------
def progress_update(status_text='act?'):
    if progress_bar_active == 1:
        cmds.progressWindow(e=1, step=1, status = status_text )
#-----------------------------------------------------------
def progress_start(title=[], maxV=[], ends=[] ):
    try:
        if progress_bar_active == 1:
            cmds.progressWindow(endProgress=1)
            cmds.progressWindow(    title=title,
                                    maxValue=len(maxV),
                                    isInterruptable=True )
            if ends == 1:
                cmds.progressWindow(endProgress=1)
    except:
        pass
#-----------------------------------------------------------
def contact_window():
    # Contact Window  
    if cmds.window (nameTool+'_Contact', exists=True ):
        cmds.deleteUI (nameTool+'_Contact')
    windowContact = cmds.window (nameTool+'_Contact', title="Contact", s=0)
    #
    cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0),
    columnWidth=[(1, 100), (2, 250)] )
    # Name
    cmds.text( label='Name:  ' )
    name = cmds.textField(text='Francisco Cerchiara Montero', editable=True)
    # Email
    cmds.text( label='Email:  ' )
    Email = cmds.textField(text='FranCM127@hotmail.com', editable=True)
    # Linktree 
    cmds.text( label='Linktree:  ' )
    linkTree = cmds.textField(text='linktr.ee/FranCerchiara', editable=True)
    cmds.popupMenu()
    cmds.menuItem(l='Go to web', c= "cmds.launch( web = '%s' )" % (linktree_link) )
    # 
    cmds.showWindow( windowContact)
#-----------------------------------------------------------
if __name__ == '__main__':
    # if the script runs locally all the print and warning messages will appear
    imp_or_loc = ''
    GUI()
else:
    imp_or_loc = 'MV.'
#-----------------------------------------------------------
#========#========#========#========#========#========#
#                 T H E   E N D
#========#========#========#========#========#========#

'''
---------------------------------
Upcoming features and bug fixes:

maya 2022 bugs:
- glitchy viewport, make it work in render engine Open GL.
- NurbsSurfaces eyes don't work in ED-405 rig.
Features:
- Add MV button.
- Be able to save your current setting, sliders and BG color as default.
- most of the default setting now are as numbers inside the code,
would be better as a user friendly option in the settings 
tab and directly overriding the file.
- MV camera position matching the latest active camera (keeping in mind the lens)
---------------------------------
'''


 