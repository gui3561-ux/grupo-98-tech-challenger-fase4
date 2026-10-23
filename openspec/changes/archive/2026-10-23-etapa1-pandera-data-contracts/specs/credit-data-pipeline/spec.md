## ADDED Requirements

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

