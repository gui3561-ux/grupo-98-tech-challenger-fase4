## Purpose

Oferece artefatos narrativos de exploração e avaliação do LSTM de PETR4.SA para a entrega acadêmica, sem substituir o treino em script nem a API.

## ADDED Requirements

### Requirement: Notebook de exploração da série
O repositório SHALL incluir um notebook de exploração que apresente a série de fechamento de PETR4.SA, a limpeza de valores inválidos e a separação cronológica entre treino, validação e teste.

#### Scenario: Leitor vê a série e o split temporal
- **WHEN** o notebook de exploração é aberto após a coleta histórica existir
- **THEN** ele mostra o fechamento ao longo do tempo e identifica visualmente os trechos de treino, validação e teste, com treino anterior à validação e validação anterior ao teste

### Requirement: Notebook de treino e avaliação
O repositório SHALL incluir um notebook de treino e avaliação que explique o LSTM de horizonte D+1, apresente MAE, RMSE e MAPE do modelo e da baseline naive, e compare previsões com o fechamento real no teste.

#### Scenario: Leitor vê LSTM versus naive
- **WHEN** o notebook de avaliação é aberto com as métricas persistidas disponíveis
- **THEN** ele exibe MAE, RMSE e MAPE do LSTM e da baseline naive lado a lado e um gráfico de previsão D+1 versus fechamento real no conjunto de teste

### Requirement: Notebooks reutilizam o pipeline existente
Os notebooks MUST NOT ser o caminho oficial de treino ou de serve da API. Eles SHALL reutilizar a coleta, o pré-processamento e os artefatos já produzidos pelo pipeline.

#### Scenario: Treino oficial permanece o script
- **WHEN** um leitor consulta os notebooks e o README
- **THEN** fica explícito que o treino reproduzível é o script de treino do projeto e que a API continua sendo o único serviço de previsão

#### Scenario: Sem reimplementar a coleta
- **WHEN** o notebook de exploração precisa da série histórica
- **THEN** ele usa a coleta ou o cache já existentes do pipeline, em vez de baixar e transformar os dados por um fluxo paralelo

### Requirement: Documentação de uso acadêmico
O README SHALL descrever a pasta de notebooks, o papel de cada arquivo e como executá-los no ambiente de desenvolvimento.

#### Scenario: Entrega reproduzível só com o README
- **WHEN** um membro do grupo segue o README
- **THEN** consegue localizar os dois notebooks e saber que servem à apresentação, não ao deploy da API
