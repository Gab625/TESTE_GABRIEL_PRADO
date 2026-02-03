# 📊 IntuitiveCare - Gabriel Prado

# Projeto para o tratamentos de dados da ANS

## 1. Configuração do Ambiente e Instalação

Para garantir que o projeto execute de forma isolada e segura, siga os passos abaixo:

### 1.1 Criando o Ambiente Virtual (VENV)

python -m venv venv

### 1.2 Ativando o ambiente virtual

Windows (PowerShell): .\venv\Scripts\activate.ps1
Windows (CMD): .\venv\Scripts\activate.bat
Linux / macOS: source venv/bin/activate

### 1.3 Instalando as dependências

pip install -r requirements.txt

### 1.4 Dependências Utilizadas

Pandas (3.0.0): Manipulação e agregação de dados.

BeautifulSoup4: Extração de dados da web.

Requests: Comunicação com a API pública da ANS.

NumPy: Cálculos vetoriais e estatísticos.

## 2. Teste de Integração com API Pública (Tópico 1)

### 2.1. Arquitetura da Solução

A solução foi desenhada seguindo princípios de **modularidade** e **separação de responsabilidades**, facilitando a manutenção e testes isolados:

- **`extracao.py`**: Gerencia o _web scraping_ dinâmico e a automação de downloads.
- **`transformacao.py`**: Centraliza a inteligência de limpeza, normalização e cruzamento de dados (_Merge/Join_).
- **`main.py`**: Atua como o orquestrador do pipeline de ETL (Extract, Transform, Load).

---

### 2.2. Justificativas das Decisões Técnicas

#### **Resiliência no Acesso à API Pública**

Para lidar com a instabilidade de nomenclaturas da API da ANS, utilizei a biblioteca `BeautifulSoup`.

- **Decisão:** Em vez de mapear links estáticos (que quebrariam caso a ANS mudasse a versão do arquivo), o código varre dinamicamente as tags `<a>`, identificando padrões de extensões `.zip` e `.csv`.
- **Justificativa:** Garante que o pipeline continue funcionando mesmo se novos arquivos forem adicionados ou se a estrutura de diretórios sofrer pequenas alterações.

#### **Trade-off: Processamento Incremental vs. Memória**

- **Decisão:** Optei pelo processamento **incremental**, realizando a leitura e filtragem individual de cada arquivo antes da consolidação.
- **Justificativa:** Os dados contábeis da ANS são massivos. O carregamento de todos os arquivos simultaneamente poderia causar falhas devido capacidade de memória. Ao filtrar por "Eventos/Sinistros" antes do agrupamento final, otimizamos o consumo de RAM.

---

### 2.3. Análise Crítica e Tratamento de Inconsistências

Durante a etapa de consolidação, apliquei as seguintes tratativas para garantir a integridade analítica:

| **Valores (`VL_SALDO_FINAL`)** | Substituição de separadores e conversão para `float`. | Padronização essencial para cálculos matemáticos e compatibilidade com o tipo `Numeric` do PostgreSQL. |
| **Inconsistência de Datas** | `pd.to_datetime` com `errors='coerce'`. | Evita que registros com datas corrompidas interrompam o pipeline, permitindo extrair Ano/Trimestre com segurança. |
| **Identificadores (CNPJ/ANS)** | `str.strip()`, `zfill(14)` e remoção de máscaras. | Tratamento de strings para preservar zeros à esquerda, garantindo que o `Join` entre tabelas não falhe por formatação. |
| **Dados Fragmentados** | `df.groupby()` por Operadora/Ano/Tri. | Consolida múltiplas linhas de despesas em um único valor por período, evitando duplicidade de registros no banco. |

---

### 2.4. Normalização Automática de Estruturas

Para resolver o desafio de arquivos com formatos e colunas variadas, implementei:

1.  **Identificação de dados não passados no script de teste:** Dados necessários como: CNPJ e Razão_Social, não estavam nos documentos de despesas. Verifiquei que esses dados estavam na mesma base pública, porém em outro documento com nome Relatório_cadop.csv. Desse modo, foi possível realizar a inserção das colunas requeridas através do REG_ANS, que são dados comuns entre as tabelas de despesas e dados do cadop.
2.  **Identificação por Conteúdo:** O código busca a despesa através de palavras-chave (`Eventos` ou `Sinistros`) na coluna de descrição, tornando a captura independente da ordem das linhas no CSV original.
3.  **Mapeamento de Chaves Relacionais:** O cruzamento entre a base financeira e a base cadastral (`CADOP`) é realizado através do `REG_ANS`, o identificador mais resiliente e padronizado nas publicações da ANS.

---

### 2.5. Entrega Final

Ao final do processo, o sistema gera o arquivo `consolidado_despesas.csv` com as colunas padronizadas (`CNPJ`, `Razao_Social`, `Trimestre`, `Ano`, `ValorDespesas`) e realiza a compactação automática em um arquivo ZIP, conforme exigido pelos requisitos técnicos.

# 3. Teste de Transformação e Validação de Dados (Tópico 2)

Nesta etapa, o foco foi garantir a **qualidade** e o **enriquecimento** dos dados financeiros através do cruzamento com a base cadastral das operadoras (Relatório_cadop).

## 3.1. Validação de Dados e Estratégias de Tratamento

Para garantir a integridade dos dados antes da agregação, implementei as seguintes validações:

- **Valores Numéricos:** Realizei a conversão da coluna `ValorDespesas` para o tipo `float`. Registros que continham caracteres não numéricos ou nulos foram descartados via `dropna`.
- **Limpeza de Identificadores (CNPJ):** Utilizei expressões regulares (Regex) para remover máscaras e caracteres especiais, aplicando o método `zfill(14)` para garantir a padronização das chaves.

#### **Trade-off: Tratamento de CNPJs Inválidos**

- **Decisão:** Optei pela normalização e preenchimento (padding) em vez do descarte imediato.
- **Justificativa:** Em bases públicas como a da ANS, é comum encontrar CNPJs que perderam os zeros à esquerda durante exportações prévias para formatos como Excel. O descarte causaria perda de histórico financeiro relevante. A validação final ocorre de forma intrínseca durante o `Join`: se o CNPJ normalizado não existir no cadastro oficial, ele é sinalizado para auditoria posterior.

---

## 3.2. Enriquecimento de Dados e Tratamento de Falhas

O enriquecimento foi realizado através do cruzamento (Join) do consolidado financeiro com o **Relatório CADOP** (Operadoras Ativas).

#### **Análise Crítica: Conflito de Chaves e Duplicidade**

- **Problema:** Encontrei CNPJs que aparecem múltiplas vezes no cadastro com dados divergentes.
- **Solução:** Apliquei `drop_duplicates(subset=['CNPJ'], keep='first')` na base cadastral antes do cruzamento.
- **Justificativa:** Esta estratégia garante a cardinalidade **1:1** no relacionamento. Sem este tratamento, o valor das despesas seria multiplicado indevidamente ao encontrar múltiplos registros cadastrais para a mesma empresa.

#### **Trade-off: Estratégia de Join e Registros sem Match**

- **Decisão:** Utilizei a estratégia de **Left Join**, mantendo a base de despesas como a tabela principal (_left_).
- **Justificativa:** O objetivo do teste é a análise financeira. Registros de despesas que não possuem correspondente no cadastro ativo foram mantidos e enriquecidos com labels padrão (ex: `UF = 'N/I'`, `RegistroANS = '000000'`). Isso garante que o **Total de Despesas** do setor não seja subestimado por defasagem no cadastro.

---

## 3.3. Agregação e Estatística Descritiva

Implementei uma lógica de agregação para identificar o perfil de gastos por Operadora e Estado:

- **Métricas Calculadas:** Soma total, média trimestral e **Desvio Padrão** das despesas.
- **Tratamento de Volatilidade:** Operadoras com apenas um registro trimestral geram desvio padrão nulo (`NaN`). Nestes casos, o código trata automaticamente para `0`, indicando ausência de variação histórica.

#### **Trade-off: Ordenação e Performance**

- **Decisão:** A ordenação (`sort_values`) é executada apenas **após** a agregação dos dados.
- **Justificativa:** Ordenar milhões de linhas de dados brutos é custoso para a CPU. Ao realizar o agrupamento (`groupby`) primeiro, reduzimos drasticamente o volume de dados na memória, tornando a ordenação por valor total (do maior para o menor) muito mais eficiente e rápida.

---

## 3.4. Entrega e Exportação

O pipeline gera o arquivo `despesas_agregadas.csv` com separador `;` e codificação `latin1`, otimizado para abertura em ferramentas de BI e Excel. O arquivo final é compactado automaticamente seguindo o padrão: `Teste_Gabriel_Prado.zip`.

# 4 Teste de Banco de Dados e Análise (Tópico 3)

Nesta etapa, estruturei o ambiente de banco de dados utilizando **PostgreSQL** (versão 18.0) para suportar análises complexas e garantir a precisão dos cálculos financeiros exigidos pela ANS.

## 4.1. Arquitetura e Modelagem (DDL)

### **Justificativa de Desnormalização (Opção A)**

- **Decisão:** Optei pela abordagem **Desnormalizada**.
- **Justificativa:** Considerando que os dados cadastrais das tabelas, a desnormalização é o mais indicada, como os dados serviram para relatórios analíticos, devido ter menos `JOIN` para ser feito. Isso implica que ele não terá uma frequência grande de atualização, por ter menos operações, com isso o ideal é ele estar desnormalizado. Outro motivo é que queries analíticas são mais complexas e é interessante os dados estarem pré-processados na base, caso com a tabela `despesas_agregadas`, que os dados já estão parcialmente agregados e facilitam queries sem `JOIN`.

### **Justificativa de Tipos de Dados**

- **Valores Monetários (`NUMERIC`):** Diferente do tipo `FLOAT`, que possui imprecisão binária em cálculos de ponto flutuante, o `NUMERIC(20,2)` garante precisão absoluta para contabilidade, evitando erros de arredondamento em somatórios de bilhões de reais.
- **Datas (`DATE`):** Utilizei o tipo `DATE` nativo. Isso permite o uso de funções de série temporal e ordenação cronológica de forma performática, superior ao processamento de strings (`VARCHAR`).

---

## 4.2. Análise Crítica das Queries Analíticas

### **Query 1: Crescimento Percentual (Window Functions)**

- **Desafio:** Como tratar operadoras com trimestres faltantes?
- **Solução:** Utilizei as funções de janela `FIRST_VALUE` e `LAST_VALUE` com a cláusula `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
- **Destaque Técnico:** Implementei o uso de `NULLIF(valor_inicial, 0)` no cálculo da taxa. Isso evita o erro crítico de **Divisão por Zero**, transformando-o em um valor nulo, o que garante a continuidade da execução da query em grandes datasets.

### **Query 2: Distribuição por UF**

- **Estratégia:** Realizei um `JOIN` entre a tabela de agregados e a tabela de operadoras.
- **Métrica Avançada:** Calculei a média por operadora utilizando `SUM(total) / COUNT(DISTINCT cnpj)`. Isso remove distorções causadas por operadoras com múltiplos registros no mesmo estado, entregando o gasto médio real por entidade federativa.

### **Query 3: Operadoras Acima da Média (CTEs)**

- **Trade-off Técnico:** Optei pelo uso de **CTEs (Common Table Expressions)**.
- **Justificativa:** Embora pudesse ser resolvido com subqueries, a CTE (`media_geral` e `analise_trimestral`) torna o código muito mais legível e fácil de debugar. O otimizador de consulta do PostgreSQL trata a CTE de forma eficiente, calculando a média global uma única vez antes da comparação.

---
