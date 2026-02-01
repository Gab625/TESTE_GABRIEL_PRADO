from scripts.transformacao import carregar_dados, processar_join, gerar_estatisticas, exportar_resultado

def executar_pipeline():    
    df_cont = carregar_dados("./dados/consolidado_despesas.csv")
    df_cad = carregar_dados("./dados/Relatorio_cadop.csv")
    
    df_unificado = processar_join(df_cont, df_cad)
    
    df_agregado = gerar_estatisticas(df_unificado)

    exportar_resultado(df_agregado, nome_zip="despesas_agregadas.zip")

if __name__ == "__main__":
    executar_pipeline()