import pymel.core as pm
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import QFile
from SassyMaterialsUI import Ui_MainWindow
import json
import pymel.mayautils as pmu
import pymel.core.system as ps
import os

# functions

def print_selected_attributes():
    selected = pm.ls(sl=True)[0]
    list_attr = pm.listAttr(selected, c=True)
    print("BONUS! Printing attributes for selected node: {} of type {}".format(str(selected),str(pm.nodeType(selected))))
    for attr in list_attr:
        print(attr)

def connect_file_to_place(filenode,placenode):
    pm.connectAttr(placenode.coverage,filenode.coverage,force=True)
    pm.connectAttr(placenode.translateFrame,filenode.translateFrame,force=True)
    pm.connectAttr(placenode.rotateFrame,filenode.rotateFrame,force=True)
    pm.connectAttr(placenode.mirrorU,filenode.mirrorU,force=True)
    pm.connectAttr(placenode.mirrorV,filenode.mirrorV,force=True)
    pm.connectAttr(placenode.stagger,filenode.stagger,force=True)
    pm.connectAttr(placenode.wrapU,filenode.wrapU,force=True)
    pm.connectAttr(placenode.wrapV,filenode.wrapV,force=True)
    pm.connectAttr(placenode.repeatUV,filenode.repeatUV,force=True)
    pm.connectAttr(placenode.offset,filenode.offset,force=True)
    pm.connectAttr(placenode.rotateUV,filenode.rotateUV,force=True)
    pm.connectAttr(placenode.noiseUV,filenode.noiseUV,force=True)
    pm.connectAttr(placenode.vertexUvOne,filenode.vertexUvOne,force=True)
    pm.connectAttr(placenode.vertexUvTwo,filenode.vertexUvTwo,force=True)
    pm.connectAttr(placenode.vertexUvThree,filenode.vertexUvThree,force=True)
    pm.connectAttr(placenode.outUV,filenode.uv,force=True)
    pm.connectAttr(placenode.outUvFilterSize,filenode.uvFilterSize,force=True)

def check_attribute_float3(attribute,checknode):
    return pm.attributeQuery(attribute,node=checknode,at=True)=="float3"

def get_imagefile(basedir):
    dialog = QFileDialog()
    path = dialog.getOpenFileName(dialog,"Select image file",basedir,"Image Files (*.png *.jpg *.jpeg *.tiff *.exr)")
    path = str(path[0])
    return path
    
def get_folder(basedir):
    dialog = QFileDialog()
    path = dialog.getExistingDirectory(dialog,"Select folder",basedir)
    path = str(path)
    return path

def show_message(message_text):
    msgBox = QMessageBox()
    msgBox.setText(message_text)
    msgBox.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.read_json()

        #setup box defaults
        self.set_lines_toStandard()

        #define button events

        #preset button
        self.ui.button_resetnames.clicked.connect(self.set_lines_toStandard)

        #root folder
        self.ui.pushButton.clicked.connect(self.change_searchrootfolder)

        #search for files button
        self.ui.button_searchfolder.clicked.connect(self.search_files)

        #Json Reset
        self.ui.button_readJSON.clicked.connect(self.read_json)

        #browse folder buttons next to text
        self.ui.button_browse_diffuse.clicked.connect(lambda: self.Change_imagefile(self.ui.line_diffuse))
        self.ui.button_browse_roughness.clicked.connect(lambda: self.Change_imagefile(self.ui.line_roughness))
        self.ui.button_browse_metalness.clicked.connect(lambda: self.Change_imagefile(self.ui.line_metalness))
        self.ui.button_browse_reflectivity.clicked.connect(lambda: self.Change_imagefile(self.ui.line_reflectivity))
        self.ui.button_browse_refraction.clicked.connect(lambda: self.Change_imagefile(self.ui.line_refraction))
        self.ui.button_browse_opacity.clicked.connect(lambda: self.Change_imagefile(self.ui.line_opacity))
        self.ui.button_browse_normal.clicked.connect(lambda: self.Change_imagefile(self.ui.line_normal))
        self.ui.button_browse_height.clicked.connect(lambda: self.Change_imagefile(self.ui.line_height))
        self.ui.button_browse_emissive.clicked.connect(lambda: self.Change_imagefile(self.ui.line_emissive))

        #the big boy
        self.ui.button_creatematerial.clicked.connect(self.make_material)

        # about button

        self.ui.button_about.clicked.connect(self.about_message)

        #setup root folder var
        basename = str(ps.sceneName())
        basesplit = basename.split('/')
        basesplit.pop(len(basesplit) - 1)
        self.basedir = "/".join(basesplit) + "/"

    def read_json(self):
        scriptfolder = pmu.getUserScriptsDir()
        jsonfile = open(scriptfolder + "/SassyMaterials_Presets/mat_setup.json", "r").read()
        prefixfile = open(scriptfolder + "/SassyMaterials_Presets/mat_prefix.json", "r").read()
        self.jsonlist = json.loads(jsonfile)
        self.prefixlist = json.loads(prefixfile)
        self.prefix_preset = self.prefixlist[0]

        self.setup_combobox()

    def setup_combobox(self):
        self.ui.presetbox.clear()
        self.ui.presetbox_prefix.clear()

        for preset in self.jsonlist:
            itemtext = preset["Preset"]
            print(itemtext)
            self.ui.presetbox.addItem(itemtext)

        for convention in self.prefixlist:
            con_itemtext = convention["Prefixname"]
            print(con_itemtext)
            self.ui.presetbox_prefix.addItem(con_itemtext)

    def Change_imagefile(self,line_instance):
        base = self.ui.line_folder.text()
        if base == "":
            base = self.basedir
        path = get_imagefile(base)
        if path != "":
            line_instance.setText(path)

    def set_lines_toStandard(self):
        preset = self.prefixlist[self.ui.presetbox_prefix.currentIndex()]["Prefixes"]
        for ref in preset:
            reference = eval(ref)
            self.change_line(reference,preset[ref])

    def change_searchrootfolder(self):
        base = self.ui.line_folder.text()
        if base == "":
            base = self.basedir
        path = get_folder(base)
        print(path)
        if path != "":
            self.ui.line_folder.setText(path)

    def line_check_list_setup(self):
        self.linelist = [self.ui.line_diffuse, self.ui.line_roughness, self.ui.line_metalness, self.ui.line_reflectivity,
                    self.ui.line_refraction, self.ui.line_opacity, self.ui.line_normal, self.ui.line_height,
                    self.ui.line_emissive]
        self.checklist = [self.ui.check_diffuse.checkState(), self.ui.check_roughness.checkState(),
                     self.ui.check_metalness.checkState(), self.ui.check_reflectivity.checkState(),
                     self.ui.check_refraction.checkState(), self.ui.check_opacity.checkState(),
                     self.ui.check_normal.checkState(), self.ui.check_height.checkState(),
                     self.ui.check_emissive.checkState()]

    def about_message(self):
        if self.ui.line_prefix.text() == "TOOL_ATTR":
            print_selected_attributes()
        else:
            show_message("Sassy Materials v1.0 - An automated way of setting up materials.\n \n- Sas van Gulik 2021 - \nFor my students at HKU, in Singapore, and everyone who needs it. \n \nTIP! \nIf you are making a preset in mat_setup.JSON, if one of the maps is not compatible with the shader,\njust write 'none', 'None', or '' as the attribute, and it'll never make the file node, even if the checkbox is checked.\n\n TIP 2!\nType 'TOOL_ATTR' in the substring search, and press the about button to print information about a selected node to the script console! \n \nGood luck and have fun!")

    def change_line(self,line_obj,settext):
        line_obj.setText(settext)

    def search_files(self):
        rootdir = self.ui.line_folder.text()
        itemlist = os.listdir(rootdir)

        self.line_check_list_setup()

        linelist = self.linelist
        checklist = self.checklist

        for idx, line in enumerate(linelist):
            if checklist[idx] == False:
                continue
            substring = line.text()
            add_sub = self.ui.line_prefix.text()

            for file in itemlist:
                print(rootdir + "/" + file)
                if substring in file:
                    if add_sub != "" and add_sub in file:
                        line.setText(rootdir + "/" + file)
                    elif add_sub == "":
                        line.setText(rootdir + "/" + file)

    def make_material(self):
        # we're gonna make the material now

        self.line_check_list_setup()

        linelist = self.linelist
        checklist = self.checklist
        # define list of keys to look at
        operationlist = ["Diffuse", "Roughness", "Metallic", "Reflectivity", "Refraction", "Opacity", "Normal", "Height", "Emissive"]

        dict_info = self.jsonlist[self.ui.presetbox.currentIndex()]  # get current preset

        ######################################
        # create base node with shader graph #
        ######################################

        shader_name = self.ui.line_materialname.text()
        shader_type = dict_info["Material"]

        base_material_node = pm.shadingNode(shader_type, asShader=True, name=shader_name + "_MAT")
        base_SG_node = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name + "_SG")

        pm.connectAttr(base_material_node.outColor, base_SG_node.surfaceShader, force=True)

        # run code that sets up things for initialising the node.
        exec (dict_info["Material_postcode"])

        #######################################################################################################################################################
        # Using order of operationlist, create filenodes, connect them with 1 placement node, and then use the dictionary to connect to appropriate attribute #
        #######################################################################################################################################################

        UVnode = pm.shadingNode("place2dTexture", asUtility=True, name=shader_name + "_UV")

        for idx, operation in enumerate(operationlist):
            if not checklist[idx] or dict_info[operation] == "None" or dict_info[operation] == "none" or dict_info[operation] == "":
                # continue if for an entry the checkbox has been turned off
                # continue if an entry in a preset has None, none, or empty sting for a connection
                continue

            if operation == "Normal":
                ###############################################################
                # Setting up normal network, it's settings and configurations #
                ###############################################################

                # build the normal network

                file_node = pm.shadingNode("file", asTexture=True, name=shader_name + "_Normal")

                file_node.setAttr("fileTextureName", linelist[idx].text())

                if self.ui.check_UDIM.checkState():
                    file_node.setAttr("uvTilingMode", 3)

                file_node.setAttr("colorSpace", "Raw")

                connect_file_to_place(file_node, UVnode)

                # collect normal node type and further info
                normal_type = dict_info["Normalnode"]
                normal_class = dict_info["Normalnode_type"]
                normal_isTexture = normal_class == "texture"
                normal_isUtility = normal_class == "utility"

                normal_node = pm.shadingNode(normal_type, asTexture=normal_isTexture, asUtility=normal_isUtility, name=shader_name + "_" + normal_type)

                # post creation code execution

                exec (dict_info["Normal_postcode"])

                # connections
                cur_attribute = str(dict_info["Normal_in"])
                if check_attribute_float3(cur_attribute, normal_node):
                    pm.connectAttr(file_node.outColor, str(normal_node) + "." + cur_attribute, force=True)
                else:
                    pm.connectAttr(file_node.outAlpha, str(normal_node) + "." + cur_attribute, force=True)
                pm.connectAttr(str(normal_node) + "." + str(dict_info["Normal_out"]), str(base_material_node) + "." + str(dict_info["Normal"]), force=True)
                continue

            if operation == "Height":
                #####################################################################
                # Setting up displacement network, it's settings and configurations #
                #####################################################################

                # build the displacement network

                file_node = pm.shadingNode("file", asTexture=True, name=shader_name + "_Displacement")

                file_node.setAttr("fileTextureName", linelist[idx].text())
                if self.ui.check_UDIM.checkState():
                    file_node.setAttr("uvTilingMode", 3)

                file_node.setAttr("colorSpace", "Raw")
                connect_file_to_place(file_node, UVnode)

                # collect displacement node type and further info
                displacement_type = dict_info["Displacementnode"]
                displacement_class = dict_info["Displacementnode_type"]

                displacement_node = pm.shadingNode(displacement_type, asShader=True, name=shader_name + "_" + displacement_type)

                # post creation code execution

                exec (dict_info["Displacement_postcode"])

                cur_attribute = str(dict_info["Displacement_in"])

                if check_attribute_float3(cur_attribute, displacement_node):
                    pm.connectAttr(file_node.outColor, str(displacement_node) + "." + cur_attribute, force=True)
                else:
                    pm.connectAttr(file_node.outAlpha, str(displacement_node) + "." + cur_attribute, force=True)
                pm.connectAttr(str(displacement_node) + "." + str(dict_info["Displacement_out"]), str(base_SG_node) + "." + str(dict_info["Height"]), force=True)

                continue

            file_node = pm.shadingNode("file", asTexture=True, name=shader_name + "_" + operation)

            # assign texture file
            file_node.setAttr("fileTextureName", linelist[idx].text())

            # if UDIM is checked, now we turn it on.
            if self.ui.check_UDIM.checkState():
                file_node.setAttr("uvTilingMode", 3)

            # assign UV node to file node
            connect_file_to_place(file_node, UVnode)

            cur_attribute = dict_info[operation]

            if operation == "Metallic" or operation == "Roughness":
                # set color space to raw for all maps that are not color (diffuse)
                file_node.setAttr("colorSpace", "Raw")

            if operation == "Emissive":
                # make sure that emission parameters get properly set, when emission texture is present
                exec (dict_info["Emissive_postcode"])

            if operation == "Opacity" and self.ui.check_invertopacity.checkState():
                invertnode = pm.shadingNode("reverse", asUtility=True, name=shader_name + "reverse")
                pm.connectAttr(file_node.outColor, invertnode.input, force=True)
                pm.connectAttr(invertnode.output, str(base_material_node) + "." + str(cur_attribute), force=True)
                continue

            if not check_attribute_float3(cur_attribute, base_material_node):
                pm.connectAttr(file_node.outAlpha, str(base_material_node) + "." + str(cur_attribute), force=True)
            else:
                pm.connectAttr(file_node.outColor, str(base_material_node) + "." + str(cur_attribute), force=True)


def main():
    # create window
    win = MainWindow()
    win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    # show window
    win.show()