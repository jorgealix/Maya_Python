import sys
import importlib
sys.path.append(r"S:\scripts")
import deleteTxFiles
importlib.reload(deleteTxFiles)
deleteTxFiles.borrar_tx_recursivo()