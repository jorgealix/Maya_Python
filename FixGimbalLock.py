import maya.cmds as cmds
curve_name = cmds.ls(selection = True)
def detect_gimbal_lock(curve_name):
    # Get the rotation values from the curve
    rotation_x = cmds.getAttr(str(curve_name[0]) + ".rotateX")
    rotation_y = cmds.getAttr(str(curve_name[0])  + ".rotateY")
    rotation_z = cmds.getAttr(str(curve_name[0])  + ".rotateZ")

    # Check for gimbal lock by comparing the values
    if abs(rotation_x % 90) < 0.0001 and abs(rotation_y % 90) < 0.0001:
        # Gimbal lock detected
        print("Gimbal lock detected in curve: " + curve_name[0])
    else:
        # No gimbal lock detected
        print("No gimbal lock detected in curve: " + curve_name[0])
detect_gimbal_lock(curve_name)