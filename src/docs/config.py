import os

# DONT CHANGE!
# IF ROOT_PATH OF APACHE CONF IS DIFERENT THEN CHANGE LINE BELOW
PUBLIC_PATH = '/app/pathologyIndexer/src/static'


LOG_FILE = os.environ.get('LOG_FILE')
ROOT_PATH = '/home/nelson/Escritorio/docker/'
INDEX_PATH = '/index'

# DATA_PATH ES UN SUB DIRECTORIO DE PUBLIC_PATH
# EJEMPLO: 	public_path="/var/www/html"
#			data_path="pathologyIndexer_Data/"
# ->->->->	ruta completa=/var/www/html/pathologyIndexer_Data/
DATA_PATH = 'docs'
