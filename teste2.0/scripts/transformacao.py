import pandas as pd
import os

def carregar_dados(caminho_csv, tipo_arquivo="contabil"):
    """Lê o CSV garantindo a tipagem correta de CNPJ e Valores."""
    # CNPJ sempre como string para não perder o zero à esquerda
    # ValorDespesas precisa converter a vírgula para ponto antes de virar float
    df = pd.read_csv(caminho_csv, sep=';', encoding='latin1', dtype={'CNPJ': str, 'REG_ANS': str})

    if 'ValorDespesas' in df.columns:
        df['ValorDespesas'] = (
            df['ValorDespesas']
            .astype(str)
            .str.replace(',', '.')
            .astype(float)
        )
    
    if 'CNPJ' in df.columns:
        df['CNPJ'] = df['CNPJ'].str.replace(r'\D', '', regex=True).str.zfill(14)
    
    if 'ValorDespesas' in df.columns:
        # Se o valor vier como '123,45', transformamos em 123.45 (float)
        if df['ValorDespesas'].dtype == object:
            df['ValorDespesas'] = df['ValorDespesas'].str.replace(',', '.').astype(float)
            
    return df

def processar_join(df_contabil, df_cadop):

    df_cadop = df_cadop.rename(columns={'REGISTRO_OPERADORA': 'RegistroANS'})
    """Realiza o join e trata inconsistências de CNPJs."""
    # Tratando duplicatas no cadastro (Trade-off: evitar inflar valores)
    df_cadop_clean = df_cadop.drop_duplicates(subset=['CNPJ'], keep='first')
    
    # Join (Left Join para manter integridade das despesas)
    df_final = pd.merge(df_contabil, 
                        df_cadop_clean[['CNPJ', 'RegistroANS', 'Modalidade', 'UF']], 
                        on='CNPJ', 
                        how='left')
    
    # Preenchimento de lacunas (Análise Crítica: registros sem match)
    df_final['UF'] = df_final['UF'].fillna('N/I')
    df_final['Modalidade'] = df_final['Modalidade'].fillna('NAO_IDENTIFICADO')
    df_final['RegistroANS'] = df_final['RegistroANS'].fillna('000000')

    return df_final

def gerar_agregacao_final(df_processado):
    """Calcula estatísticas e exporta para CSV."""
    
    # 1. Agrupamos apenas pelas colunas que IDENTIFICAM a operadora e localidade
    # NÃO colocamos 'ValorDespesas', 'Trimestre' ou 'Ano' aqui, senão a soma não acontece!
    agregado = df_processado.groupby(['CNPJ', 'Razao_Social', 'RegistroANS', 'Modalidade', 'UF']).agg(
        Total_Despesas=('ValorDespesas', 'sum'),
        Media_Trimestral=('ValorDespesas', 'mean'),
        Desvio_Padrao=('ValorDespesas', 'std')
    ).reset_index()

    # 2. Agora o 'Total_Despesas' existe! Podemos preencher o Desvio Padrão
    agregado['Desvio_Padrao'] = agregado['Desvio_Padrao'].fillna(0)

    # 3. Ordenação (Agora a chave 'Total_Despesas' está disponível no DataFrame)
    agregado = agregado.sort_values(by='Total_Despesas', ascending=False)
    
    # 4. Seleção das colunas finais que vão para o CSV
    colunas_finais = [
        'CNPJ', 'Razao_Social', 'RegistroANS', 'Modalidade', 'UF', 
        'Total_Despesas', 'Media_Trimestral', 'Desvio_Padrao'
    ]
    agregado = agregado[colunas_finais]

    # 5. Exportação
    agregado.to_csv("despesas_agregadas.csv", sep=';', index=False, encoding='latin1', decimal=',')
    print("✅ Arquivo despesas_agregadas.csv gerado com sucesso!")