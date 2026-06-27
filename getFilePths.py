import maya.cmds as cmds
import os


def get_all_file_node_paths():
    """Get all file paths from file nodes in the Maya scene."""
    file_nodes = cmds.ls(type='file')
    file_paths = []

    for node in file_nodes:
        texture_path = cmds.getAttr(f"{node}.fileTextureName")
        if texture_path:
            file_paths.append(texture_path)

    return file_paths


def find_files_recursively(search_dir, filename):
    """Search for a file recursively within a directory."""
    matched_files = []
    for root, _, files in os.walk(search_dir):
        if filename in files:
            matched_files.append(os.path.join(root, filename))

    return matched_files


def main(search_directory):
    """Main function to find missing texture files in a given directory."""
    missing_files = {}
    file_paths = get_all_file_node_paths()

    for path in file_paths:
        filename = os.path.basename(path)
        found_files = find_files_recursively(search_directory, filename)

        if found_files:
            print(f"Found '{filename}' in:")
            for file in found_files:
                print(f"  {file}")
        else:
            missing_files[filename] = path
            print(f"Missing: {filename} (Original Path: {path})")

    return missing_files


# Example usage

search_directory = "F:/WORK/CHANGELLINGS/03_Produccion/3D_Assets/Personajes/Esfinge/Maya"
missing_files = main(search_directory)