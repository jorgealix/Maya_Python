"""
╔══════════════════════════════════════════════════════════════╗
║              LOD MANAGER  —  Maya 2026                       ║
║  Genera y gestiona Level of Detail groups automáticamente    ║
║  Switching via distanceBetween + condition node network      ║
╠══════════════════════════════════════════════════════════════╣
║  Requisitos: Maya 2026  ·  Python 3.11  ·  maya.cmds         ║
╚══════════════════════════════════════════════════════════════╝

USO RÁPIDO:
    import lod_manager
    lod_manager.build_ui()

USO DESDE SCRIPT:
    import lod_manager
    lod_manager.generate_lods("miMesh_geo")
    lod_manager.update_thresholds("miMesh_LOD_GRP", [0, 20, 60, 150, 400])
"""

from __future__ import annotations
import json
import maya.cmds as cmds

# ─────────────────────────────────────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────────────────────────────────────

def get_poly_count(mesh_transform: str) -> int:
    shapes = cmds.listRelatives(mesh_transform, shapes=True, type="mesh", fullPath=True)
    if not shapes:
        return 0
    try:
        return cmds.polyEvaluate(shapes[0], face=True)
    except Exception:
        return 0


def _clean_name(source_mesh: str) -> str:
    """Elimina sufijos comunes para obtener el nombre base del asset."""
    name = source_mesh
    for sfx in ("_LOD0", "_high", "_hi", "_HI", "_HIGH", "_geo", "_GEO", "_mesh"):
        name = name.replace(sfx, "")
    return name


def _get_active_camera() -> str:
    """
    Devuelve el transform de la cámara del panel activo.
    Maya 2026: getPanel(withFocus) puede devolver paneles no-modelo
    (Script Editor, Node Editor…), por lo que verificamos el tipo antes de usarlo.
    Fallback: persp.
    """
    try:
        panel = cmds.getPanel(withFocus=True)
        # comprobar que es un modelPanel antes de pedir la cámara
        if panel and cmds.getPanel(typeOf=panel) == "modelPanel":
            cam = cmds.modelEditor(panel, q=True, camera=True)
            if cam and cmds.objExists(cam):
                # getPanel puede devolver el shape de la cámara; subimos al transform
                if cmds.nodeType(cam) == "camera":
                    parents = cmds.listRelatives(cam, parent=True, fullPath=True)
                    if parents:
                        cam = parents[0]
                return cam
    except Exception:
        pass

    # segundo intento: buscar cualquier panel de modelo visible
    try:
        for panel in cmds.getPanel(type="modelPanel") or []:
            cam = cmds.modelEditor(panel, q=True, camera=True)
            if cam and cmds.objExists(cam):
                if cmds.nodeType(cam) == "camera":
                    parents = cmds.listRelatives(cam, parent=True, fullPath=True)
                    if parents:
                        cam = parents[0]
                return cam
    except Exception:
        pass

    return "persp"


# ─────────────────────────────────────────────────────────────────────────────
#  GENERACIÓN DE LODs
# ─────────────────────────────────────────────────────────────────────────────

def generate_lods(
    source_mesh: str | None = None,
    num_lods: int = 5,
    keep_percentages: list[int] | None = None,
    distance_thresholds: list[float] | None = None,
) -> str | None:
    """
    Genera meshes LOD reducidos y conecta la visibilidad de cada uno a la
    distancia de la cámara activa usando un node network nativo de Maya.

    Parámetros
    ----------
    source_mesh        : transform del mesh de alta resolución.
                         None → usa la selección activa.
    num_lods           : número total de niveles (LOD0 = original incluido).
    keep_percentages   : % de caras a CONSERVAR en LOD1..N.  Ej: [75, 50, 25, 10]
    distance_thresholds: distancia de activación de cada nivel.  Ej: [0, 15, 40, 100, 250]

    Devuelve el nombre del LOD_GRP creado, o None si hubo un error.
    """

    # ── mesh origen ───────────────────────────────────────────────────────────
    if source_mesh is None:
        sel = cmds.ls(selection=True, transforms=True)
        if not sel:
            cmds.error("[LOD Manager] Selecciona un mesh primero.")
            return None
        source_mesh = sel[0]

    if not cmds.objExists(source_mesh):
        cmds.error(f"[LOD Manager] No existe: {source_mesh}")
        return None

    if not cmds.listRelatives(source_mesh, shapes=True, type="mesh"):
        cmds.error(f"[LOD Manager] '{source_mesh}' no tiene mesh shape.")
        return None

    # ── valores por defecto ───────────────────────────────────────────────────
    # FIX: usar 'not' en lugar de 'is None' para capturar también listas vacías []
    if not keep_percentages:
        keep_percentages = [max(int(100 * (0.55 ** i)), 3) for i in range(1, num_lods)]
    if not distance_thresholds:
        distance_thresholds = [0] + [int(15 * (3.0 ** i)) for i in range(num_lods - 1)]

    base       = _clean_name(source_mesh)
    orig_faces = get_poly_count(source_mesh)

    print(f"\n[LOD Manager] ▶ Generando LODs para '{source_mesh}' ({orig_faces} caras)")
    print(f"[LOD Manager]   Niveles   : {num_lods}")
    print(f"[LOD Manager]   Keep %    : {keep_percentages}")
    print(f"[LOD Manager]   Distancias: {distance_thresholds}\n")

    lod_meshes: list[str] = []

    # ── LOD0 = duplicado del original ─────────────────────────────────────────
    lod0 = cmds.duplicate(source_mesh, name=f"{base}_LOD0", returnRootsOnly=True)[0]
    lod_meshes.append(lod0)
    print(f"  LOD0 : {lod0:48s}  {orig_faces:>7} caras  (original)")

    # ── LOD1..N con polyReduce ────────────────────────────────────────────────
    # Maya 2026: usar version=1 (nuevo algoritmo Softimage-derived) +
    #            cachingReduce=True (recomendado con version=1)
    for i, keep_pct in enumerate(keep_percentages[: num_lods - 1]):
        lod_mesh = cmds.duplicate(
            source_mesh, name=f"{base}_LOD{i + 1}", returnRootsOnly=True
        )[0]

        cmds.polyReduce(
            lod_mesh,
            version=1,                          # ← Maya 2026: nuevo algoritmo
            percentage=100.0 - float(keep_pct), # % a ELIMINAR (no a conservar)
            keepQuadsWeight=0.5,
            sharpness=0.0,
            keepBorder=True,
            keepMapBorder=True,
            keepColorBorder=True,
            keepCreaseEdge=True,
            keepHardEdge=False,
            keepOriginalVertices=False,
            cachingReduce=True,                 # ← recomendado con version=1
            constructionHistory=False,
        )

        actual = get_poly_count(lod_mesh)
        print(f"  LOD{i+1}: {lod_mesh:48s}  {actual:>7} caras  ({keep_pct}% conservado)")
        lod_meshes.append(lod_mesh)

    # ── LOD Group ─────────────────────────────────────────────────────────────
    ws_pos = cmds.xform(source_mesh, q=True, worldSpace=True, translation=True)
    ws_rot = cmds.xform(source_mesh, q=True, worldSpace=True, rotation=True)

    lod_grp = create_lod_group(lod_meshes, distance_thresholds, base)
    cmds.xform(lod_grp, worldSpace=True, translation=ws_pos, rotation=ws_rot)
    cmds.hide(source_mesh)

    print(f"\n[LOD Manager] ✓ LOD Group: {lod_grp}")
    cmds.select(lod_grp)
    return lod_grp


# ─────────────────────────────────────────────────────────────────────────────
#  NODE NETWORK DE SWITCHING
# ─────────────────────────────────────────────────────────────────────────────

def create_lod_group(
    lod_meshes: list[str],
    distance_thresholds: list[float],
    base_name: str,
) -> str:
    """
    Agrupa los meshes LOD y conecta la visibilidad de cada uno a la distancia
    de cámara mediante nodos Maya nativos:

        cam.worldMatrix  ──→ decomposeMatrix ──┐
                                               ├──→ distanceBetween.distance
        grp.worldMatrix  ──→ decomposeMatrix ──┘
                                  │
              ┌───────────────────┼────────────────────┐
              ▼                   ▼                    ▼
         condition₀          cond_lo₁ × cond_hi₁   conditionₙ
        (dist < thr₁)            AND lógico        (dist >= thrₙ)
              │                   │                    │
         LOD0.vis             LOD1.vis             LODn.vis

    Los thresholds se guardan en un atributo string del grupo para poder
    recuperarlos y modificarlos después con update_thresholds().
    """
    n = len(lod_meshes)

    lod_grp = cmds.group(lod_meshes, name=f"{base_name}_LOD_GRP")

    # guardar thresholds y conteo como atributos del grupo
    cmds.addAttr(lod_grp, longName="lodThresholds", dataType="string")
    cmds.setAttr(f"{lod_grp}.lodThresholds", json.dumps(distance_thresholds), type="string")
    cmds.addAttr(lod_grp, longName="lodCount", attributeType="long", defaultValue=n)

    cam = _get_active_camera()

    # nodo distanceBetween
    dist_node = cmds.createNode("distanceBetween", name=f"{base_name}_LOD_dist")

    grp_dec = cmds.createNode("decomposeMatrix", name=f"{base_name}_LOD_decGRP")
    cmds.connectAttr(f"{lod_grp}.worldMatrix[0]", f"{grp_dec}.inputMatrix")
    cmds.connectAttr(f"{grp_dec}.outputTranslate", f"{dist_node}.point1")

    cam_dec = cmds.createNode("decomposeMatrix", name=f"{base_name}_LOD_decCAM")
    cmds.connectAttr(f"{cam}.worldMatrix[0]",  f"{cam_dec}.inputMatrix")
    cmds.connectAttr(f"{cam_dec}.outputTranslate", f"{dist_node}.point2")

    # leer hijos en el orden en que quedaron tras el group()
    children = cmds.listRelatives(lod_grp, children=True, type="transform") or []

    for i in range(n):
        mesh_node = children[i] if i < len(children) else lod_meshes[i]
        thr_lo    = float(distance_thresholds[i])     if i     < len(distance_thresholds) else 0.0
        thr_hi    = float(distance_thresholds[i + 1]) if i + 1 < len(distance_thresholds) else None

        if n == 1:
            # un solo nivel → siempre visible
            cmds.setAttr(f"{mesh_node}.visibility", 1)
            continue

        if i == 0:
            # LOD0: visible si dist < thr[1]
            cond = cmds.createNode("condition", name=f"{base_name}_LOD{i}_cond")
            cmds.connectAttr(f"{dist_node}.distance", f"{cond}.firstTerm")
            cmds.setAttr(f"{cond}.secondTerm",     thr_hi if thr_hi is not None else 999_999.0)
            cmds.setAttr(f"{cond}.operation",      4)   # less than
            cmds.setAttr(f"{cond}.colorIfTrueR",   1.0)
            cmds.setAttr(f"{cond}.colorIfFalseR",  0.0)
            cmds.connectAttr(f"{cond}.outColorR",  f"{mesh_node}.visibility")

        elif thr_hi is None:
            # último LOD: visible si dist >= thr[n]
            cond = cmds.createNode("condition", name=f"{base_name}_LOD{i}_cond")
            cmds.connectAttr(f"{dist_node}.distance", f"{cond}.firstTerm")
            cmds.setAttr(f"{cond}.secondTerm",     thr_lo)
            cmds.setAttr(f"{cond}.operation",      5)   # greater or equal
            cmds.setAttr(f"{cond}.colorIfTrueR",   1.0)
            cmds.setAttr(f"{cond}.colorIfFalseR",  0.0)
            cmds.connectAttr(f"{cond}.outColorR",  f"{mesh_node}.visibility")

        else:
            # nivel intermedio: thr[i] <= dist < thr[i+1]
            # AND lógico = cond_lo (dist >= thr_lo) × cond_hi (dist < thr_hi)
            cond_lo = cmds.createNode("condition", name=f"{base_name}_LOD{i}_condLO")
            cmds.connectAttr(f"{dist_node}.distance", f"{cond_lo}.firstTerm")
            cmds.setAttr(f"{cond_lo}.secondTerm",    thr_lo)
            cmds.setAttr(f"{cond_lo}.operation",     5)
            cmds.setAttr(f"{cond_lo}.colorIfTrueR",  1.0)
            cmds.setAttr(f"{cond_lo}.colorIfFalseR", 0.0)

            cond_hi = cmds.createNode("condition", name=f"{base_name}_LOD{i}_condHI")
            cmds.connectAttr(f"{dist_node}.distance", f"{cond_hi}.firstTerm")
            cmds.setAttr(f"{cond_hi}.secondTerm",    thr_hi)
            cmds.setAttr(f"{cond_hi}.operation",     4)
            cmds.setAttr(f"{cond_hi}.colorIfTrueR",  1.0)
            cmds.setAttr(f"{cond_hi}.colorIfFalseR", 0.0)

            mult = cmds.createNode("multiplyDivide", name=f"{base_name}_LOD{i}_AND")
            cmds.connectAttr(f"{cond_lo}.outColorR", f"{mult}.input1X")
            cmds.connectAttr(f"{cond_hi}.outColorR", f"{mult}.input2X")
            cmds.connectAttr(f"{mult}.outputX",      f"{mesh_node}.visibility")

    return lod_grp


# ─────────────────────────────────────────────────────────────────────────────
#  UPDATE / QUERY
# ─────────────────────────────────────────────────────────────────────────────

def update_thresholds(lod_group: str, new_thresholds: list[float]) -> bool:
    """Actualiza las distancias de switching en un LOD_GRP existente."""
    if not cmds.objExists(lod_group):
        cmds.warning(f"[LOD Manager] '{lod_group}' no existe.")
        return False

    if cmds.attributeQuery("lodThresholds", node=lod_group, exists=True):
        cmds.setAttr(f"{lod_group}.lodThresholds", json.dumps(new_thresholds), type="string")

    base = lod_group.replace("_LOD_GRP", "")
    n    = len(new_thresholds)

    for i in range(n):
        thr_lo = new_thresholds[i]
        thr_hi = new_thresholds[i + 1] if i + 1 < n else None

        if i == 0:
            cond = f"{base}_LOD0_cond"
            if cmds.objExists(cond):
                cmds.setAttr(f"{cond}.secondTerm",
                             float(new_thresholds[1]) if n > 1 else 999_999.0)
        elif thr_hi is None:
            cond = f"{base}_LOD{i}_cond"
            if cmds.objExists(cond):
                cmds.setAttr(f"{cond}.secondTerm", float(thr_lo))
        else:
            cond_lo = f"{base}_LOD{i}_condLO"
            cond_hi = f"{base}_LOD{i}_condHI"
            if cmds.objExists(cond_lo):
                cmds.setAttr(f"{cond_lo}.secondTerm", float(thr_lo))
            if cmds.objExists(cond_hi):
                cmds.setAttr(f"{cond_hi}.secondTerm", float(thr_hi))

    print(f"[LOD Manager] ✓ Thresholds actualizados: {new_thresholds}")
    return True


def get_lod_info(lod_group: str) -> dict | None:
    """Devuelve info del LOD_GRP: niveles, thresholds y conteo de caras."""
    if not cmds.objExists(lod_group):
        return None

    thresholds: list[float] = []
    if cmds.attributeQuery("lodThresholds", node=lod_group, exists=True):
        try:
            thresholds = json.loads(cmds.getAttr(f"{lod_group}.lodThresholds"))
        except Exception:
            pass

    children = cmds.listRelatives(lod_group, children=True, type="transform") or []
    levels = [
        {
            "name":      child,
            "threshold": thresholds[i] if i < len(thresholds) else 0.0,
            "faces":     get_poly_count(child),
        }
        for i, child in enumerate(children)
    ]
    return {"group": lod_group, "lod_count": len(children), "levels": levels}


# ─────────────────────────────────────────────────────────────────────────────
#  INTERFAZ DE USUARIO  (maya.cmds — compatible con todas las versiones)
# ─────────────────────────────────────────────────────────────────────────────

_WIN_ID = "lodManagerWin"
_UI: dict = {}


def _log(msg: str) -> None:
    print(f"[LOD Manager] {msg}")
    if "log" in _UI and cmds.scrollField(_UI["log"], exists=True):
        cur = cmds.scrollField(_UI["log"], q=True, text=True)
        cmds.scrollField(_UI["log"], e=True, text=f"{cur}\n{msg}")


def _pick_mesh(*_) -> None:
    sel = cmds.ls(selection=True, transforms=True)
    if sel:
        cmds.textField(_UI["source"], e=True, text=sel[0])
        _log(f"Seleccionado: {sel[0]}  ({get_poly_count(sel[0])} caras)")
    else:
        _log("⚠  Selecciona un mesh en la escena primero.")


def _pick_group(*_) -> None:
    sel = cmds.ls(selection=True, transforms=True)
    if sel:
        cmds.textField(_UI["upd_group"], e=True, text=sel[0])


def _rebuild_rows(*_) -> None:
    _build_rows(cmds.intSliderGrp(_UI["num_lods"], q=True, value=True))


def _build_rows(num_lods: int) -> None:
    layout = _UI["rows_layout"]
    for c in (cmds.layout(layout, q=True, childArray=True) or []):
        try:
            cmds.deleteUI(c)
        except Exception:
            pass
    _UI["rows"] = []

    default_keep       = [100, 75, 50, 25, 10, 5, 3, 2]
    default_thresholds = [0.0, 15.0, 40.0, 100.0, 250.0, 600.0, 1500.0, 4000.0]

    for i in range(num_lods):
        row = cmds.rowLayout(
            numberOfColumns=4,
            columnWidth4=[90, 90, 130, 80],
            parent=layout,
            columnAlign4=["center", "center", "center", "center"],
        )
        cmds.text(label=f"LOD{i}" + ("  (orig)" if i == 0 else ""), align="center")
        keep_ctrl = cmds.intField(
            value=default_keep[i] if i < len(default_keep) else 5,
            minValue=1, maxValue=99,
            enable=(i > 0),
        )
        if i == 0:
            cmds.intField(keep_ctrl, e=True, value=100)

        thr_ctrl  = cmds.floatField(
            value=default_thresholds[i] if i < len(default_thresholds) else float(i * 100),
            minValue=0.0, precision=1,
        )
        faces_lbl = cmds.text(label="—", align="center")
        cmds.setParent("..")

        _UI["rows"].append({"keep": keep_ctrl, "thr": thr_ctrl, "faces": faces_lbl})


def _run_generate(*_) -> None:
    source = cmds.textField(_UI["source"], q=True, text=True).strip()
    if not source or not cmds.objExists(source):
        _log("⚠  Especifica un mesh origen válido.")
        return

    num_lods   = cmds.intSliderGrp(_UI["num_lods"], q=True, value=True)
    rows       = _UI.get("rows", [])
    keep_pcts: list[int]   = []
    thresholds: list[float] = []

    for i, row in enumerate(rows):
        thresholds.append(cmds.floatField(row["thr"],  q=True, value=True))
        if i > 0:
            keep_pcts.append(cmds.intField(row["keep"], q=True, value=True))

    if not thresholds:
        _log("⚠  No hay filas. Ajusta 'Num niveles' para regenerarlas.")
        return

    _log(f"▶ Generando {num_lods} LODs para '{source}'  |  keep%: {keep_pcts}  |  dist: {thresholds}")

    try:
        result = generate_lods(
            source_mesh=source,
            num_lods=num_lods,
            keep_percentages=keep_pcts,
            distance_thresholds=thresholds,
        )
        if result:
            _log(f"✓  LOD Group creado: {result}")
            info = get_lod_info(result)
            if info:
                for i, lvl in enumerate(info["levels"]):
                    if i < len(rows):
                        cmds.text(rows[i]["faces"], e=True, label=str(lvl["faces"]))
        else:
            _log("✗  No se pudo crear el LOD Group.")
    except Exception as exc:
        _log(f"✗  Error: {exc}")
        import traceback
        traceback.print_exc()


def _run_update(*_) -> None:
    grp = cmds.textField(_UI["upd_group"], q=True, text=True).strip()
    if not grp or not cmds.objExists(grp):
        _log("⚠  Especifica un LOD_GRP válido.")
        return
    thresholds = [cmds.floatField(r["thr"], q=True, value=True) for r in _UI.get("rows", [])]
    if update_thresholds(grp, thresholds):
        _log(f"✓  Thresholds actualizados en {grp}")


def build_ui() -> str:
    """Construye y muestra la ventana del LOD Manager."""
    if cmds.window(_WIN_ID, exists=True):
        cmds.deleteUI(_WIN_ID)

    win = cmds.window(_WIN_ID, title="LOD Manager  ·  Maya 2026",
                      widthHeight=(440, 650), sizeable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=["both", 10])

    cmds.separator(height=10, style="none")
    cmds.text(label="LOD MANAGER", font="boldLabelFont", height=26, align="center")
    cmds.text(
        label="Maya 2026  ·  polyReduce v1  ·  distanceBetween + condition nodes",
        wordWrap=True, align="center", font="smallPlainLabelFont",
    )
    cmds.separator(height=8)

    # ── Mesh origen ───────────────────────────────────────────────────────────
    cmds.frameLayout(label=" Mesh origen (LOD0)", collapsable=False,
                     marginWidth=8, marginHeight=8)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[270, 130], adjustableColumn=1)
    _UI["source"] = cmds.textField(placeholderText="Nombre del mesh de alta resolución...")
    cmds.button(label="← Usar selección", command=_pick_mesh)
    cmds.setParent("..")
    cmds.setParent("..")

    # ── Niveles ───────────────────────────────────────────────────────────────
    cmds.frameLayout(label=" Niveles LOD", collapsable=False,
                     marginWidth=8, marginHeight=8)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    _UI["num_lods"] = cmds.intSliderGrp(
        field=True, label="Num niveles :",
        minValue=2, maxValue=8, value=5,
        columnWidth3=[110, 50, 200],
        changeCommand=_rebuild_rows,
    )
    cmds.separator(height=4)

    cmds.rowLayout(numberOfColumns=4, columnWidth4=[90, 90, 130, 80])
    for lbl in ("Nivel", "Mantener %", "Dist. inicio (u)", "Caras"):
        cmds.text(label=lbl, align="center", font="boldLabelFont")
    cmds.setParent("..")
    cmds.separator(height=3, style="in")

    _UI["rows_layout"] = cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    _UI["rows"] = []
    cmds.setParent("..")   # salir de rows_layout
    cmds.setParent("..")   # salir de columnLayout
    cmds.setParent("..")   # salir de frameLayout

    # ── Botón principal ───────────────────────────────────────────────────────
    cmds.separator(height=8)
    cmds.button(
        label="▶   Generar LODs",
        height=38,
        backgroundColor=[0.18, 0.55, 0.28],
        command=_run_generate,
    )

    # ── Actualizar grupo existente ────────────────────────────────────────────
    cmds.separator(height=6)
    cmds.frameLayout(label=" Actualizar thresholds de LOD_GRP existente",
                     collapsable=True, collapse=True, marginWidth=8, marginHeight=8)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=4)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[270, 130], adjustableColumn=1)
    _UI["upd_group"] = cmds.textField(placeholderText="Nombre del LOD_GRP existente...")
    cmds.button(label="← Usar selección", command=_pick_group)
    cmds.setParent("..")
    cmds.button(label="Actualizar thresholds  →",
                command=_run_update, backgroundColor=[0.25, 0.38, 0.55])
    cmds.setParent("..")
    cmds.setParent("..")

    # ── Log ───────────────────────────────────────────────────────────────────
    cmds.separator(height=6)
    cmds.text(label="Log:", align="left", font="smallBoldLabelFont")
    _UI["log"] = cmds.scrollField(
        height=110, editable=False, wordWrap=True,
        text="Listo. Selecciona un mesh y pulsa 'Generar LODs'.",
    )
    cmds.separator(height=10, style="none")

    cmds.showWindow(win)
    _build_rows(5)
    return win


# ── punto de entrada ──────────────────────────────────────────────────────────
build_ui()
