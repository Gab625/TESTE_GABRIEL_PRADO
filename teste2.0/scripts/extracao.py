import requests
import os
import zipfile

URL_BASE = "https://dadosabertos.ans.gov.br/FTP/PDA/"
PASTA_DESTINO = "../dados"

def baixar_arquivo(caminho_especifico):
    URL_ALVO = requests.compat.urljoin(URL_BASE, caminho_especifico)
    os.makedirs(PASTA_DESTINO, exist_ok=True)

    nome_arquivo = caminho_especifico.split('/')[-1]
    caminho_salvamento = os.path.join(PASTA_DESTINO, nome_arquivo)
    
    try:
        response = requests.get(URL_ALVO, stream=True)
        response.raise_for_status()

        with open(caminho_salvamento, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    except Exception as e:
        print("{e}")


def extrair_dados():
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.abspath(os.path.join(caminho_script, "..", ".."))

    nome_zip = "consolidado_despesas.zip"
    caminho_zip = os.path.join(diretorio_raiz, nome_zip)

    pasta_destino = os.path.join(PASTA_DESTINO)

    if os.path.exists(caminho_zip):
        os.makedirs(pasta_destino, exist_ok=True)
        with zipfile.ZipFile(caminho_zip, 'r') as z:
            z.extractall(pasta_destino)
            print(f"✅ Extraído com sucesso para: {pasta_destino}")
            print(f"📄 Arquivos dentro do ZIP: {z.namelist()}")
    else:
        print(f"❌ Erro: Arquivo não encontrado!")
        print(f"📍 Caminho verificado: {caminho_zip}")

if __name__ == "__main__":
    extrair_dados()


def extrair_dados():
    baixar_arquivo("operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv")


if __name__ == "__main__":
    extrair_dados()