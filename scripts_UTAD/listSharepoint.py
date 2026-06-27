from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

# 🔐 Credenciales (rellenar)
client_id = "jorge.medina@ext.u-tad.com"
client_secret = "Ut@t2026Render"

# 🌐 URL de tu sitio
site_url = "https://liveutad.sharepoint.com/sites/ANIG_2026_PRY_ALTR/"

# 📁 Ruta de la carpeta (IMPORTANTE: server-relative URL)
folder_url = "/sites/ANIG_2026_PRY_ALTR/altr/assets"

# 🔌 Conexión
ctx = ClientContext(site_url).with_credentials(
    ClientCredential(client_id, client_secret)
)

# 📂 Obtener carpeta
folder = ctx.web.get_folder_by_server_relative_url(folder_url)

# 📄 Archivos
files = folder.files
ctx.load(files)
ctx.execute_query()

print("📄 Archivos:")
for file in files:
    print("-", file.properties["Name"])

# 📁 Subcarpetas (opcional)
folders = folder.folders
ctx.load(folders)
ctx.execute_query()

print("\n📁 Carpetas:")
for f in folders:
    print("-", f.properties["Name"])