import sys
import importlib
sys.path.append(r"S:\cena\_logs_texturas")
import TextureRelocationPaths
importlib.reload(TextureRelocationPaths)
TextureRelocationPaths.fix_textures_paths()