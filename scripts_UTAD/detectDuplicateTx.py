import os
import json
import argparse

KEYWORDS = ["acescg"]


def normalize_name(filename):
    name = os.path.splitext(filename)[0].lower()

    for k in KEYWORDS:
        name = name.replace(k, "")

    return name.strip("_- ")


def find_tx_files(root):
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith(".tx"):
                yield os.path.join(dirpath, f)


def ask_for_directory():
    while True:
        path = input("📂 Introduce el directorio a analizar:\n> ").strip('"')

        if os.path.isdir(path):
            return path
        else:
            print("❌ Ruta no válida, inténtalo de nuevo.\n")


def find_duplicate_tx(root_dir):

    groups = {}
    duplicates = {}

    reports_dir = os.path.join(root_dir, "_tx_reports")
    os.makedirs(reports_dir, exist_ok=True)

    print("\n🔍 Analizando .tx...\n")

    total = 0

    for tx in find_tx_files(root_dir):

        total += 1

        if total % 100 == 0:
            print(f"Procesados: {total}")

        base = normalize_name(os.path.basename(tx))
        groups.setdefault(base, []).append(tx)

    for base, files in groups.items():
        if len(files) > 1:
            duplicates[base] = files

    json_path = os.path.join(reports_dir, "duplicate_tx_variants.json")

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(duplicates, f, indent=4)

    print("\n✅ Análisis completado")
    print(f"Total .tx encontrados: {total}")
    print(f"Grupos duplicados: {len(duplicates)}")
    print(f"Reporte guardado en:\n{json_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Detectar duplicados de .tx")
    parser.add_argument("path", nargs="?", help="Directorio raíz")

    args = parser.parse_args()

    if args.path:
        root = args.path
    else:
        root = ask_for_directory()

    find_duplicate_tx(root)