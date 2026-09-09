## MODIFIED Requirements

### Requirement: Identidade e recorte da entrega
O README SHALL identificar o grupo da entrega, os integrantes (RM e nome), a ação escolhida e o horizonte da previsão, deixando explícito que o ticker do enunciado é apenas exemplo.

#### Scenario: Avaliador reconhece o recorte
- **WHEN** um avaliador abre o README
- **THEN** encontra o grupo da entrega, PETR4.SA como ação escolhida, horizonte de um pregão à frente, e a indicação de que DIS no enunciado é exemplo, não obrigação

#### Scenario: Integrantes visíveis
- **WHEN** um avaliador procura quem entregou o trabalho
- **THEN** o README lista RM371323 Guilherme Ramos Couceiro, RM372947 Lucas Ribeiro Pestana, RM373551 Sávio Aparecido Crispim, RM373555 Wesley Oliveira e RM373529 Cristiano Santos de Oliveira

### Requirement: Entregáveis da fase visíveis
O README SHALL declarar o estado dos entregáveis do enunciado: documentação, contêiner, vídeo e API em nuvem. O README SHALL deixar explícito que o vídeo será gravado posteriormente por um integrante e MUST NOT inventar uma URL pública.

#### Scenario: Nuvem e vídeo sem ambiguidade
- **WHEN** um avaliador procura o link da API em produção e o vídeo
- **THEN** o README indica Render como alvo de nuvem, mostra a URL pública se já houver deploy ou declara que a URL ainda será colada após o deploy, e deixa explícito que o vídeo será gravado posteriormente por um integrante usando `/docs`

### Requirement: Notebook de treino e avaliação
O repositório SHALL incluir um notebook de treino e avaliação que explique o LSTM de horizonte D+1, apresente MAE, RMSE e MAPE do modelo e da baseline naive, compare previsões com o fechamento real no teste, mostre os hiperparâmetros escolhidos e discuta por que a naive pode ganhar em preço absoluto.

#### Scenario: Leitor vê LSTM versus naive
- **WHEN** o notebook de avaliação é aberto com as métricas persistidas disponíveis
- **THEN** ele exibe MAE, RMSE e MAPE do LSTM e da baseline naive lado a lado e um gráfico de previsão D+1 versus fechamento real no conjunto de teste

#### Scenario: Hiperparâmetros e defesa da naive
- **WHEN** o leitor percorre o notebook de avaliação
- **THEN** vê a configuração escolhida (camadas, unidades, dropout, early stopping) em contraste com alternativas consideradas, e um texto que liga o atraso suavizado do LSTM à vitória da naive sem apontar retreino no notebook como caminho oficial
