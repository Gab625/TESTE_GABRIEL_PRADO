import pandas as pd
import os

def processar_cadop(caminho_entrada, caminho_saida):
    arquivos = [f for f in os.listdir(caminho_entrada) if "cadop" in f.lower() and f.endswith('.csv')]
    
    if not arquivos:
        print(f"Nenhum arquivo CADOP encontrado em: {caminho_entrada}")
        return

    arquivo_input = os.path.join(caminho_entrada, arquivos[0])

    print(f"Lendo arquivo de: {arquivo_input}")
    df = pd.read_csv(arquivo_input, sep=';', encoding='latin1', quotechar='"')

    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df['CNPJ'] = (df['CNPJ'].astype(str)
                  .str.replace(r'\D', '', regex=True)
                  .str.zfill(14))

    if 'Data_Registro_ANS' in df.columns:
        df['Data_Registro_ANS'] = pd.to_datetime(df['Data_Registro_ANS'], errors='coerce')
