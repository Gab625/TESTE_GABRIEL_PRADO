import pandas as pd
import os

# Pega só o primeiro arquivo pra gente espiar
data_folder = "./dados_contabeis_2025"
arquivos = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

if arquivos:
    df_teste = pd.read_csv(os.path.join(data_folder, arquivos[0]), sep=";", encoding="latin1", nrows=5)
    print("--- NOMES REAIS DAS COLUNAS NO CSV ---")
    print(df_teste.columns.tolist())