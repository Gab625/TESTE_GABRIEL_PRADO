from scripts import extracao
from scripts import transformacao

def executar_pipeline():
    extracao.extrair_dados()
    transformacao.tabela_consolidada()
if __name__ == "__main__":
    executar_pipeline()