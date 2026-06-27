# Este script revisa los jos provenientes de Animtion Library
# y resuelve los nombre de los controles que contienen namespces.
# Se puede indicar desde que parte de la liberría se ejecuta la revisión
# Para ejecutarlo hay que abrir una consola de msdos y escribir:
# C:\Python3.7.9\python.exe P:\LIBRERIA\MAYA_SCRIPTS\PYTHON\jsonRepair.py

import os

root_path = "P:\PROYECTOS\DIN_DIM\STUDIO_LIBRARY\Escenas\SC_65_300\Facial_anim.anim" # Ruta desde donde se ejecuta la revisión
root_path.replace('\\','/')
namespace = '"DINDIM:' # Namespace incluyendo " y :
namespaceUpdated = ''
dirpath= ''
dirnames = []
filenames = []
# Estos son todos los nodos de control del esqueleto a revisar y sustituir en el json
nsCtrllist =["main:root_ctl_0", "main:root_ctl_1", "head:ctl_0", "neck:fk:ctl_2", "neck:fk:ctl_1", "neck:fk:ctl_0",
             "chest:chest_ctl_0", "spine:fk:ctl_2", "spine:fk:ctl_1", "spine:fk:ctl_0", "hip:ctl_0", "main:cog_ctl_0",
             "main:cog_ctl_1", "tail:ctl_0", "tail:ctl_1", "tail:ctl_2", "spine:ik:ctl_2" "spine:ik:ctl_0",
             "L_shoulder:ctl_0", "L_arm:root:ctl_0", "L_arm:limb:fk:ctl_0", "L_arm:limb:fk:ctl_1",
             "L_arm:extremity:fk:root_ctl_0", "L_arm:extremity:fk:ctl_0", "L_arm:digit_0:ctl_0",
             "R_shoulder:ctl_0", "R_arm:root:ctl_0", "R_arm:limb:fk:ctl_0", "R_arm:limb:fk:ctl_1",
             "R_arm:extremity:fk:root_ctl_0", "R_arm:extremity:fk:ctl_0", "R_arm:digit_0:ctl_0", "R_leg:root:ctl_0",
             "R_leg:limb:ik:root_ctl", "R_leg:limb:ik:up_ctl", "R_leg:extremity:ik:root_ctl_0", "R_leg:extremity:ik:srt_ctl",
             "R_leg:extremity:ik:tip_ctl", "R_leg:extremity:ik:back_ctl", "R_leg:extremity:ik:ctl_0", "R_leg:extremity:ik:ctl_1",
             "R_leg:extremity:ik:ctl_2", "R_leg:digit_1:fk:ctl_0", "R_leg:digit_2:fk:ctl_0", "R_leg:digit_0:fk:ctl_0",
             "R_leg:digit_0:fk:ctl_1", "R_leg:digit_1:fk:ctl_1", "R_leg:digit_2:fk:ctl_1", "L_leg:root:ctl_0",
             "L_leg:limb:ik:root_ctl", "L_leg:limb:ik:up_ctl", "L_leg:extremity:ik:ctl_0", "L_leg:extremity:ik:back_ctl",
             "L_leg:extremity:ik:srt_ctl", "L_leg:extremity:ik:root_ctl_0", "L_leg:extremity:ik:tip_ctl", "L_leg:extremity:ik:ctl_1",
             "L_leg:extremity:ik:ctl_2", "L_leg:digit_2:fk:ctl_0", "L_leg:digit_1:fk:ctl_0", "L_leg:digit_0:fk:ctl_0",
             "L_leg:digit_2:fk:ctl_1", "L_leg:digit_1:fk:ctl_1", "L_leg:digit_0:fk:ctl_1", "chest:chest_ctl_1",
             "spine:ik:ctl_1", "spine:ik:ctl_2", "spine:ik:ctl_0", "neck:ik:ctl_2", "neck:ik:ctl_0", "neck:ik:ctl_1", "main_n:cog_ctl_1",
             "main_n:cog_ctl_0", "main_n:cog_ctl_1", "face:doubleChin_ctl", "face:D_jaw_ctl", "face:tongue_ctl_0", "face:tongue_ctl_1",
             "face:tongue_ctl_2", "face:tongue_ctl_3", "face:R_lip_ctl", "face:L_lip_ctl",  "face:LU_lip_ctl_0", "face:LD_lip_ctl_0",
             "face:RU_lip_ctl_0", "face:RD_lip_ctl_0", "face:R_eye_ctl", "face:R_pupil_ctl", "face:RD_eyelid_ctl", "face:RU_eyelid_ctl",
             "face:R_membrana_ctl", "face:RU_eyelid_ctl_1", "face:RU_eyelid_ctl_0", "face:RO_eyelid_ctl", "face:RI_eyelid_ctl",
             "face:RD_eyelid_ctl_0", "face:RD_eyelid_ctl_1", "face:R_brow_ctl", "face:R_brow_ctl_2", "face:R_brow_ctl_1",
             "face:R_brow_ctl_0", "face:R_eyeTarget_ctl", "face:R_orbit_ctl_0", "face:R_orbit_ctl_1", "face:R_malar_ctl",
             "face:R_bucinator_ctl", "face:L_malar_ctl", "face:L_bucinator_ctl", "face:L_eye_ctl", "face:LU_eyelid_ctl_0",
             "face:LU_eyelid_ctl_1", "face:LU_eyelid_ctl_2", "face:LO_eyelid_ctl", "face:LD_eyelid_ctl_2", "face:LD_eyelid_ctl_1",
             "face:LD_eyelid_ctl_0", "face:LI_eyelid_ctl", "face:RU_eyelid_ctl_2", "face:RD_eyelid_ctl_2", "face:L_membrana_ctl",
             "face:L_pupil_ctl", "face:LU_eyelid_ctl", "face:LD_eyelid_ctl", "face:L_eyeTarget_ctl",  "face:L_brow_ctl",
             "face:L_brow_ctl_0", "face:L_brow_ctl_1", "face:L_brow_ctl_2", "face:L_orbit_ctl_0", "face:L_orbit_ctl_1"]

# Iteramos todos los archivos .joson que encontremos en la carpeta de Animation Library
for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        if filename.endswith('.json'):
            jsonToRepair = (dirpath + '/' + filename)
            #for ctrl in ctrlList:
            for nsCtrl in nsCtrllist:
                nsCtrlUpdated = nsCtrl.replace(':', '_') # Sustituimos los : por _ en la lista y actualizamos el nuevo nombre del control
                #namespaceUpdated = (namespace + ctrl)
                print(jsonToRepair, nsCtrlUpdated)
                with open(jsonToRepair, "r") as f:
                    text = f.read()
                text = text.replace(nsCtrl, nsCtrlUpdated) # Sustituimos los nombres viejos de los controles por los nuevos sin :
                text = text.replace(namespace, '"') # Si queremos sustituir los namespace por " o lo que queramos
                with open(jsonToRepair, "w") as f:
                    f.write(text)

