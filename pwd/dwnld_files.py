import os
from drive import Create_Service
import io
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = '/home/dethoalihamza/python_scripts/client_service.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['18uo-T0Z8WVkRkOMLSxwnTRiXCMfBZliy']
file_names = ['markanl_sps.xlsx']
for file_id, file_name in zip(file_ids, file_names):
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download progress {0}'.format(status.progress() * 100))
    
    fh.seek(0)
    with open(file_name, 'wb') as f:
        f.write(fh.read())
        f.close()
