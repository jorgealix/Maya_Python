cacheNode = hou.node('/obj/OUT_SIM/liquid_cache/render')
cacheNode.render(frame_range = (hou.frame(), hou.frame()))