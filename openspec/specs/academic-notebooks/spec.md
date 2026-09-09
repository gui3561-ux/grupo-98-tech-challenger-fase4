# academic-notebooks Specification

## Purpose

Oferece artefatos narrativos de exploração e avaliação do LSTM de PETR4.SA para a entrega acadêmica, sem substituir o treino em script nem a API.

## Requirements

### Requirement: Notebook de exploração da série
O repositório SHALL incluir um notebook de exploração que apresente a série de fechamento de PETR4.SA, a limpeza de valores inválidos e a separação cronológica entre treino, validação e teste.

#### Scenario: Leitor vê a série e o split temporal
- **WHEN** o notebook de exploração é aberto após a coleta histórica existir
- **THEN** ele mostra o fechamento ao longo do tempo e identifica visualmente os trechos de treino, validação e teste, com treino anterior à validação e validação anterior ao teste

### Requirement: Notebook de treino e avaliação
O repositório SHALL incluir um notebook de treino e avaliação que explique o LSTM de horizonte D+1, apresente MAE, RMSE e MAPE do modelo e da baseline naive, compare previsões com o fechamento real no teste, mostre os hiperparâmetros escolhidos e discuta por que a naive pode ganhar em preço absoluto.

#### Scenario: Leitor vê LSTM versus naive
- **WHEN** o notebook de avaliação é aberto com as métricas persistidas disponíveis
- **THEN** ele exibe MAE, RMSE e MAPE do LSTM e da baseline naive lado a lado e um gráfico de previsão D+1 versus fechamento real no conjunto de teste

#### Scenario: Hiperparâmetros e defesa da naive
- **WHEN** o leitor percorre o notebook de avaliação
- **THEN** vê a configuração escolhida (camadas, unidades, dropout, early stopping) em contraste com alternativas consideradas, e um texto que liga o atraso suavizado do LSTM à vitória da naive sem apontar retreino no notebook como caminho oficial

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

### Requirement: Identidade e recorte da entrega
O README SHALL identificar o grupo da entrega, os integrantes (RM e nome), a ação escolhida e o horizonte da previsão, deixando explícito que o ticker do enunciado é apenas exemplo.

#### Scenario: Avaliador reconhece o recorte
- **WHEN** um avaliador abre o README
- **THEN** encontra o grupo da entrega, PETR4.SA como ação escolhida, horizonte de um pregão à frente, e a indicação de que DIS no enunciado é exemplo, não obrigação

#### Scenario: Integrantes visíveis
- **WHEN** um avaliador procura quem entregou o trabalho
- **THEN** o README lista RM371323 Guilherme Ramos Couceiro, RM372947 Lucas Ribeiro Pestana, RM373551 Sávio Aparecido Crispim, RM373555 Wesley Oliveira e RM373529 Cristiano Santos de Oliveira

### Requirement: Fluxo após clone
O README SHALL descrever o que o clone contém e o que não contém, de modo que treino, notebooks e API local não dependam de um cache de dados que não está no Git.

#### Scenario: Clone sem cache de mercado
- **WHEN** um leitor clona o repositório sem o arquivo de cache histórico
- **THEN** o README deixa claro que os artefatos do modelo já estão no repositório para servir a API, e que treino ou notebooks baixam a série histórica se o cache não existir

### Requirement: Chamada reproduzível de previsão
O README SHALL incluir um exemplo de chamada à API de previsão que um leitor consegue copiar e executar, com janela de tamanho correto e resposta de exemplo coerente com o modelo persistido.

#### Scenario: Copiar e prever
- **WHEN** a API local está no ar e o leitor segue o exemplo de previsão do README
- **THEN** o comando usa JSON válido com exatamente 60 fechamentos e a resposta de exemplo contém ticker PETR4.SA, horizonte D+1 e um fechamento previsto numérico alinhado ao artefato atual

### Requirement: Entregáveis da fase visíveis
O README SHALL declarar o estado dos entregáveis do enunciado: documentação, contêiner, vídeo e API em nuvem. O README SHALL deixar explícito que o vídeo será gravado posteriormente por um integrante e MUST NOT inventar uma URL pública.

#### Scenario: Nuvem e vídeo sem ambiguidade
- **WHEN** um avaliador procura o link da API em produção e o vídeo
- **THEN** o README indica Render como alvo de nuvem, mostra a URL pública se já houver deploy ou declara que a URL ainda será colada após o deploy, e deixa explícito que o vídeo será gravado posteriormente por um integrante usando `/docs`

### Requirement: Monitoramento demonstrável no README
O README SHALL mostrar como observar latência e uso de recursos após uma previsão, usando o endpoint de métricas já existente.

#### Scenario: Métricas depois do predict
- **WHEN** o leitor segue a seção de monitoramento do README após uma previsão bem-sucedida
- **THEN** consegue chamar o endpoint de métricas e reconhecer contagem, latência, CPU e memória
