import os

# DONT CHANGE!
# IF ROOT_PATH OF APACHE CONF IS DIFERENT THEN CHANGE LINE BELOW
PUBLIC_PATH = '/var/www/html'


LOG_FILE = os.environ.get('LOG_FILE') or '/home/nelson/Documentos/pathologyIndexer/src/docs/logs.log'
ROOT_PATH = '/home/nelson/Documentos/'
INDEX_PATH = '/home/nelson/Documentos/pathologyIndexer/index'

# DATA_PATH ES UN SUB DIRECTORIO DE PUBLIC_PATH
# EJEMPLO: 	public_path="/var/www/html"
#			data_path="pathologyIndexer_Data/"
# ->->->->	ruta completa=/var/www/html/pathologyIndexer_Data/
DATA_PATH = 'pathologyIndexer_Data'