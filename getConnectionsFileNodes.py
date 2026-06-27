import maya.cmds as cmds
import os
import shutil
selShader = cmds.ls(selection=True)
print(selShader)
# try:
#     import sgtk
#     print("Module is accessible.")
#     checkSgtkEnv(current_engine)
#     connectedAttrbs()
# except ImportError as e:
#     print(f"Module is not accessible.>>>>Error: {e}")



def checkSel(selShader):
    print(selShader, cmds.nodeType(selShader))
    global currentProj, preffixes, suffixes
    # Check if there is a selection and node is a shader node
    if not selShader:
        cmds.confirmDialog(t="Oops! Nothing Selected", message='Oops! No Shader Engine Selected.', icon="warning")
    elif not cmds.nodeType(selShader[0]) in ['lambert', 'blinn', 'phong', 'phongE', 'standardSurface', 'surfaceShader', 'useBackground']:
        cmds.confirmDialog(t="Oops! The node is not a shader node.", message='Oops! The node ' + selShader[0] + ' is not a shader node.', icon="warning")
    else:
        currentScene = os.path.abspath(cmds.file(q=True, sn=True))
        currentProj = os.path.split(currentScene)
        preffixes = ("T_", "TC_", "MT_", "RT_", "RT_", "RTC_", "TLP_")
        suffixes = ("_D", "_N", "_R", "_A", "_O", "_B", "_E", "_I", "_M", "_S", "_M", "_H")
        checkNodeType()

def checkNodeType():
    listNodeFile = []
    # Obtener todos los file nodes del Shader Network usando hyperShade
    nodos_shader_network = cmds.hyperShade(listUpstreamNodes = selShader[0])
    if nodos_shader_network:
        for node in nodos_shader_network:
            if cmds.nodeType(node) == 'file':
                listNodeFile.append(node)
        conformFileNodes(listNodeFile)

def conformFileNodes(listNodeFile):
    for nodeFile in listNodeFile:
        file_path = cmds.getAttr(nodeFile + ".fileTextureName")
        if not os.path.exists(file_path):
            cmds.confirmDialog(t="Oops! Missing file", message='Oops! Some files are missing.', icon="warning")
            return None
        fileConnect = cmds.listConnections(nodeFile, plugs=True, source=False, destination=True,
                                           type='lambert' or 'blinn' or 'phong' or 'phongE' or 'standardSurface' or 'surfaceShader' or 'useBackground' or 'bump2d')
        print(nodeFile)

        file_name, file_ext = os.path.basename(file_path).split(".")
        # Check name file textures
        if file_name != asset_name:
            new_file_name = (os.path.dirname(file_path) + "/" + preffixes[0] + asset_name + "_" + selShader[0] + suffixes[0] + "." + file_ext)
            # Check aacces to folder
            if not os.access(os.path.dirname(file_path), os.W_OK):
                say = "Path is not writable."
            else:
                say = new_file_name + " Path is writeable"
                # Allow write file
                f = open(new_file_name, 'w')
                f.write(new_file_name)
                f.close()
            print(say)

            # Copy file with new name and update the call to it in the file node
            try:
                shutil.copy2(file_path, new_file_name)
                cmds.setAttr((nodeFile + ".fileTextureName"),
                             new_file_name,
                             type="string")
            except:
                cmds.setAttr((nodeFile + ".fileTextureName"),
                             new_file_name,
                             type="string")
                print("This file has been processed jet")

def connectedAttrbs():
    # Get connected attribs in the shader engine
    for attr in attributes:
        global sourceAttr, destinationAttr
        # Check correct attrb connection
        if "." not in attr:
            attrSH = (f"{selShader[0]}.{attr}")
            fileConnect = cmds.listConnections(attrSH, s=True, c=True)
            if fileConnect:
                if cmds.connectionInfo(attrSH, isDestination=True):
                    sourceAttr = cmds.connectionInfo(attrSH, sourceFromDestination=True)
                    destinationAttr = cmds.connectionInfo(attrSH, destinationFromSource=True)
                    print(fileConnect[1])
                    checkNodeType(fileConnect)

#checkSgtkEnv(current_engine)
#connectedAttrbs()