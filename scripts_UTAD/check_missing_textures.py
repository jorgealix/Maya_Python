"""
check_missing_textures.py
-------------------------
Revisa todas las texturas referenciadas en la escena de Maya,
detecta las que no existen en disco y exporta un JSON con el reporte.

Uso:
    Ejecutar desde el Script Editor de Maya (Python) o desde mayapy.
    El JSON se guarda junto a la escena actual, o en el directorio
    temporal del sistema si la escena no ha sido guardada.
"""

import os
import json
import maya.cmds as cmds


# ─────────────────────────────────────────────
# Tipos de nodo que contienen rutas de textura
# ─────────────────────────────────────────────
TEXTURE_NODE_ATTRS = {
    "file":             ["fileTextureName"],
    "aiImage":          ["filename"],
    "aiStandIn":        ["dso"],          # .ass files – opcional, quitar si no interesa
    "RedshiftNormalMap":["tex0"],
    "RedshiftDomeLight":["tex0"],
    "pxrTexture":       ["filename"],
}


def get_scene_dir():
    """Devuelve el directorio de la escena o el temp del sistema."""
    scene = cmds.file(q=True, sceneName=True)
    if scene:
        return os.path.dirname(scene)
    import tempfile
    return tempfile.gettempdir()


def resolve_path(raw_path):
    """
    Resuelve variables de proyecto de Maya (<UDIM>, tokens, etc.)
    y expande variables de entorno.
    """
    if not raw_path:
        return ""
    # Expande variables de entorno tipo $VAR o %VAR%
    resolved = os.path.expandvars(raw_path)
    # Expande ~ si existe
    resolved = os.path.expanduser(resolved)
    return resolved


def collect_texture_paths():
    """
    Recorre todos los nodos de textura conocidos y recopila
    {nodo, atributo, ruta_raw, ruta_resuelta}.
    """
    entries = []

    for node_type, attrs in TEXTURE_NODE_ATTRS.items():
        nodes = cmds.ls(type=node_type) or []
        for node in nodes:
            for attr in attrs:
                plug = f"{node}.{attr}"
                if not cmds.attributeQuery(attr, node=node, exists=True):
                    continue
                raw = cmds.getAttr(plug) or ""
                if not raw.strip():
                    continue
                entries.append({
                    "node":      node,
                    "node_type": node_type,
                    "attribute": attr,
                    "path_raw":  raw,
                    "path_resolved": resolve_path(raw),
                })

    return entries


def classify_entries(entries):
    """Separa entradas en existentes y faltantes."""
    found   = []
    missing = []

    for e in entries:
        resolved = e["path_resolved"]

        # Texturas UDIM: sustituye <UDIM> / %04d / #### por un glob
        check_path = resolved
        udim_entry = False
        for token in ("<UDIM>", "%04d", "####", "<udim>"):
            if token in resolved:
                udim_entry = True
                # Verifica si existe al menos un tile
                import glob
                pattern = resolved.replace(token, "*")
                matches = glob.glob(pattern)
                if matches:
                    e["udim_tiles_found"] = len(matches)
                    found.append(e)
                else:
                    e["udim_tiles_found"] = 0
                    missing.append(e)
                break

        if not udim_entry:
            if os.path.isfile(check_path):
                found.append(e)
            else:
                missing.append(e)

    return found, missing


def build_report(found, missing):
    """Construye el diccionario del reporte final."""
    scene_path = cmds.file(q=True, sceneName=True) or "unsaved_scene"

    report = {
        "scene":          scene_path,
        "total_textures": len(found) + len(missing),
        "found_count":    len(found),
        "missing_count":  len(missing),
        "missing": [
            {
                "node":          e["node"],
                "node_type":     e["node_type"],
                "attribute":     e["attribute"],
                "path_raw":      e["path_raw"],
                "path_resolved": e["path_resolved"],
            }
            for e in missing
        ],
        "found": [
            {
                "node":          e["node"],
                "node_type":     e["node_type"],
                "attribute":     e["attribute"],
                "path_raw":      e["path_raw"],
                "path_resolved": e["path_resolved"],
            }
            for e in found
        ],
    }
    return report


def save_report(report, output_dir):
    """Guarda el JSON en disco y devuelve la ruta."""
    filename = "missing_textures_report.json"
    out_path = os.path.join(output_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    return out_path


def print_summary(report):
    """Imprime un resumen legible en el Output Window de Maya."""
    sep = "─" * 60
    print(sep)
    print(f"  CHECK MISSING TEXTURES")
    print(f"  Escena : {report['scene']}")
    print(f"  Total  : {report['total_textures']}  |  "
          f"OK: {report['found_count']}  |  "
          f"MISSING: {report['missing_count']}")
    print(sep)

    if report["missing_count"] == 0:
        print("  ✓ Todas las texturas están presentes.")
    else:
        print("  TEXTURAS FALTANTES:")
        for i, e in enumerate(report["missing"], 1):
            print(f"  [{i:>3}] {e['node']}  ({e['node_type']})")
            print(f"        attr : {e['attribute']}")
            print(f"        ruta : {e['path_resolved']}")
    print(sep)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def run():
    entries        = collect_texture_paths()
    found, missing = classify_entries(entries)
    report         = build_report(found, missing)

    output_dir = get_scene_dir()
    json_path  = save_report(report, output_dir)

    print_summary(report)
    print(f"\n  JSON guardado en:\n  {json_path}\n")

    return report  # útil si se llama desde otro script


if __name__ == "__main__":
    run()
