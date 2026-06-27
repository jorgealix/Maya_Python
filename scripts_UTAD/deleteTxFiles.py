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

    # Preguntar tipo de borrado
    tipo_borrado = cmds.confirmDialog(
        title="Tipo de borrado",
        message=(
            "¿Qué archivos deseas borrar?\n\n"
            "• 'Todos' → Elimina TODOS los .tx\n"
            "• 'Solo ACEScg' → Solo los .tx que contengan 'ACEScg'"
        ),
        button=["Todos", "Solo ACEScg", "Cancelar"],
        defaultButton="Cancelar",
        cancelButton="Cancelar",
        dismissString="Cancelar"
    )

    if tipo_borrado == "Cancelar":
        cmds.warning("Borrado cancelado por el usuario.")
        return

    # Confirmación final
    mensaje_confirmacion = (
        f"Se eliminarán archivos .tx de forma RECURSIVA en:\n\n{folder}\n\n"
    )

    if tipo_borrado == "Solo ACEScg":
        mensaje_confirmacion += "Solo los que contengan 'ACEScg' en el nombre.\n\n"

    mensaje_confirmacion += "¿Deseas continuar?"

    result = cmds.confirmDialog(
        title="Confirmar borrado",
        message=mensaje_confirmacion,
        button=["Sí", "Cancelar"],
        defaultButton="Cancelar",
        cancelButton="Cancelar",
        dismissString="Cancelar"
    )

    if result != "Sí":
        cmds.warning("Borrado cancelado por el usuario.")
        return

    # Construcción del comando PowerShell
    if tipo_borrado == "Todos":
        ps_command = (
            f'Get-ChildItem -Path "{folder}" -Recurse -Include *.tx | '
            f'Remove-Item -Force'
        )
    else:  # Solo ACEScg
        ps_command = (
            f'Get-ChildItem -Path "{folder}" -Recurse -Include *.tx | '
            f'Where-Object {{$_.Name -like "*ACEScg*"}} | '
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