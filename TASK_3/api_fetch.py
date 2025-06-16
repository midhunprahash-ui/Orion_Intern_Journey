import io
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

def read_excel_from_drive(file_id):
    # Create a request to get the file content
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    fh.seek(0)  # Move to the beginning of the BytesIO buffer

    # Read Excel file from BytesIO buffer using pandas
    df = pd.read_excel(fh)
    return df

# Example usage: replace with your actual file ID
file_id = '105236659273419217183'
df = read_excel_from_drive(file_id)

print(df.head())
