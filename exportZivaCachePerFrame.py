import maya.mel as mel
import maya.cmds as cmds
startframe = cmds.playbackOptions(query=True, minTime=True)
endframe = cmds.playbackOptions(query=True, maxTime=True)
current_project_path = cmds.workspace(q=True, rd=True)
normalized_path = os.path.normpath(current_project_path)
path_components = normalized_path.split(os.sep)
cacheZivaFolder = (current_project_path + 'cache/')
selection = cmds.ls(selection=True)
for sel in selection:
    if ':' in sel:
        nodeName = sel.split(':')
filecacheZivaFolder = (cacheZivaFolder + str(path_components[6]) + '_' + nodeName[1])
print(filecacheZivaFolder)
for i in xrange( int(startframe),int(endframe) ):
    cmds.currentTime( i )
    zivapath = (filecacheZivaFolder + '.%04i.zCache' % i)
    print(zivapath)
    mel.eval('zCache -save "%s";' % zivapath )
    mel.eval('zCache -clear' )