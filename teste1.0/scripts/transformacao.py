import pandas as pd
import os
import zipfile
import io

PASTA_DADOS = "./dados"

def transformar_contabeis():
    arquivo_contabeis = [f for f in os.listdir(PASTA_DADOS) if f.endswith('.csv') and "cadop" not in f.lower()]
    
    lista_dfs = []

    for arquivo in arquivo_contabeis:
        caminho_contabeis = os.path.join(PASTA_DADOS, arquivo)
        print(f"Lendo dados: {arquivo}")

        df = pd.read_csv(caminho_contabeis, sep=';', encoding='latin1', decimal=",")

        df['REG_ANS'] = df['REG_ANS'].astype(str).str.strip()

        df['DATA'] = pd.to_datetime(df['DATA'])
        df['Ano'] = df['DATA'].dt.year
        df['Trimestre'] = ((df['DATA'].dt.month - 1) // 3) + 1

        filtro_despesas = df['DESCRICAO'].str.contains('Eventos|Sinistros', case=False, na=False)
        df_filtrado = df[filtro_despesas].copy()
        df_filtrado = df_filtrado.rename(columns={'VL_SALDO_FINAL': 'ValorDespesas'})

        colunas_alvo = ['REG_ANS', 'Trimestre', 'Ano', 'ValorDespesas']
        lista_dfs.append(df_filtrado[colunas_alvo])

    if lista_dfs:
        df_consolidado = pd.concat(lista_dfs, ignore_index=True)

        df_agrupado = df_consolidado.groupby(['REG_ANS', 'Ano', 'Trimestre'], as_index=False)['ValorDespesas'].sum()

        return df_agrupado

def transformar_cadop():
    arquivo_cadop = [f for f in os.listdir(PASTA_DADOS) if "relatorio_cadop" in f.lower() and f.endswith('.csv')]
    print(f"Lendo dados: cadop.csv")

    caminho_cadop = os.path.join(PASTA_DADOS, arquivo_cadop[0])
    df_cadop = pd.read_csv(caminho_cadop, sep=';', encoding='latin1')

    df_cadop.columns = df_cadop.columns.str.strip()

    colunas_alvo = ['CNPJ', 'Razao_Social', 'REGISTRO_OPERADORA']
    df_cadop = df_cadop[colunas_alvo].copy()

    df_cadop = df_cadop.rename(columns={'REGISTRO_OPERADORA': 'REG_ANS'})

    df_cadop['REG_ANS'] = df_cadop['REG_ANS'].astype(str).str.strip()

    return df_cadop

def tabela_consolidada():
    df_contabil = transformar_contabeis()
    df_cadop = transformar_cadop()

    for df in [df_contabil, df_cadop]:
        if 'CNPJ' in df.columns:
            df['CNPJ'] = df['CNPJ'].astype(str).str.replace(r'\.0$', '', regex=True).str.zfill(14)

    df_final = pd.merge(df_contabil, df_cadop, on='REG_ANS', how='left')

    df_final = df_final.dropna()
    df_final = df_final[(df_final != '').all(axis=1)]

    colunas_ordenadas = ['CNPJ', 'Razao_Social', 'Trimestre','Ano', 'ValorDespesas']
    df_final = df_final[colunas_ordenadas]

    zip_path = "../consolidado_despesas.zip"
    csv_name = "consolidado_despesas.csv"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:     
        csv_buffer = io.StringIO()
        df_final.to_csv(csv_buffer, sep=';', index=False, encoding='latin1', decimal=',')
        
        zf.writestr(csv_name, csv_buffer.getvalue())