# Este script relacciona los nodos de textura con sus path de texturas
import maya.cmds as cmds

def list_texture_files():
    texture_files = set()  # Using a set to avoid duplicate entries
    dict_txtFile_txtNode = {} # Dictionary contents textures path and file nodes
    current_project_path = cmds.workspace(q=True, rd=True)
    print(current_project_path)
    # Get all file nodes in the scene
    file_nodes = cmds.ls(type="file")

    # Iterate through each file node
    for file_node in file_nodes:
        # Get the file path from the file node
        file_path = cmds.getAttr(file_node + ".fileTextureName")
        print(file_node, file_path)
        
        # Update Dictionary contents textures path and file nodes
        additional_items = {file_node:file_path}
        dict_txtFile_txtNode.update(additional_items)
    


        # Example usage:
        get_texture_connections_to_shader(file_node)

            
        
#list_texture_files()

def get_texture_connections_to_shader(file_node):
    # Get connections from the texture node to the shader
    shader_connections = cmds.listConnections(file_node + ".outColor", source=True, destination=False)

    if shader_connections:
        print(f"Connections from {texture_node} to the shader:")
        
        # Print each connected shader node
        for shader_connection in shader_connections:
            print(f"  {shader_connection}")


