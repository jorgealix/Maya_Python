import os
import subprocess
import sys
# Este script es para convertir las texturas a formato tx dentro de una carppeta /tx
# Para ejecutar este script desde una shell de windows escribimos
# python P:\LIBRERIA\MAYA_SCRIPTS\PYTHON\convertTexturesToTx.py "Unidad:\...\path"

def sourcepath(input_dir):
    # Set the path to the directory containing the textures to convert
    #input_dir = "P:/PROYECTOS/DIN_DIM/VFX/ASSETS/Character/DIM_DindimCG/STEPS/TXT/MAYA/sourceimages"
    input_dir.replace('\\', '/')
    print(input_dir)

    # Set the path to the directory where the converted textures will be saved
    output_dir = str(input_dir) #+ '/tx'
    if not os.path.exists(str(output_dir)):
        # Create a new directory because it does not exist
        os.makedirs(str(output_dir))

    # Set the path to the maketx.exe executable
    maketx_exe = "C:/Program Files/Autodesk/Arnold/maya2024/bin/maketx.exe"

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):

        # Check if the file has a supported extension
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Set the input and output file paths
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".tx")

            # Call maketx.exe to convert the texture
            subprocess.run([maketx_exe, "-u", "-v", "--checknan", "--unpremult" ,"--colorconvert", "sRGB", "ACEScg", "-o", output_path, input_path])
        if filename.endswith(".exr") or filename.endswith(".tif"):
            # Set the input and output file paths
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".tx")

            # Call maketx.exe to convert the texture
            subprocess.run([maketx_exe, "-u", "-v", "--checknan", "--unpremult", "--colorconvert", "Raw", "ACEScg" , "-o", output_path, input_path])

sourcepath("F:/WORK/CursoSubstance/JudyHops/sourceimages")