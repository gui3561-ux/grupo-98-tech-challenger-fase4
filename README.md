# Previsão de fechamento PETR4.SA (LSTM D+1)

Tech Challenge da Fase 4 da pós em Machine Learning (FIAP). O projeto treina um LSTM univariado no preço de fechamento de **PETR4.SA** e serve a previsão do **próximo pregão (D+1)** por uma API REST.

O usuário envia 60 fechamentos históricos. A API **não** consulta a bolsa na inferência.

## Requisitos

- Python 3.11+
- Docker (opcional, para o deploy)

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Para os notebooks acadêmicos (não entram na imagem Docker):

```bash
pip install -e ".[notebooks]"
```

## Notebooks (entrega acadêmica)

Pasta `notebooks/`. São o material de **exploração e gráficos** para o vídeo/relatório. Não substituem o treino nem a API.

| Arquivo | Papel |
|---|---|
| `notebooks/01_exploracao_petr4.ipynb` | Série PETR4.SA, limpeza e split cronológico 70/15/15 |
| `notebooks/02_treino_e_avaliacao.ipynb` | LSTM D+1, MAE/RMSE/MAPE vs naive, gráfico real vs previsto |

Como abrir (na raiz do repositório, com o venv ativo):

```bash
pip install -e ".[notebooks]"
python -m src.model.train   # se ainda não gerou models/metrics.json
jupyter notebook notebooks/01_exploracao_petr4.ipynb
```

O `Dockerfile` instala só `pip install .` — Jupyter e matplotlib **não** vão para o container da API.

## Treino

```bash
python -m src.model.train
```

O script:

1. baixa PETR4.SA desde 2018-01-01 via yfinance (cache em `data/raw.parquet`)
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

## API local (sem Docker)

Com os artefatos em `models/`:

```bash
uvicorn src.api.main:app --reload --port 8000
```

- Documentação interativa: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

### Prever D+1

```bash
curl -s http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"prices":[/* 60 fechamentos, do mais antigo ao mais recente */]}'
```

Resposta:

```json
{
  "ticker": "PETR4.SA",
  "horizon": "D+1",
  "predicted_close": 38.12
}
```

A lista `prices` deve ter **exatamente 60** números finitos. Qualquer outro tamanho, `null` ou `Infinity` retorna **422**.

Outros endpoints:

| Método | Caminho | Papel |
|---|---|---|
| GET | `/health` | processo no ar |
| GET | `/ready` | modelo e scaler carregados |
| GET | `/metrics` | Prometheus (contagem, latência, CPU, RSS) |
| GET | `/docs` | Swagger UI |

## Docker

```bash
docker compose up --build
```

A imagem sobe o uvicorn com o modelo já copiado. Não há retreino no arranque.

Depois:

- http://127.0.0.1:8000/docs
- `curl http://127.0.0.1:8000/health`
- `curl http://127.0.0.1:8000/ready`
- `curl http://127.0.0.1:8000/metrics`

## Deploy (Render ou Railway)

A mesma imagem do `Dockerfile` pode ir para a nuvem.

### Render

1. New → Web Service → conectar este repositório
2. Runtime: Docker
3. A porta 8000 já está no `EXPOSE` / CMD do Dockerfile
4. Após o deploy, use `https://<serviço>.onrender.com/docs`

### Railway

1. New Project → Deploy from GitHub
2. Railway detecta o Dockerfile
3. Expor a porta 8000 (variável `PORT` se o painel exigir: ajuste o CMD ou defina o start command `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`)

Se a cota gratuita estiver fria no dia da demo, o plano B é `docker compose up` local e gravar o vídeo em `http://127.0.0.1:8000/docs`.

## Testes

```bash
pytest
```

## Estrutura

```
src/data/       coleta yfinance, limpeza, split, scaler, janelas
src/model/      LSTM, treino, métricas, exportação
src/api/        FastAPI (sem yfinance)
notebooks/      exploração e avaliação para a banca (não vai no Docker)
models/         lstm_petr4.keras, scaler.pkl, metrics.json
```
