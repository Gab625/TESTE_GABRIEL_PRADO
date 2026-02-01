import pandas as pd
import os

# O script vai procurar o arquivo na mesma pasta onde ele estiver
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

def processar_cadop():
    # Busca qualquer CSV que tenha "cadop" no nome na pasta atual
    arquivos = [f for f in os.listdir(diretorio_atual) if "cadop" in f.lower() and f.endswith('.csv')]
    
    if not arquivos:
        print("❌ Nenhum arquivo CADOP encontrado na pasta!")
        return

    arquivo_input = arquivos[0]
    arquivo_output = "cadop_pronto_para_o_sql.csv"
    
    print(f"🛠️  Tratando: {arquivo_input}...")

    # 1. Lendo com quotechar para ELIMINAR as aspas duplas que travam o SQL
    df = pd.read_csv(arquivo_input, sep=';', encoding='latin1', quotechar='"')

    # 2. Limpeza de strings (remove espaços em branco sobrando)
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # 3. Tratamento do CNPJ (garante 14 dígitos, sem .0 e sem lixo)
    df['CNPJ'] = (df['CNPJ'].astype(str)
                  .str.replace(r'\D', '', regex=True)
                  .str.zfill(14))

    # 4. Formatação de Data para o padrão ISO (YYYY-MM-DD) que o SQL exige
    if 'Data_Registro_ANS' in df.columns:
        df['Data_Registro_ANS'] = pd.to_datetime(df['Data_Registro_ANS'], errors='coerce')

    # 5. Exportação LIMPA
    # Usamos quoting=3 (QUOTE_NONE) para garantir que o Pandas não coloque aspas de volta
    # O separador continua ';' mas agora o dado está 'nu', como o SQL gosta.
    df.to_csv(arquivo_output, sep=';', index=False, encoding='latin1', decimal='.')

    print(f"✅ Prontinho! Use o arquivo '{arquivo_output}' no seu COPY do PostgreSQL.")
    print(f"🚀 Colunas tratadas: {len(df.columns)}")

if __name__ == "__main__":
    processar_cadop()