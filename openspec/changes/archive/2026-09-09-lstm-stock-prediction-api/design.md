## Context

Repositório greenfield, sem código de modelo nem API. A motivação está em `proposal.md`. As exigências observáveis estão nas specs `stock-data-pipeline`, `lstm-forecast`, `prediction-api` e `production-ops`.

Restrições que moldam o desenho:

- Inferência stateless: o cliente envia a janela; a API não consulta a bolsa no `/predict`.
- Horizonte único D+1, Close univariado, janela de 60 pregões.
- Entrega acadêmica precisa de Docker e de evidência de monitoramento, sem exigir Kubernetes.
- Imagem precisa caber em nuvem gratuita/barata (CPU only).

## Goals / Non-Goals

**Goals:**

- Separar treino (script offline) de serviço (API que só carrega artefatos).
- Garantir que a mesma escala do treino seja aplicada na inferência.
- Deixar a API demonstrável via OpenAPI e `docker compose up`.

**Non-Goals:**

- Frontend, autenticação e banco de dados.
- Retreino contínuo ou job agendado.
- Previsão multi-step ou múltiplos tickers no mesmo modelo.
- Orquestração (Kubernetes) e observabilidade com stack completa (Grafana obrigatório).

## Decisions

### 1. FastAPI em vez de Flask

FastAPI gera OpenAPI/Swagger sem trabalho extra (útil no vídeo) e valida o body com Pydantic (tamanho 60, valores finitos). Flask atenderia o enunciado, mas exigiria schema e docs manuais.

### 2. Keras/TensorFlow CPU em vez de PyTorch

O fluxo treinar → `model.keras` → carregar na API é direto. A imagem usa TensorFlow CPU-only para reduzir tamanho. PyTorch seria equivalente em qualidade; o custo está na operação da entrega, não na métrica.

### 3. yfinance só no pipeline de treino

Coleta e janelas vivem em `src/data`. A API não importa yfinance. Assim o `/predict` continua válido se o Yahoo estiver fora do ar (spec `prediction-api`).

### 4. Split temporal 70/15/15 e MinMaxScaler no treino

Ordem cronológica, sem shuffle. O scaler é ajustado só no treino e persistido em `models/scaler.pkl` junto de `models/lstm_petr4.keras`. Alternativa: StandardScaler; MinMax é o padrão didático para preço e facilita a inversão para MAE/RMSE/MAPE em reais.

### 5. Arquitetura LSTM pequena e baseline naive

Duas camadas LSTM com Dropout e `Dense(1)` bastam para o enunciado. A baseline “D+1 = último Close da janela” é calculada no mesmo teste para evitar vender persistência como inteligência.

Hiperparâmetros (unidades, dropout, epochs, early stopping) ficam no script de treino e podem ser ajustados sem mudar specs, desde que a entrada continue 60×1 e a saída 1.

### 6. Contrato HTTP mínimo

| Método | Caminho | Papel |
|---|---|---|
| POST | `/predict` | Body `{ "prices": [float × 60] }` → `{ "ticker": "PETR4.SA", "horizon": "D+1", "predicted_close": number }` |
| GET | `/health` | Processo no ar |
| GET | `/ready` | Modelo e scaler carregados |
| GET | `/metrics` | Contagem, latência, CPU e memória |
| GET | `/docs` | OpenAPI |

Erros de validação: 422. Falha interna de inferência: 500 sem stack trace.

### 7. Layout do repositório

```
src/data/       coleta yfinance, limpeza, split, janelas, scaler
src/model/      definicao LSTM, treino, metricas, export
src/api/        FastAPI, carga dos artefatos, metricas
models/         lstm_petr4.keras + scaler.pkl (commitados apos o treino)
Dockerfile
compose.yaml
```

Treino é um módulo/`python -m` offline. A imagem de runtime copia `src/api` + `models/` e sobe uvicorn. Não retreina no boot.

### 8. Docker + métricas simples

`Dockerfile` multi-stage se o tamanho exigir; senão uma imagem CPU-only. `compose.yaml` publica a porta da API.

Métricas em formato Prometheus no `/metrics` (latência de `/predict`, `http_requests_total`, CPU e RSS via psutil). Alternativa considerada: JSON ad hoc; Prometheus facilita colar no vídeo e em qualquer scraper.

### 9. Deploy em nuvem com a mesma imagem

Render ou Railway com o Dockerfile do repo. A escolha do provedor é operacional e pode mudar sem alterar specs. O README documenta o comando local (`docker compose up`) como plano B do vídeo.

## Risks / Trade-offs

- [LSTM em preço absoluto tende a copiar o último Close] → Mitigação: reportar baseline naive nas mesmas métricas e discutir o resultado no README.
- [yfinance instável ou com rate limit] → Mitigação: cache local da série no treino (`data/raw.parquet`); API não depende da fonte.
- [Imagem TensorFlow pesada / cota de nuvem] → Mitigação: CPU-only, compose local para a demo, evitar GPU.
- [Vazamento temporal se alguém shuffle] → Mitigação: split e janelas só por data; testes cobrindo a ordem dos conjuntos.
- [Modelo não commitado quebra o Docker] → Mitigação: artefatos em `models/` versionados após o primeiro treino bem-sucedido.

## Migration Plan

1. Implementar pipeline e treinar localmente até gerar `models/`.
2. Subir API local apontando para esses artefatos.
3. Empacotar a imagem e validar `/predict`, `/ready` e `/metrics`.
4. Publicar a mesma imagem na nuvem.
5. Rollback: voltar à imagem anterior; a API é stateless, não há migração de dados.

## Open Questions

- Qual provedor de nuvem usar na entrega (Render vs Railway) — não altera contrato nem tarefas além do README de deploy.
- Dimensões exatas das camadas LSTM — ajuste de hiperparâmetro no treino, sem mudar o contrato 60 → 1.
