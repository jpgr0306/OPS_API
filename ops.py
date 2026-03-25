import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

def autenticar_service_account():
    # Opção A: Carregar do arquivo local (para desenvolvimento)
    # Opção B: Carregar de uma string JSON (para produção/GitHub Actions)
    service_account_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    
    if service_account_info:
        # Converte a string da variável de ambiente de volta para dicionário
        info = json.loads(service_account_info)
        creds = service_account.Credentials.from_service_account_info(info)
    else:
        # Fallback para o arquivo local se a variável não existir
        creds = service_account.Credentials.from_service_account_file(
            'service_account.json', 
            scopes=['https://www.googleapis.com/auth/drive']
        )
    
    return build('drive', 'v3', credentials=creds)
