# Previsão de fechamento PETR4.SA (LSTM D+1)

Tech Challenge da Fase 4 da pós em Machine Learning (FIAP). **Grupo 98.**

Repositório: https://github.com/gui3561-ux/grupo-98-tech-challenger-fase4

| RM | Integrante |
|---|---|
| RM371323 | Guilherme Ramos Couceiro |
| RM372947 | Lucas Ribeiro Pestana |
| RM373551 | Sávio Aparecido Crispim |
| RM373555 | Wesley Oliveira |
| RM373529 | Cristiano Santos de Oliveira |

O projeto treina um LSTM univariado no fechamento de **PETR4.SA** e serve a previsão do **próximo pregão (D+1)** por uma API REST. O enunciado usa `DIS` só como exemplo de `yfinance`; a ação é de livre escolha. O usuário envia 60 fechamentos históricos. A API **não** consulta a bolsa na inferência.

## Entregáveis da fase

| Item do enunciado | Estado neste repositório |
|---|---|
| Código + documentação | este README, código em `src/`, notebooks em `notebooks/` |
| Docker da API | `Dockerfile` + `compose.yaml` |
| Vídeo da API | será gravado **depois por um integrante**, no Swagger (`POST /predict` em `/docs`) — nuvem ou `http://127.0.0.1:8000/docs` |
| Link da API em nuvem | **Render Hobby**: https://grupo-98-tech-challenger-fase4.onrender.com (`/docs`, `/health`) |

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

O último close dessa janela está perto de **R$ 48**. O LSTM devolve ~**41** porque suaviza a série em vez de copiar o valor de hoje — o mesmo efeito que faz a naive ganhar nas métricas abaixo. Não é bug da API.

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
5. treina o LSTM (64 e 32 unidades, dropout 0.2, batch 32, até 40 épocas, early stopping em `val_loss` com patience 5)
6. grava `models/lstm_petr4.keras`, `models/scaler.pkl` e `models/metrics.json`

O recorte acima é o artefato em `models/`. Alternativas consideradas (rede 32/16; dropout 0.4) e o critério de escolha estão no notebook `02`. O treino oficial **não** é o notebook.

### Métricas (teste, em R$)

Valores gerados pelo último treino (`models/metrics.json`), no conjunto de teste, após inverter o scaler:

| Modelo | MAE | RMSE | MAPE |
|---|---|---|---|
| LSTM | 2.28 | 3.00 | 5.68% |
| Naive (amanhã = hoje) | 0.48 | 0.64 | 1.26% |

A baseline naive ganhou. Em preço absoluto isso é esperado: o fechamento de D+1 quase sempre está colado no de D, e o LSTM suaviza (daí ~41 vs ~48 no exemplo do `/predict`). O trabalho documenta a comparação em vez de escondê-la. **Não retreine só para “ganhar” da naive** — isso não muda o fato de o alvo ser o Close em reais.

## Notebooks (entrega acadêmica)

Pasta `notebooks/`. São o material de **exploração e gráficos** para o vídeo/relatório. Não substituem o treino nem a API.

| Arquivo | Papel |
|---|---|
| `notebooks/01_exploracao_petr4.ipynb` | Série PETR4.SA, limpeza e split cronológico 70/15/15 |
| `notebooks/02_treino_e_avaliacao.ipynb` | LSTM D+1, hiperparâmetros, MAE/RMSE/MAPE vs naive, gráfico real vs previsto |

Como abrir (na raiz do repositório, com o venv ativo):

```bash
pip install -e ".[notebooks]"
python -m src.model.train   # se ainda não gerou models/metrics.json; baixa yfinance sem cache
jupyter notebook notebooks/01_exploracao_petr4.ipynb
```

O `Dockerfile` instala só `pip install .` — Jupyter e matplotlib **não** vão para o container da API.

## Deploy (Render)

Alvo de nuvem da entrega: **Render Hobby**, com a mesma imagem do `Dockerfile`.

| Recurso | URL |
|---|---|
| API | https://grupo-98-tech-challenger-fase4.onrender.com |
| Swagger | https://grupo-98-tech-challenger-fase4.onrender.com/docs |
| Health | https://grupo-98-tech-challenger-fase4.onrender.com/health |

Arquivo `render.yaml` na raiz: Web Service Docker e health check em `/health`. A imagem escuta `PORT` (Render define; local sem `PORT` continua 8000). O compute permanece no Hobby (`free` ou Starter 512 MB). **Não** subir para Standard/Pro.

O Hobby pode **dormir** depois de ocioso. Antes da demo, chame `GET /health` e espere o 200 (o primeiro hit pode demorar um minuto). Se a instância estiver suspensa, use o fallback local:

```bash
docker compose up --build
```

Swagger local: http://127.0.0.1:8000/docs

Passos no painel (ou Blueprint com o `render.yaml`), se for preciso recriar o serviço:

1. New → Web Service → conectar este repositório GitHub
2. Runtime: **Docker** (o Render usa o `Dockerfile`)
3. Health check: `/health`
4. Compute: Hobby (`free` ou `starter`); não escolher Standard/Pro
5. Não é preciso retreinar: o modelo já vai na imagem

### Railway (alternativa)

1. New Project → Deploy from GitHub
2. Railway detecta o Dockerfile
3. A variável `PORT` já é lida pelo `CMD` da imagem

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
Dockerfile      imagem da API (PORT ou 8000)
compose.yaml    docker compose na porta 8000
render.yaml     Blueprint Render (Docker + /health)
```
