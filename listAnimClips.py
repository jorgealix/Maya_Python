## Lista todos los clips creaos para cada character
from os import listdir
from os.path import isfile, join

mypath = 'P:\PROYECTOS\CAMPEONES_2\VFX\ASSETS\Character'
myclips = '\STEPS\RIG\MAYA\clips'
assetList = (os.listdir(mypath))
totalclips = 0
with open('P://PROYECTOS//CAMPEONES_2//VFX//ASSETS//clips.txt', 'a+') as f:
    f.truncate(0)
    for assets in assetList:
        listDir = os.listdir(mypath + '\\' + assets)
        if '.DS_Store' in listDir:
            listDir.remove('.DS_Store')
        if '.mayaSwatches' in listDir:
            listDir.remove('.mayaSwatches')
        if listDir:
            if os.path.isdir(mypath + '\\' + assets + myclips) is True:
                cliplist = (os.listdir(mypath + '\\' + assets + myclips))
                if cliplist:
                    totalclips = totalclips + (len(cliplist))
                    print('_________________________________')
                    for clipanim in cliplist:
                        print(assets, clipanim)
                        f.write(assets + ' ' + clipanim + "\n")
                    f.write('_________________________________' + "\n")
f.close()
print('P:/PROYECTOS/CAMPEONES_2/VFX/ASSETS/clips.txt')