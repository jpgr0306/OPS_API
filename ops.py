import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

def autenticar_service_account():
    if service_account_info:
        info = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
        creds = service_account.Credentials.from_service_account_info(info)
    else:
        creds = service_account.Credentials.from_service_account_file(
            'service_account.json', 
            scopes=['https://www.googleapis.com/auth/drive']
        )
    
    return build('drive', 'v3', credentials=creds)
