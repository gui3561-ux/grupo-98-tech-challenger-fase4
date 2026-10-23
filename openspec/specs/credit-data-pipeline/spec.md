# credit-data-pipeline Specification

## Purpose

Prepara o dataset base de Credit Scoring a partir do German Credit Data com recuperação do rótulo de risco e divisão estratificada entre referência e produção.

## Requirements

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

### Requirement: Contrato de dados com Pandera para controle de qualidade
O pipeline de dados SHALL validar as instâncias do dataset de crédito contra um schema formal do Pandera (`DataFrameSchema`), impondo regras rígidas de integridade: tipos de dados corretos, limites numéricos (`Age >= 18` e `<= 120`, `Credit amount > 0`, `Duration > 0`), domínios categóricos válidos para `Sex`, `Job`, `Housing`, `Saving accounts`, `Checking account`, `Purpose` e `Risk`, e ausência de valores nulos nas colunas obrigatórias.

#### Scenario: Dataset válido é aprovado pelo contrato
- **WHEN** o dataset pré-processado contendo valores conformes é submetido à validação de esquema
- **THEN** o contrato do Pandera valida com sucesso e devolve o dataframe inalterado sem levantar exceções

#### Scenario: Violações de esquema disparam erro estruturado e detalhado
- **WHEN** um conjunto de dados violar uma ou mais restrições do contrato (ex.: idade menor que 18 ou nulos em colunas obrigatórias)
- **THEN** o validador interrompe o processamento e emite uma exceção contendo a listagem analítica das colunas, índices e valores que falharam na checagem

### Requirement: Interceptação e bloqueio de lote corrompido (Ingestion Gate)
O sistema SHALL disponibilizar uma rotina demonstrativa que gera ou injeta um lote de dados com anomalias propositais (ex.: clientes menores de idade, crédito negativo, categorias inexistentes e nulos não autorizados) e comprova que a barreira de ingestão bloqueia o lote, impedindo que o modelo consuma dados inválidos.

#### Scenario: Lote anômalo é interceptado e bloqueado antes da ingestão
- **WHEN** o lote intencionalmente corrompido é processado pela barreira de validação
- **THEN** a operação de ingestão é imediatamente abortada, registrando em log as razões do bloqueio e garantindo que nenhum registro defeituoso avance para as etapas de treino ou predição


