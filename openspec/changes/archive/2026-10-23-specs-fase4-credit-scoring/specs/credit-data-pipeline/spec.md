## Purpose

Prepara o dataset base de Credit Scoring a partir do German Credit Data com recuperação do rótulo de risco e divisão estratificada entre referência e produção.

## ADDED Requirements

### Requirement: Recuperação do rótulo original de risco
O pipeline de dados SHALL obter o rótulo binário de risco (`Risk` com valores `good` e `bad`) a partir do repositório UCI (dataset id 144) e anexá-lo às variáveis preditoras do dataset bruto sem alterar a ordenação dos registros.

#### Scenario: Execução bem-sucedida da montagem do dataset
- **WHEN** o script de preparação de dataset é executado com acesso à fonte do UCI
- **THEN** o sistema gera o arquivo `data/raw/german_credit_with_risk.csv` contendo todas as variáveis preditoras e a coluna `Risk` com exatamente 1.000 registros

#### Scenario: Fallback para download direto caso a API falhe
- **WHEN** o cliente de API do UCI encontrar erro de conexão
- **THEN** o sistema aciona o download alternativo do arquivo de dados oficial preservando a integridade das 1.000 amostras

### Requirement: Tratamento de categorias ausentes legítimas
O pipeline de dados SHALL tratar valores ausentes nas variáveis de saldo bancário (`Saving accounts` e `Checking account`) como categoria legítima denominada `no_account` em vez de descartar registros ou imputar estatísticas de tendência central.

#### Scenario: Normalização de dados ausentes de conta
- **WHEN** o dataset com rótulo é carregado para pré-processamento
- **THEN** todas as ocorrências nulas em `Saving accounts` e `Checking account` são substituídas pelo valor `no_account` mantendo o total de linhas intacto

### Requirement: Particionamento estratificado Referência e Produção
O pipeline de dados SHALL dividir o dataset pré-processado em um conjunto de Referência (70%) e um conjunto de Produção-base (30%) mantendo a mesma proporção de classes do target `Risk` em ambas as partições.

#### Scenario: Geração dos conjuntos de dados de referência e produção-base
- **WHEN** o particionamento é executado com semente aleatória determinística e proporção de 30% para produção
- **THEN** o sistema salva `data/reference/reference.csv` com 700 linhas e `data/production/production_raw.csv` com 300 linhas, ambos preservando aproximadamente 70% de instâncias `good` e 30% de instâncias `bad`

