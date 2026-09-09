## 1. Setup do projeto

- [x] 1.1 Criar a estrutura `src/data`, `src/model`, `src/api`, `models/` e `data/` com `__init__.py` onde couber e verificar que os diretórios existem no repo
- [x] 1.2 Adicionar `pyproject.toml` ou `requirements.txt` com yfinance, tensorflow (CPU), fastapi, uvicorn, scikit-learn, pandas, numpy, psutil, pytest e httpx, e verificar que a instalação em um venv conclui sem erro

## 2. Pipeline de dados

- [x] 2.1 Implementar coleta yfinance de PETR4.SA desde 2018-01-01 com cache em `data/raw.parquet` e verificar que a série sai ordenada por data com coluna de fechamento
- [x] 2.2 Fazer a coleta falhar de forma explícita quando a fonte está indisponível e verificar com teste que nenhuma janela é gerada nesse caso
- [x] 2.3 Implementar limpeza (drop de Close inválido) e split cronológico 70/15/15 sem shuffle e verificar com teste que as datas de treino < validação < teste
- [x] 2.4 Ajustar MinMaxScaler só no treino, aplicar nos três conjuntos e gerar janelas 60→1, verificando com testes o tamanho da janela, o alvo D+1 e que série com menos de 61 pontos não gera exemplos

## 3. LSTM, métricas e exportação

- [x] 3.1 Definir o LSTM (duas camadas + Dropout + Dense(1), entrada 60×1) e o script de treino com early stopping na validação, e verificar que o treino termina e emite uma previsão numérica para uma janela válida
- [x] 3.2 Calcular MAE, RMSE e MAPE no teste após inverter a escala e verificar que o script grava essas métricas em artefato reproduzível (ex.: `models/metrics.json`)
- [x] 3.3 Calcular as mesmas métricas da baseline naive (último Close da janela) no mesmo teste e verificar que LSTM e naive aparecem lado a lado no artefato de métricas
- [x] 3.4 Salvar `models/lstm_petr4.keras` e `models/scaler.pkl` e verificar que recarregar os dois reproduz a mesma previsão para a mesma janela

## 4. API de previsão

- [x] 4.1 Implementar FastAPI com POST `/predict` (Pydantic: exatamente 60 floats finitos) carregando modelo e scaler no startup, e verificar que 60 preços válidos retornam 200 com `ticker=PETR4.SA`, `horizon=D+1` e `predicted_close` numérico
- [x] 4.2 Rejeitar janelas com tamanho ≠ 60 ou valores não finitos com 422 e verificar com testes que a inferência não é chamada nesses casos
- [x] 4.3 Garantir que `/predict` não chama yfinance nem rede de mercado e verificar por inspeção/teste de importação que o módulo da API não depende da fonte histórica
- [x] 4.4 Mapear falha interna de inferência para 500 sem stack trace e verificar que o body de erro não contém traceback nem caminhos internos
- [x] 4.5 Confirmar que `/docs` descreve o contrato de `/predict` (janela 60 e saída D+1) abrindo a OpenAPI da API em execução

## 5. Saúde, prontidão e métricas

- [x] 5.1 Expor GET `/health` (processo no ar) e GET `/ready` (modelo e scaler carregados) e verificar 200 em ambos com artefatos presentes e `/ready` em falha quando o modelo está ausente
- [x] 5.2 Expor GET `/metrics` em Prometheus com contagem, latência de `/predict`, CPU e memória e verificar que após um predict bem-sucedido a contagem sobe e há amostra de latência, CPU e RSS

## 6. Docker e documentação de operação

- [x] 6.1 Escrever `Dockerfile` CPU-only que copia `src/api` + `models/` e sobe uvicorn sem treinar, e verificar que a imagem builda
- [x] 6.2 Escrever `compose.yaml` expondo a porta HTTP e verificar que `docker compose up` deixa `/predict`, `/health`, `/ready` e `/metrics` acessíveis
- [x] 6.3 Documentar no README: como treinar, métricas LSTM vs naive, como chamar `/predict`, `docker compose up` e o caminho de deploy em Render ou Railway, e verificar que um leitor consegue reproduzir o fluxo só com o README
