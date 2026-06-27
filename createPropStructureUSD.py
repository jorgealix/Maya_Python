import maya.cmds as cmds
def createPropStrucUSD():
    # Create an empty prop structure
    propStr = cmds.ls( 'geo' )
    if propStr:
        cmds.confirmDialog( title='Warning', message = "Prop structure already exist!", icon = "information", button=['OK'] )
    else:
        cmds.group(em=True, name='simproxy')
        cmds.group(em=True, name='proxy')
        cmds.group(em=True, name='render')
        cmds.group(em=True, name='mtl')
        cmds.group( em=True, name='rig' )
        cmds.group( em=True, name='fx' )
        cmds.group( 'proxy','render', 'simproxy',  name = 'geo' )
        cmds.group( 'geo', 'rig', 'fx','mtl', name ='asset_prop' )
        cmds.addAttr("asset_prop", ln = "notes", sn="nts", dt="string")
        cmds.setAttr("asset_prop.notes",
                     """
                    1- El asset debe estar en el 0,0.\n
                    2- Debe poseer todas las transformaciones freezeadas.\n
                    3- Si es un prop se haran grupos de movilidad.\n
                    4- Todas las piezas que puedan moverse iran en un grupo.\n
                    5- Dentro de los grupos el elemento debe tener colapsadas las geometrias por materiales y catclarck. Por ejemplo tenemos 4 piezas dos de ellas son plastico con catclarck 1 y las otras dos son madera con catclarck 1 y 2 respectivamente. Los dos plasticos los podremos colapsar, sin embargo las maderas no porque pasaran a tener el catclarck the la primera geometria que hayamos colapsado. Es importante que no se colapse nada que esta en grupos diferentes. Hay que tener cuidado al combinar geometrias con el opaque desactivado ya que al combinarlas Maya activara el opaque de nuevo. Haciendo asi que por ejemplo dos bombillas con el opaque desactivado al combinarse pierdan la transparencia y vuelvan a ser opacas de nuevo.\n
                    6- Los grupos tiene que tener el punto de pivote de acuerdo con el tipo de movilidad de elemento.\n""",
                     type = "string")
        cmds.confirmDialog( title='Confirm', backgroundColor = [1,1,1], messageAlign = 'left', message='''
                    1- El asset debe estar en el 0,0.\n
                    2- Debe poseer todas las transformaciones freezeadas.\n
                    3- Si es un prop se haran grupos de movilidad.\n
                    4- Todas las piezas que puedan moverse iran en un grupo.\n
                    5- Dentro de los grupos el elemento debe tener colapsadas las geometrias por materiales y catclarck. Por ejemplo tenemos 4 piezas dos de ellas son plastico con catclarck 1 y las otras dos son madera con catclarck 1 y 2 respectivamente. Los dos plasticos los podremos colapsar, sin embargo las maderas no porque pasaran a tener el catclarck the la primera geometria que hayamos colapsado. Es importante que no se colapse nada que esta en grupos diferentes. Hay que tener cuidado al combinar geometrias con el opaque desactivado ya que al combinarlas Maya activara el opaque de nuevo. Haciendo asi que por ejemplo dos bombillas con el opaque desactivado al combinarse pierdan la transparencia y vuelvan a ser opacas de nuevo.\n
                    6- Los grupos tiene que tener el punto de pivote de acuerdo con el tipo de movilidad de elemento.\n
                    ''' )

