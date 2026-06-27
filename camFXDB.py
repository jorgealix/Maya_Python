#import camFXDB;camFXDB.initialize();
#Flimback Matcher. Creates camera like you want.

import maya.cmds as cmds
import re
import sys
encoding = 'utf-8'
pythonVersion = sys.version_info[0]
test=['feed','articles','film-back-calculator','about-2','contact','donate','lens-image-circle-and-sensor-imaging-area','image-circle-database','phfx','camera-apertures-and-image-formats','dslr-sensor-formats','dslr-sensor-dimensions-table','film-scanning-dimensions','film-back-calculator']

def initialize():
    url='http://www.vfxcamdb.com'
    html=''
    if pythonVersion<3:
        import urllib2
        req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        html = urllib2.urlopen(req).read()
    else:
        import urllib.request
        req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        html1 = urllib.request.urlopen(req).read()
        html=html1.decode(encoding)
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    #menuLinks=[]
    global vfxcamdbUIStuff
    vfxcamdbUIStuff={}
    buildUI(links)

def buildUI(links):
    menuItems=[]
    if cmds.window('vfxcamdbUI',ex=True):
        cmds.deleteUI('vfxcamdbUI',window=True)
    cmds.window('vfxcamdbUI',sizeable=True, title='vfxcamdbUI - v0.2.0')
    cmds.columnLayout('vfxcamdbUIMC',adj=True,cat=["both",18])
    cmds.separator(h=20,style="none")
    optMenu=cmds.optionMenu(label="Camera")
    cmds.optionMenu(optMenu,e=1,cc='camFXDB.getInfo("' + optMenu+ '")')
#    print links
    for link in links:
        if link[0].startswith("http"):
#            print link[0]
            tempitem=link[0].replace('http://vfxcamdb.com/','')
            tempitem=tempitem.replace('https://vfxcamdb.com/','')
            tempitem=tempitem.replace('camera/','')
            tempitem=tempitem.replace('format/','')
#            print tempitem
            spl=link[0].split("/")
            if len(spl)==5:
                if "?" not in tempitem and tempitem!='' and tempitem.endswith('.js')!=True and tempitem.endswith('.php')!=True and tempitem.endswith('.png')!=True and tempitem.startswith('category')!=True and tempitem.startswith('http')!=True and tempitem.startswith('wp-')!=True:
                    t=0
                    for testy in test:
                        if tempitem==testy+"/":
                            t=1
                    if t==1:
                        continue
                    menuItems.append(tempitem)
    menuSort=sorted(menuItems)
    for item in menuSort:
        cmds.menuItem(item,p=optMenu)
    cmds.showWindow('vfxcamdbUI')
    getInfo(optMenu)


def getInfo(optMenu):
    tempCam=cmds.optionMenu(optMenu,q=1,v=1)
    global vfxcamdbUIStuff
    vfxcamdbUIStuff={}
    urlTemp='http://www.vfxcamdb.com/'+tempCam

    html=''
    if pythonVersion<3:
        import urllib2
        req = urllib2.Request(urlTemp, headers={ 'User-Agent': 'Mozilla/5.0' })
        html = urllib2.urlopen(req).read()
    else:
        import urllib.request
        req = urllib.request.Request(urlTemp, headers={ 'User-Agent': 'Mozilla/5.0' })
        html1 = urllib.request.urlopen(req).read()
        html=html1.decode(encoding)
    cmds.columnLayout('vfxcamdbUIMC',e=True,h=100)
    if cmds.columnLayout('vfxcamdbUIMCMini',q=1,ex=1):
        cmds.deleteUI('vfxcamdbUIMCMini',layout=True)
    cmds.setParent('vfxcamdbUIMC')
    cmds.columnLayout('vfxcamdbUIMCMini',adj=True)
    cmds.separator(h=30,style="none")
    counter=0
    splitHtml=html.split("\n")
    for line in splitHtml:
## Sensor Type
        if line=="<p><strong>Sensor Type:</strong><br />" or line=="<p><b>Sensor Type:</b><br />":
            sensorType= digReplace(splitHtml[counter+1].replace('</p>',''))
            cmds.rowLayout(nc=2)
            cmds.text("Sensor Type:")
            vfxcamdbUIStuff["sensorType"]=cmds.text("  "+sensorType+"  ",bgc=[.18,.18,.18])
            cmds.setParent('..')
## Shutter
        if line=="<p><strong>Shutter:</strong><br />" or line=="<p><b>Shutter:</b><br />":
            cmds.separator(h=10,style="none")
            shutter= digReplace(splitHtml[counter+1].replace('</p>',''))
            cmds.rowLayout(nc=2)
            cmds.text("Shutter:")
            vfxcamdbUIStuff["shutter"]=cmds.text("  "+shutter+"  ",bgc=[.18,.18,.18])
            cmds.setParent('..')
## Image Resolution
        if line=="<p><strong>Image Resolution:</strong><br />" or line=="<p><b>Image Resolution:</b><br />":
            cmds.separator(h=10,style="none")
            counter2=1
            t="no"
            cmds.text("Image Resolutions:",al="left")
            cmds.separator(h=4,style="none")
            tempScroll=cmds.textScrollList(nr=5)
            vfxcamdbUIStuff["imageResolutionScroll"]=tempScroll
            while t=="no":
                dig1=digReplace(splitHtml[counter+counter2])
                if splitHtml[counter+counter2].startswith("<p><strong") or splitHtml[counter+counter2].startswith("<p><b"):
                     t="yes"
                else:
                    cmds.textScrollList(tempScroll,e=1,append=((dig1.replace('<br />','')).replace('<p>','')).replace('</p>',''))
                counter2=counter2+1
            ht=cmds.textScrollList(tempScroll,q=1,ni=True)
            cmds.textScrollList(tempScroll,e=1,sii=1)
            if ht>10:
                ht=10
            cmds.textScrollList(tempScroll,e=1,nr=ht)
## Sensor Imaging Area
        if line=="<p><strong>Sensor Imaging Area:</strong><br />" or line=="<p><b>Sensor Imaging Area:</b><br />":
            cmds.separator(h=10,style="none")
            counter2=1
            t="no"
            cmds.text("Sensor Imaging Area:",al="left")
            cmds.separator(h=4,style="none")
            tempScroll2=cmds.textScrollList(nr=5)
            vfxcamdbUIStuff["sensorAreaScroll"]=tempScroll2
            while t=="no":
                dig1=digReplace(splitHtml[counter+counter2])
                if splitHtml[counter+counter2].startswith("<span"):
                    counter2=counter2+1
                    continue
                if splitHtml[counter+counter2].startswith("<p><strong>") or splitHtml[counter+counter2].startswith("<p><b"):
                     t="yes"
                else:
                    cmds.textScrollList(tempScroll2,e=1,append=((dig1.replace('<br />','')).replace('<p>','')).replace('</p>',''))
                counter2=counter2+1
            ht=cmds.textScrollList(tempScroll2,q=1,ni=True)
            cmds.textScrollList(tempScroll2,e=1,sii=1)
            if ht>10:
                ht=10
            cmds.textScrollList(tempScroll2,e=1,nr=ht)
##
## Sensor Dimensions
        if line=="<p><strong>Sensor Dimensions:</strong><br />" or line=="<p><b>Sensor Dimensions:</b><br />":
            cmds.separator(h=10,style="none")
            counter2=1
            t="no"
            cmds.text("Sensor Dimensions:",al="left")
            cmds.separator(h=4,style="none")
            tempScroll3=cmds.textScrollList(nr=5)
            vfxcamdbUIStuff["sensorDimensionsScroll"]=tempScroll3
            suff=""
            while t=="no":
                dig1=digReplace(splitHtml[counter+counter2])
                if dig1.startswith("<span"):
                    counter2=counter2+1
                    continue
                if dig1.startswith("<a href"):
                    counter2=counter2+1
                    continue
                if dig1.startswith("<p><em"):
                    suff="   *** "+dig1.replace("<p>","").replace('<em>','').replace("</em>","").replace("<br />","") + " ***"
                    counter2=counter2+1
                    continue
                if splitHtml[counter+counter2].startswith("<p><strong>") or splitHtml[counter+counter2].startswith("<p><b"):
                     t="yes"
                else:
                    cmds.textScrollList(tempScroll3,e=1,append=((dig1.replace('<br />','')).replace('<p>','')).replace('</p>','')+suff)
                counter2=counter2+1
            ht=cmds.textScrollList(tempScroll3,q=1,ni=True)
            cmds.textScrollList(tempScroll3,e=1,sii=1)
            if ht>10:
                ht=10
            cmds.textScrollList(tempScroll3,e=1,nr=ht)
##
## Output Type
        if line=="<p><strong>Output Type:</strong><br />" or line=="<p><b>Output Type:</b><br />" or '>Output Type:<' in line:
            cmds.separator(h=10,style="none")
            cmds.text("Output Types:",al="left")
            cmds.separator(h=4,style="none")
            tempScroll3=cmds.textScrollList(nr=5)
            vfxcamdbUIStuff["outputTypeScroll"]=tempScroll3
            counter2=1
            t="no"
            while t=="no":
                dig1=digReplace(splitHtml[counter+counter2])
                if '<!-- .entry-content -->' in dig1:
                    t="yes"
                    continue
                elif dig1.endswith("</p>"):
                    cmds.textScrollList(tempScroll3,e=1,append=dig1.replace('</p>',''))
                    t="yes"
                elif splitHtml[counter+counter2].startswith("<p>"):
                    cmds.textScrollList(tempScroll3,e=1,append=dig1.replace('<p>','').replace('<br />',''))
                else:
                    cmds.textScrollList(tempScroll3,e=1,append=dig1.replace('<br />','').replace('<p>',''))
                counter2=counter2+1
            ht=cmds.textScrollList(tempScroll3,q=1,ni=True)
            if ht>10:
                ht=10
            cmds.textScrollList(tempScroll3,e=1,nr=ht)
            cmds.textScrollList(tempScroll3,e=1,sc='import maya.cmds as cmds;cmds.textScrollList("' + tempScroll3+ '",e=1,da=True)')
        counter=counter+1
    cmds.separator(h=20,style="none")
    vfxcamdbUIStuff["camName"]=cmds.textFieldGrp(label="Camera Name:",cw=[(1,75),(2,200)],tx='cam_main')
    cmds.columnLayout(cat=["left",40],adj=True)
    vfxcamdbUIStuff["check"]=cmds.checkBox(l=" Use image resolution for render resolution",v=0)
    cmds.setParent('..')
    cmds.separator(h=25,style="none")
    cmds.button(l="Create Camera",c='camFXDB.createCam("' + optMenu + '")')
    cmds.separator(h=40,style="none")
    colH=cmds.columnLayout('vfxcamdbUIMCMini',q=1,h=1)
    cmds.window('vfxcamdbUI',e=1,h=colH+100)

def digReplace(stringCode):
    test=['\xc2','\xc3','\x97','\x93','\xa0','\xe2','\x80','\x99Cb','\xe2','\x80','\x99Cr','\xe2','\x80','\x99']
    for t in test:
        stringCode=stringCode.replace(t,"")
    return stringCode
    
def createCam(optMenu):
    global vfxcamdbUIStuff
    dicKeys= vfxcamdbUIStuff.keys()
    sensorScroll=""
    resolutionScroll=""
    results=""
    cameraName=cmds.textFieldGrp(vfxcamdbUIStuff["camName"],q=1,tx=True)
    for dicKey in dicKeys:
        if dicKey=='sensorDimensionsScroll':
            sensorScroll=vfxcamdbUIStuff['sensorDimensionsScroll']
        elif dicKey=='sensorAreaScroll':
            sensorScroll=vfxcamdbUIStuff['sensorAreaScroll']
        if dicKey=='imageResolutionScroll':
            resolutionScroll=vfxcamdbUIStuff['imageResolutionScroll']
    if cmds.objExists(cameraName):
        results=cmds.confirmDialog(message="\n'" + cameraName + "' exists in this scene.  Do you want to:\n",button=["Create New","Edit Existing","Cancel"])
        if results=="Cancel":
            return
    sensorX,sensorY=tester(cmds.textScrollList(sensorScroll,q=1,si=1)[0])
    sensorX=sensorX*0.0393701
    sensorY=sensorY*0.0393701
    if results=="Edit Existing":
        cmds.setAttr(cameraName+".horizontalFilmAperture",l=False)
        cmds.setAttr(cameraName+".verticalFilmAperture",l=False)
        cmds.setAttr(cameraName+".horizontalFilmAperture",sensorX)
        cmds.setAttr(cameraName+".verticalFilmAperture",sensorY)
    elif results=="Create New":
# delete Camera
        cmds.delete(cameraName)
    if results!="Edit Existing":
        echoObjs=cmds.camera(name=cameraName,verticalFilmAperture=sensorY,horizontalFilmAperture=sensorX,centerOfInterest=5, focalLength=35,lensSqueezeRatio=1,cameraScale=1,horizontalFilmOffset=0,verticalFilmOffset=0,filmFit="Overscan",overscan=1,motionBlur=0,shutterAngle=144,nearClipPlane=1,farClipPlane=500000,orthographic=0,orthographicWidth=30,panZoomEnabled=0,horizontalPan=0,verticalPan=0,zoom=1)
        cmds.rename(echoObjs[0],cameraName)
    if cmds.checkBox(vfxcamdbUIStuff["check"],q=1,v=True):
        resolutionTxt=cmds.textScrollList(resolutionScroll,q=1,si=True)[0]
        whitelist = set('01234567890 ')
        answer = ''.join(filter(whitelist.__contains__, resolutionTxt))
        splitAnswer=answer.split(" ")
        x=0
        wd=1
        ht=1
        for res in splitAnswer:
            if res and x==0:
                wd=int(res)
                cmds.setAttr("defaultResolution.width",int(res))
                x=1
            elif res and x==1:
                ht=int(res)
                cmds.setAttr("defaultResolution.height",int(res))
                x=2
        if x!=0:
            cmds.setAttr("defaultResolution.deviceAspectRatio",float(wd)/float(ht))
            cmds.evalDeferred('cmds.setAttr("defaultResolution.pixelAspect",1)')

def getRes():
    global vfxcamdbUIStuff
    rawRes=vfxcamdbUIStuff['']

def tester(STRING1):
    splitString=STRING1.split("mm")
    split2=splitString[0].split(" ")
    first=""
    second=""
    counter=len(split2)
    while counter>0:
        if split2[counter-1]:
            first=split2[counter-1]
            break
        counter=counter-1
#        
    split3=splitString[1].split(" ")
    counter2=len(split3)
    while counter2>0:
        if split3[counter2-1]:
            second=split3[counter2-1]
            second=second.replace("x","")
            second=second.replace("X","")
            break
        counter2=counter2-1
    return float(first),float(second)

