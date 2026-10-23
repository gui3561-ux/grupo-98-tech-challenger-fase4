## Why

A Etapa 3 do Tech Challenge (Fase 4), correspondente a 20% da nota, exige a observabilidade operacional de pipelines e modelos de crédito. Ela demanda a centralização de logs e métricas de execução (sucessos/falhas na ingestão, validação de contratos e detecção de drift) e a implementação de rastreamento com **MLflow** (ou dashboard equivalente), documentando métricas de saúde operacional (latência, volume de dados e alertas de degradação). Atualmente, os scripts do projeto rodam de maneira isolada sem uma ferramenta de tracking que registre parâmetros, métricas e artefatos em uma interface unificada de MLOps.

## What Changes

- Adição da biblioteca `mlflow` para rastreamento local de experimentos e ciclo de vida do modelo.
- Criação do módulo de observabilidade e logging estruturado em `src/credit/observability.py`, centralizando eventos de pipeline, tempos de execução de cada estágio e alertas emitidos por testes de drift.
- Criação do orquestrador de ponta a ponta `src/credit/pipeline.py`, que executa a esteira completa em uma run do MLflow:
  1. Validação dos dados brutos com contrato Pandera;
  2. Particionamento e carga de datasets;
  3. Treinamento e registro dos parâmetros/métricas do modelo baseline XGBoost;
  4. Simulação de drift em produção;
  5. Cálculo estatístico (PSI e KS) e geração do relatório Evidently AI;
  6. Registro no MLflow de métricas de estabilidade populacional, alertas de anomalia e do arquivo HTML interativo como artefato da run.
- Documentação formal e disponibilização da UI interativa do MLflow (`mlflow ui`).

## Capabilities

### New Capabilities
- `credit-pipeline-observability`: Centralização de logs estruturados, monitoramento de métricas operacionais e rastreamento de experimentos com MLflow.

### Modified Capabilities
<!-- Nenhuma especificação anterior alterada estruturalmente -->

## Impact

- Dependência `mlflow` adicionada ao projeto para tracking reproduzível.
- Disponibiliza um orquestrador unificado (`uv run python -m src.credit.pipeline`) e acesso a dashboard visual via `uv run mlflow ui`.
- Conclui os 20% da nota correspondentes à Etapa 3 do Tech Challenge.

