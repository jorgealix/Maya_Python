import maya.cmds as cmds
matches = cmds.ls(f"*.model_grp", long=True) or cmds.ls(f"*:model_grp", long=True)
selected_objects = cmds.ls(matches[0])
# Loop through each selected object and export it as a USD file using its name
for obj in selected_objects:
    # Get the short name of the object (without the full path)
    short_name = cmds.ls(obj, shortNames=True)[0]
    cmds.select( short_name )
    # Set the export path based on the object's name
    export_path = "P:/Jorge_Medina/MayaTests/USD_exportation/" + short_name.split(":")[0] + ".usda"
    print( export_path )
    print( "\n" )
    cmds.file(export_path, 
                force=True, 
                type="USD Export",
                defaultExtensions=False, 
                options=";exportUVs=1; exportColorSets=1; exportComponentTags=1; defaultMeshScheme=catmullClark; defaultUSDFormat=usda; parentScope=Arnold_Data; jobContext=[Arnold]; materialsScopeName=mtl;stripNamespaces=1", 
                exportSelected=True)