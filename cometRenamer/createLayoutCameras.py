import maya.cmds as cmds
def create():

    #Reference Audio sequence file

    multipleFilters = "Audio Files (*.wav);;All Files (*.*)"
    audiopath = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, fm=1)
    cmds.file( audiopath, i=True )

    #Open file with list of metadata of shots
    fileHandle = open('C:\Users\drakhar\Downloads\shots.txt', 'r' )
    myShots  = {"clip":"","nameShot":"","inFrame":"","outFrame":"","duration":""}
    str1 = fileHandle.read()
    fileHandle.close()

    #Separate cameras
    cams = str1.split()

    #Create list for cemeras
    cameras = []

    #Create dict for cameras attribs
    for sh in range (0,len(cams)):
        shotComp = cams[sh].split(",")
        print shotComp
        myShots['clip'] = shotComp[0]
        myShots['nameShot'] = shotComp[1] + "_cam"
        myShots['inFrame'] = shotComp[2]
        myShots['outFrame'] = shotComp[3]
        myShots['duration'] = shotComp[4]

        #Create new camera and add to the list
        cam = cmds.camera()
        newCamName = cmds.rename(cam[0], myShots['nameShot'])

        #Conform camera
        cmds.camera( newCamName, e=True, dfg=1 )
        cmds.camera( newCamName, e=True, dr=1 )
        cmds.camera( newCamName, e=True, dsa=1 )
        cmds.camera( newCamName, e=True, ovr=1.4 )

        #Add to the list
        cameras.append(newCamName)
        cmds.parent( str(newCamName), 'cams', relative=True  )
        myShot = cmds.shot(
            ("clip" + str(sh)),
            cc= myShots['nameShot'],
            sn=myShots['nameShot'],
            st=myShots['inFrame'],
            et=myShots['outFrame'],
            sst=myShots['inFrame'],
            set=myShots['outFrame']
            )
    print cameras
