from scripts.transformacao import carregar_dados, processar_join, gerar_agregacao_final

def executar_pipeline():
    # 1. Carrega os dados usando as funções do outro arquivo
    df_cont = carregar_dados("./dados/consolidado_despesas.csv")
    df_cad = carregar_dados("./dados/Relatorio_cadop.csv")
    
    # 2. Faz o Join (Ajustado os nomes das variáveis aqui)
    df_unificado = processar_join(df_cont, df_cad)
    
    # 3. Gera o resultado
    gerar_agregacao_final(df_unificado)

if __name__ == "__main__":
    executar_pipeline()