import maya.cmds as cmds
import random

def random_color_overrides_on_transforms(avoid_repeats=True):
    """
    Aplica un color aleatorio distinto a cada transform seleccionado,
    usando drawing overrides en el nodo de transformación.

    avoid_repeats:
        True  → intenta que no se repitan colores
        False → permite colores repetidos
    """

    sel = cmds.ls(sl=True, long=True, type="transform")
    if not sel:
        cmds.warning("No hay transform nodes seleccionados.")
        return

    # Maya soporta índices 0–31 (algunos son grises)
    valid_colors = list(range(0, 32))

    used_colors = set()

    for transform in sel:

        # Elegir color aleatorio sin repetición
        if avoid_repeats:
            available = [c for c in valid_colors if c not in used_colors]
            if not available:  # si se acaban los colores
                used_colors.clear()
                available = valid_colors
            color = random.choice(available)
            used_colors.add(color)
        else:
            # Color aleatorio simple
            color = random.choice(valid_colors)

        # Activar override
        cmds.setAttr(transform + ".overrideEnabled", 1)
        cmds.setAttr(transform + ".overrideColor", color)

    print("Overrides aplicados a {} transforms con colores aleatorios.".format(len(sel)))

def clear_random_overrides_on_transforms():
    sel = cmds.ls(sl=True, long=True, type="transform")
    if not sel:
        cmds.warning("No hay transform nodes seleccionados.")
        return

    for transform in sel:
        cmds.setAttr(transform + ".overrideEnabled", 0)

    print("Overrides eliminados en {} transforms.".format(len(sel)))
