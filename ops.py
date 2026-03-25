import os
import json
import requests
import base64
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

KEY = os.getenv('OPS_CONSUMER_KEY')
SECRET = os.getenv('OPS_CONSUMER_SECRET')
GOOGLE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

def autenticar_service_account():
    # CORREÇÃO: Alterado 'service_account_info' para 'GOOGLE' que é a variável definida no topo
    if GOOGLE:
        info = json.loads(GOOGLE)
        creds = service_account.Credentials.from_service_account_info(info)
    else:
        creds = service_account.Credentials.from_service_account_file(
            'service_account.json', 
            scopes=['https://www.googleapis.com/auth/drive']
        )
    
    return build('drive', 'v3', credentials=creds)

# 2. Obter Token (OAuth2)
token = None # Começa vazio

def get_token():
    # URL CORRETA para a versão 3.2 (conforme o padrão que você enviou)
    auth_url = "https://ops.epo.org/3.2/auth/accesstoken"
    
    auth_string = f"{KEY}:{SECRET}"
    auth_b64 = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = "grant_type=client_credentials"
    
    res = requests.post(auth_url, headers=headers, data=payload)
    
    if res.status_code != 200:
        # Mostra o erro real se falhar
        print(f"Erro {res.status_code}: {res.text}")
        exit(1)
        
    return res.json()['access_token']

def consultar(patente):
    global token
    if not token: token = get_token()
    
    # URL de serviços continua com /rest-services/
    url = f"https://ops.epo.org/rest-services/published-data/publication/epodoc/{patente}/biblio"
    
    res = requests.get(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    
    if res.status_code == 401:
        token = get_token()
        res = requests.get(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    
    return res.json()

# Exemplo de uso direto
if __name__ == "__main__":
    print(consultar("EP1676595"))

# Exemplo de uso direto
print(consultar("EP1676595"))
