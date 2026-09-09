## Why

O Tech Challenge da Fase 4 da pós em Machine Learning (FIAP) exige um pipeline completo de Deep Learning: coletar preços históricos de uma ação, treinar um LSTM para prever o fechamento, servir o modelo em API e demonstrar deploy com monitoramento. O repositório ainda não tem essa capacidade, e a entrega vale 90% da nota das disciplinas da fase.

## What Changes

- Coletar preços históricos de **PETR4.SA** via yfinance (série diária a partir de 2018) e preparar janelas temporais de 60 pregões para treino, validação e teste sem shuffle.
- Treinar um LSTM univariado no Close para prever o **fechamento do próximo pregão (D+1)**, avaliar com MAE, RMSE e MAPE e comparar com baseline naive (amanhã = hoje).
- Persistir o modelo treinado e o scaler para inferência.
- Expor uma API REST (FastAPI) em que o usuário envia a janela histórica de fechamentos e recebe a previsão de D+1.
- Empacotar a API em Docker, com endpoints de saúde e métricas de latência e uso de recursos, e documentar o caminho de deploy em nuvem.

## Capabilities

### New Capabilities

- `stock-data-pipeline`: coleta de preços históricos via yfinance e pré-processamento temporal (limpeza, split cronológico, normalização, janelas).
- `lstm-forecast`: treino, avaliação (MAE/RMSE/MAPE vs baseline naive) e exportação do LSTM de fechamento D+1.
- `prediction-api`: API REST que recebe preços históricos e devolve a previsão de fechamento do próximo pregão.
- `production-ops`: empacotamento Docker, health/readiness e monitoramento de latência e recursos.

### Modified Capabilities

- Nenhuma. O repositório ainda não possui specs principais.

## Impact

- Projeto greenfield: código Python em `src/` (dados, modelo, API), artefatos em `models/`, `Dockerfile` e `compose.yaml`.
- Dependências novas: yfinance, TensorFlow/Keras, FastAPI, scikit-learn (scaler), instrumentação de métricas.
- Sem banco de dados e sem frontend: inferência stateless; documentação interativa via OpenAPI/Swagger.
- Entregáveis acadêmicos fora do runtime (vídeo e README) acompanham o deploy, mas não são comportamento de sistema.
