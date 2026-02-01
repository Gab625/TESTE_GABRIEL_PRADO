import pandas as pd
import zipfile
import os

def carregar_dados(caminho_csv):
    df = pd.read_csv(
        caminho_csv, 
        sep=';', 
        encoding='latin1', 
        quotechar='"', 
        on_bad_lines='skip',
        dtype=str,
        decimal='.'
    )

    df.columns = df.columns.str.strip()

    if 'ValorDespesas' in df.columns:       
        df['ValorDespesas'] = (
            df['ValorDespesas']
            .str.replace(',', '.')
            .str.strip()
        )
        df['ValorDespesas'] = pd.to_numeric(df['ValorDespesas'], errors='coerce')
        
        df = df.dropna(subset=['ValorDespesas'])
    
    if 'CNPJ' in df.columns:
        df['CNPJ'] = df['CNPJ'].str.replace(r'\D', '', regex=True).str.zfill(14)
            
    return df

def processar_join(df_contabil, df_cadop):
    df_cadop = df_cadop.rename(columns={'REGISTRO_OPERADORA': 'RegistroANS'})
    
    df_cadop_clean = df_cadop.drop_duplicates(subset=['CNPJ'], keep='first')
    
    df_final = pd.merge(df_contabil, 
                        df_cadop_clean[['CNPJ', 'RegistroANS', 'Modalidade', 'UF']], 
                        on='CNPJ', 
                        how='left')
    
    df_final['UF'] = df_final['UF'].fillna('N/I')
    df_final['Modalidade'] = df_final['Modalidade'].fillna('NAO_IDENTIFICADO')
    df_final['RegistroANS'] = df_final['RegistroANS'].fillna('000000')

    return df_final

def gerar_estatisticas(df_processado):
    agregado = df_processado.groupby(['Razao_Social', 'UF', 'CNPJ', 'RegistroANS', 'Modalidade']).agg(
        Total_Despesas=('ValorDespesas', 'sum'),
        Media_Trimestral=('ValorDespesas', 'mean'),
        Desvio_Padrao=('ValorDespesas', 'std')
    ).reset_index()

    agregado['Desvio_Padrao'] = agregado['Desvio_Padrao'].fillna(0)

    agregado = agregado.sort_values(by='Total_Despesas', ascending=False)
    
    return agregado

def exportar_resultado(df_agregado, nome_arquivo="despesas_agregadas.csv", nome_zip="Teste_Gabriel_Prado.zip"):
    zip_path = os.path.join("..", nome_zip)

    df_agregado.to_csv(
        nome_arquivo, 
        sep=';', 
        index=False, 
        encoding='latin1', 
        decimal='.'
    )

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(nome_arquivo)

    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)