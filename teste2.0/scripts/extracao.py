import requests
import os
import zipfile

URL_BASE = "https://dadosabertos.ans.gov.br/FTP/PDA/"
PASTA_DESTINO = os.path.join(os.path.dirname(__file__), "..", "dados")

def baixar_arquivo(caminho_especifico):
    url_alvo = requests.compat.urljoin(URL_BASE, caminho_especifico)
    os.makedirs(PASTA_DESTINO, exist_ok=True)

    nome_arquivo = caminho_especifico.split('/')[-1]
    caminho_salvamento = os.path.join(PASTA_DESTINO, nome_arquivo)
    
    try:
        response = requests.get(url_alvo, stream=True)
        response.raise_for_status()
        with open(caminho_salvamento, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception:
        pass

def descompactar_despesas():
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.abspath(os.path.join(caminho_script, "..", ".."))
    
    nome_zip = "consolidado_despesas.zip"
    caminho_zip = os.path.join(diretorio_raiz, nome_zip)
    
    if os.path.exists(caminho_zip):
        os.makedirs(PASTA_DESTINO, exist_ok=True)
        with zipfile.ZipFile(caminho_zip, 'r') as z:
            z.extractall(PASTA_DESTINO)

def iniciar_extracao():
    baixar_arquivo("operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv")
    descompactar_despesas()

if __name__ == "__main__":
    iniciar_extracao()