import os
import re
import json

UDIM_REGEX = re.compile(r"(.*?)(\d{4})(\.\w+)$")


def ask_for_directory():
    while True:
        path = input("📂 Directorio a analizar:\n> ").strip('"')
        if os.path.isdir(path):
            return path
        print("❌ Ruta no válida\n")


def find_udim_sets(root):

    udim_sets = {}

    for dirpath, _, files in os.walk(root):
        for f in files:

            match = UDIM_REGEX.match(f)

            if not match:
                continue

            base, udim, ext = match.groups()

            key = os.path.join(dirpath, base + ext)

            udim_sets.setdefault(key, []).append(int(udim))

    return udim_sets


def find_missing_udims(udim_sets):

    report = {}

    for key, udims in udim_sets.items():

        udims = sorted(set(udims))

        expected = set(range(min(udims), max(udims) + 1))
        missing = sorted(expected - set(udims))

        if missing:
            report[key] = {
                "existing": udims,
                "missing": missing
            }

    return report


def main():

    root = ask_for_directory()

    print("\n🔍 Analizando UDIMs...\n")

    udim_sets = find_udim_sets(root)
    report = find_missing_udims(udim_sets)

    reports_dir = os.path.join(root, "_tx_reports")
    os.makedirs(reports_dir, exist_ok=True)

    json_path = os.path.join(reports_dir, "missing_udims.json")

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(report, f, indent=4)

    print("✅ Análisis completado")
    print(f"UDIM sets analizados: {len(udim_sets)}")
    print(f"Sets con huecos: {len(report)}")
    print(f"Reporte:\n{json_path}")


if __name__ == "__main__":
    main()