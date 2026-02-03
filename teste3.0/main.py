from scripts.extracao import baixar_arquivo
from scripts.transformacao import processar_cadop
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

PASTA_RAIZ_DADOS = os.path.abspath(os.path.join(diretorio_atual, "..", "dados"))

def executar_pipeline_sql():
    print(f"--- Iniciando Preparação (Diretório Alvo: {PASTA_RAIZ_DADOS}) ---")

    caminho_final_csv = os.path.join(PASTA_RAIZ_DADOS, "Relatorio_cadop.csv")

    baixar_arquivo("operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv", PASTA_RAIZ_DADOS)

    processar_cadop(PASTA_RAIZ_DADOS, caminho_final_csv)

    print(f"--- Pipeline Concluído! Verifique a pasta: {PASTA_RAIZ_DADOS} ---")

if __name__ == "__main__":
    executar_pipeline_sql()