import sys
import importlib
sys.path.append(r"S:\scripts")
import ConvertTxRecursively
importlib.reload(ConvertTxRecursively)
ConvertTxRecursively.convert_to_tx(r"S:/cena/assets")