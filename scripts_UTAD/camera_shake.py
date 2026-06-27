
import maya.cmds as cmds

CAMERA = "sq003_sh030"  #Name of your camera
SHAKE_GRP = f"{CAMERA}_shake_grp"

if not cmds.objExists(CAMERA):
    cmds.error(f"Camera '{CAMERA}' does not exist.")

# Create shake group if missing
if not cmds.objExists(SHAKE_GRP):
    parent = cmds.listRelatives(CAMERA, parent=True)
    SHAKE_GRP = cmds.group(CAMERA, name=SHAKE_GRP)
    if parent:
        cmds.parent(SHAKE_GRP, parent[0])

# Add control attributes
def add_attr(attr, default):
    if not cmds.attributeQuery(attr, node=SHAKE_GRP, exists=True):
        cmds.addAttr(
            SHAKE_GRP,
            longName=attr,
            attributeType="double",
            defaultValue=default,
            keyable=True
        )

# Amplitude and Freq values
add_attr("shakeAmp", 0.07)    # Gentle rotation
add_attr("shakeFreq", 7.0)    # Gentle mechanic motion

# Expression
expr = f"""
float $t = time * {SHAKE_GRP}.shakeFreq;
float $amp = {SHAKE_GRP}.shakeAmp;

// Ultra-subtle subway vibration
{SHAKE_GRP}.rotateX = noise($t) * $amp * 0.6;        // Pitch
{SHAKE_GRP}.rotateY = noise($t + 10) * $amp * 0.1;   // Nearly zero yaw
{SHAKE_GRP}.rotateZ = noise($t + 20) * $amp * 0.9;   // Gentle roll
"""

expr_name = f"{SHAKE_GRP}_expr"
if cmds.objExists(expr_name):
    cmds.delete(expr_name)

cmds.expression(
    s=expr,
    name=expr_name,
    object=SHAKE_GRP,
    alwaysEvaluate=True,
    unitConversion="all"
)

print("Subway camera shake applied.")
