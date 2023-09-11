import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set the folder ID of the Google Drive folder containing the Excel files
FOLDER_ID = 'https://drive.google.com/drive/folders/1PiCC3UiU3pD9mBoSM0Y_na9mnhwWYB6D'
SCOPES = ['https://www.googleapis.com/auth/drive']
# Load the client ID and client secret from the credentials JSON file
flow = InstalledAppFlow.from_client_secrets_file(
    '/home/dethoalihamza/python_scripts/client_service.json', scopes=SCOPES
)

# Start the OAuth2 flow
credentials = flow.run_local_server(port=8080)

# Initialize the Google Drive API with the loaded credentials
service = build('drive', 'v3', credentials=credentials)

# Retrieve a list of files in the folder
results = service.files().list(q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'",
                               fields='files(id, name)').execute()
files = results.get('files', [])

# Download each Excel file
for file in files:
    request = service.files().get_media(fileId=file['id'])
    fh = open(file['name'], 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")

print("Download completed!")
