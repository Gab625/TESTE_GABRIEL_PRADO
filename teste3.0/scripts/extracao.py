import requests
import os

URL_BASE = "https://dadosabertos.ans.gov.br/FTP/PDA/"

def baixar_arquivo(caminho_especifico, pasta_destino):
    url_alvo = requests.compat.urljoin(URL_BASE, caminho_especifico)
    os.makedirs(pasta_destino, exist_ok=True)

    nome_arquivo = caminho_especifico.split('/')[-1]
    caminho_salvamento = os.path.join(pasta_destino, nome_arquivo)
    
    try:
        print(f"Baixando: {nome_arquivo}...")
        response = requests.get(url_alvo, stream=True)
        response.raise_for_status()
        with open(caminho_salvamento, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Download concluído: {caminho_salvamento}")
    except Exception as e:
        print(f"Erro ao baixar: {e}")