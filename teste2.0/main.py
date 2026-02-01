from scripts.extracao import iniciar_extracao
from scripts.transformacao import carregar_dados, processar_join, gerar_estatisticas, exportar_resultado
import os

def executar_pipeline_completo():
    iniciar_extracao()

    caminho_despesas = "./dados/consolidado_despesas.csv"
    caminho_cadop = "./dados/Relatorio_cadop.csv"

    if os.path.exists(caminho_despesas) and os.path.exists(caminho_cadop):
        df_cont = carregar_dados(caminho_despesas)
        df_cad = carregar_dados(caminho_cadop)
        
        df_unificado = processar_join(df_cont, df_cad)
        df_agregado = gerar_estatisticas(df_unificado)

        exportar_resultado(df_agregado)

if __name__ == "__main__":
    executar_pipeline_completo()