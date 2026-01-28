import pandas as pd
import os

data_folder = "./dados_contabeis_2025"
lista_df = []

for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        full_path = os.path.join(data_folder, file)
        print(f"Lendo: {file}")

        df_temp = pd.read_csv(full_path, sep=";", encoding="latin1")

        df_temp['DATA'] = pd.to_datetime(df_temp['DATA'])
        df_temp['Ano'] = df_temp['DATA'].dt.year
        df_temp['Trimestre'] = ((df_temp['DATA'].dt.month - 1) // 3) + 1

        mapeamento = {
            'REG_ANS': 'CNPJ',
            'DESCRICAO': 'RazaoSocial',
            'VL_SALDO_FINAL': 'ValorDespesas'
        }

        df_temp = df_temp.rename(columns=mapeamento)

        filtro = df_temp['RazaoSocial'].str.contains('Eventos|Sinistros', case=False, na=False)
        df_temp = df_temp[filtro]

        colunas_finais = ["CNPJ" , "RazaoSocial", "Trimestre", "Ano", "ValorDespesas"]

        df_temp = df_temp[colunas_finais]
        lista_df.append(df_temp)

if lista_df:
    df_final = pd.concat(lista_df, ignore_index=True)

    print(f"\nConsolidação concluída! Total de linhas: {len(df_final)}")
    df_final.to_csv("resultado_sinistros_ans.csv", sep=";", index=False, encoding="latin1")
else:
    print("Nenhum arquivo CSV encontrado para consolidar.")