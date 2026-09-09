# Previsão de fechamento PETR4.SA (LSTM D+1)

Tech Challenge da Fase 4 da pós em Machine Learning ([FIAP](https://github.com/gui3561-ux/grupo-98-tech-challenger-fase4)). **Grupo 98.**

O projeto treina um LSTM univariado no fechamento de **PETR4.SA** e serve a previsão do **próximo pregão (D+1)** por uma API REST. O enunciado usa `DIS` só como exemplo de `yfinance`; a ação é de livre escolha. O usuário envia 60 fechamentos históricos. A API **não** consulta a bolsa na inferência.

## Entregáveis da fase

| Item do enunciado | Estado neste repositório |
|---|---|
| Código + documentação | este README, código em `src/`, notebooks em `notebooks/` |
| Docker da API | `Dockerfile` + `compose.yaml` |
| Vídeo da API | gravar em `http://127.0.0.1:8000/docs` (Swagger: POST `/predict`) |
| Link da API em nuvem | **ainda não há URL pública**; a demo oficial é local (`docker compose up --build`) |

## O que vem no clone

| Caminho | No Git? | Para quê |
|---|---|---|
| `models/lstm_petr4.keras`, `scaler.pkl`, `metrics.json` | sim | a API sobe **sem retreinar** |
| `examples/predict_payload.json` | sim | `curl` de `/predict` copiável |
| `data/raw.parquet` | **não** (`.gitignore`) | cache local do yfinance |

Depois do clone, `docker compose` ou `uvicorn` já servem o modelo versionado. `python -m src.model.train` e os notebooks baixam PETR4.SA via yfinance se o cache não existir.

## Ambiente

- Python 3.11+
- Docker (para a demo e o deploy)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Caminho rápido (Docker)

Com os artefatos já no repositório, não há retreino no arranque:

```bash
docker compose up --build
```

- Swagger: http://127.0.0.1:8000/docs
- `curl http://127.0.0.1:8000/health`
- `curl http://127.0.0.1:8000/ready`

## Prever D+1 e ver monitoramento

A janela de exemplo (60 pregões, do mais antigo ao mais recente) está em `examples/predict_payload.json`.

```bash
curl -s http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  --data-binary @examples/predict_payload.json
```

Resposta do modelo persistido neste repositório:

```json
{
  "ticker": "PETR4.SA",
  "horizon": "D+1",
  "predicted_close": 40.99992294849494
}
```

A lista `prices` deve ter **exatamente 60** números finitos. Qualquer outro tamanho, `null` ou `Infinity` retorna **422**.

Em seguida, métricas de produção (contagem de previsões, latência, CPU e memória RSS):

```bash
curl -s http://127.0.0.1:8000/metrics
```

Procure `predict_requests_total`, `predict_latency_seconds_sum`, `process_cpu_seconds_total` e `process_resident_memory_bytes`. Esse endpoint é o monitoramento pedido no enunciado (tempo de resposta e uso de recursos).

Outros endpoints:

| Método | Caminho | Papel |
|---|---|---|
| GET | `/health` | processo no ar |
| GET | `/ready` | modelo e scaler carregados |
| GET | `/metrics` | Prometheus (contagem, latência, CPU, RSS) |
| GET | `/docs` | Swagger UI (roteiro do vídeo) |
| POST | `/predict` | previsão D+1 |

### API local (sem Docker)

```bash
uvicorn src.api.main:app --reload --port 8000
```

OpenAPI: http://127.0.0.1:8000/openapi.json

## Treino

Só é necessário para retreinar ou para os notebooks quando `models/metrics.json` ainda não existe. Sem `data/raw.parquet`, o script baixa a série.

```bash
python -m src.model.train
```

O script:

1. baixa PETR4.SA desde 2018-01-01 via yfinance (cache em `data/raw.parquet`, fora do Git)
2. limpa a série, faz split cronológico 70/15/15 **sem shuffle**
3. ajusta `MinMaxScaler` só no treino
4. monta janelas de 60 pregões → alvo D+1
5. treina o LSTM (duas camadas + Dropout + Dense(1)) com early stopping
6. grava `models/lstm_petr4.keras`, `models/scaler.pkl` e `models/metrics.json`

### Métricas (teste, em R$)

Valores gerados pelo último treino (`models/metrics.json`), no conjunto de teste, após inverter o scaler:

| Modelo | MAE | RMSE | MAPE |
|---|---|---|---|
| LSTM | 2.28 | 3.00 | 5.68% |
| Naive (amanhã = hoje) | 0.48 | 0.64 | 1.26% |

A baseline naive ganhou. Isso é esperado em preço absoluto: o fechamento de D+1 está muito próximo do de D, e o LSTM acaba suavizando em vez de copiar o último valor. O trabalho documenta essa comparação em vez de escondê-la.

## Notebooks (entrega acadêmica)

Pasta `notebooks/`. São o material de **exploração e gráficos** para o vídeo/relatório. Não substituem o treino nem a API.

| Arquivo | Papel |
|---|---|
| `notebooks/01_exploracao_petr4.ipynb` | Série PETR4.SA, limpeza e split cronológico 70/15/15 |
| `notebooks/02_treino_e_avaliacao.ipynb` | LSTM D+1, MAE/RMSE/MAPE vs naive, gráfico real vs previsto |

Como abrir (na raiz do repositório, com o venv ativo):

```bash
pip install -e ".[notebooks]"
python -m src.model.train   # se ainda não gerou models/metrics.json; baixa yfinance sem cache
jupyter notebook notebooks/01_exploracao_petr4.ipynb
```

O `Dockerfile` instala só `pip install .` — Jupyter e matplotlib **não** vão para o container da API.

## Deploy (Render ou Railway)

A mesma imagem do `Dockerfile` pode ir para a nuvem. **Ainda não há URL pública neste repositório.**

### Render

1. New → Web Service → conectar este repositório
2. Runtime: Docker
3. A porta 8000 já está no `EXPOSE` / CMD do Dockerfile
4. Após o deploy, use `https://<serviço>.onrender.com/docs`

### Railway

1. New Project → Deploy from GitHub
2. Railway detecta o Dockerfile
3. Expor a porta 8000 (variável `PORT` se o painel exigir: ajuste o CMD ou defina o start command `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`)

Se a cota gratuita estiver fria no dia da demo, grave o vídeo em `http://127.0.0.1:8000/docs` com `docker compose up`.

## Testes

```bash
pytest
```

## Estrutura

```
src/data/       coleta yfinance, limpeza, split, scaler, janelas
src/model/      LSTM, treino, métricas, exportação
src/api/        FastAPI (sem yfinance)
tests/          pytest da coleta, do LSTM e da API
notebooks/      exploração e avaliação para a banca (não vai no Docker)
models/         lstm_petr4.keras, scaler.pkl, metrics.json (versionados)
examples/       predict_payload.json (60 fechamentos para o curl)
Dockerfile      imagem da API
compose.yaml    docker compose na porta 8000
```
