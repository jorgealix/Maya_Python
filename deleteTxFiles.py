import subprocess
import maya.cmds as cmds

def borrar_tx_recursivo():
    # Selector de carpeta
    folder = cmds.fileDialog2(
        dialogStyle=2,
        fileMode=3,
        caption="Selecciona la carpeta donde borrar archivos .tx"
    )

    if not folder:
        cmds.warning("Operación cancelada.")
        return

    folder = folder[0]

    # Confirmación
    result = cmds.confirmDialog(
        title="Confirmar borrado",
        message=(
            "Se eliminarán TODOS los archivos .tx\n"
            "de forma RECURSIVA en:\n\n"
            f"{folder}\n\n"
            "¿Deseas continuar?"
        ),
        button=["Sí", "Cancelar"],
        defaultButton="Cancelar",
        cancelButton="Cancelar",
        dismissString="Cancelar"
    )

    if result != "Sí":
        cmds.warning("Borrado cancelado por el usuario.")
        return

    # Comando PowerShell
    ps_command = (
        f'Get-ChildItem -Path "{folder}" -Recurse -Include *.tx | '
        f'Remove-Item -Force'
    )

    full_command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command", ps_command
    ]

    try:
        subprocess.run(full_command, check=True)
        cmds.confirmDialog(
            title="Completado",
            message=(
                "Borrado finalizado correctamente.\n\n"
                f"Carpeta:\n{folder}"
            ),
            button=["OK"]
        )
    except subprocess.CalledProcessError as e:
        cmds.confirmDialog(
            title="Error",
            message=f"Error ejecutando PowerShell:\n{e}",
            button=["OK"],
            icon="critical"
        )

