def create_bbox_from_object(obj_name_uv_from):
    selection = cmds.ls(selection = True)
    for sel in selection:
        cmds.transferAttributes( obj_name_uv_from, sel,
                            transferPositions = 0,
                            transferNormals = 0,
                            transferUVs=1,
                            sourceUvSet = "map1",
                            targetUvSet = "map1", 
                            transferColors = 2,
                            sampleSpace = 4, 
                            sourceUvSpace = "map1", 
                            targetUvSpace = "map1",
                            searchMethod = 3,
                            flipUVs = 0,
                            colorBorders = 1)