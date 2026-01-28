import requests
import os
from bs4 import BeautifulSoup
import zipfile
import io


url_base = "https://dadosabertos.ans.gov.br/FTP/PDA/"
target_path = "demonstracoes_contabeis/2025/"
url_result = requests.compat.urljoin(url_base, target_path)

destination_folder = "./dados_contabeis_2025"
os.makedirs(destination_folder, exist_ok=True)

print(f"Acessando: {url_result}")

try:
    response = requests.get(url_result)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    founded_zips = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.zip')]

    print(f"Arquivos encontrados: {founded_zips}")

    for zip_name in founded_zips:
        url_download = requests.compat.urljoin(url_result,zip_name)
        print(f"Baixando e extraindo {zip_name}.")

        r = requests.get(url_download)
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall(destination_folder)
    
    print(f"\nSucesso! Tudo extraído em: {os.path.abspath(destination_folder)}")

except Exception as e:
    print(f"Erro no processo: {e}")