import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def getMObjectFromSelection():
m_selectionList = OpenMaya.MSelectionList()

OpenMaya.MGlobal.getActiveSelectionList(m_selectionList)

m_node = OpenMaya.MObject()


try:
    0

m_selectionList.getDependNode(0, m_node)

if (m_node.isNull()): return None

except:

return None

return m_node





def getAllExtraAttributes():



m_result = []

m_obj = getMObjectFromSelection()

m_workMFnDep = OpenMaya.MFnDependencyNode()

m_workMDagMod = OpenMaya.MDagModifier()

if (m_obj):

m_objFn = OpenMaya.MFnDependencyNode()

m_objFn.setObject(m_obj)  # get function set from MObject

m_objRef = m_workMFnDep.create(m_objFn.typeName())  # Create reference MObject of the given type

# -- get the list --

m_result = getAttrListDifference(m_obj, m_objRef)
26
# --
27
m_workMDagMod.deleteNode(m_objRef)  # set node to delete
28
m_workMDagMod.doIt()  # execute delete operation
29
return m_result
30

31


def getAttrListDifference(m_obj, m_objRef):
    32


m_objFn = OpenMaya.MFnDependencyNode()

m_objRefFn = OpenMaya.MFnDependencyNode()

m_objFn.setObject(m_obj)

m_objRefFn.setObject(m_objRef)

m_result = []

if (m_objFn.attributeCount() > m_objRefFn.attributeCount()):

for i in range(m_objRefFn.attributeCount(), m_objFn.attributeCount()):

m_atrr = m_objFn.attribute(i)

m_fnAttr = OpenMaya.MFnAttribute(m_atrr)

m_result.append(m_fnAttr.name())

return m_result
