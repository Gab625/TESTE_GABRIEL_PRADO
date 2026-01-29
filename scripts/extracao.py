import requests
import os
from bs4 import BeautifulSoup
import zipfile
import io

URL_BASE = "https://dadosabertos.ans.gov.br/FTP/PDA/"
PASTA_DESTINO = "./dados"

def baixar_da_url(caminho_especifico):
    URL_ALVO = requests.compat.urljoin(URL_BASE, caminho_especifico)
    os.makedirs(PASTA_DESTINO, exist_ok=True)

    response = requests.get(URL_ALVO)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    arquivos = [link.get('href') for link in soup.find_all('a') 
                if link.get('href').endswith(('.zip', '.csv'))]
    
    for nome_arq in arquivos:
        URL_DOWNLOAD = requests.compat.urljoin(URL_ALVO, nome_arq)
        
        r = requests.get(URL_DOWNLOAD)
        
        if nome_arq.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                z.extractall(PASTA_DESTINO)
        else:
            caminho_salvamento = os.path.join(PASTA_DESTINO, nome_arq)
            with open(caminho_salvamento, "wb") as f:
                f.write(r.content)

def extrair_dados():
    baixar_da_url("demonstracoes_contabeis/2025/")

    baixar_da_url("operadoras_de_plano_de_saude_ativas/")