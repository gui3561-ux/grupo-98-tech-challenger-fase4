## Context

Ver `proposal.md` para motivação.
O repositório já possui componentes funcionais para validação de dados (Pandera), modelagem (XGBoost) e cálculo de drift (PSI/KS e Evidently). A Etapa 3 exige a unificação operacional desses estágios, centralização de logs e integração com uma ferramenta de rastreamento de experimentos (MLflow) com visualização em dashboard.

## Goals / Non-Goals

**Goals:**
- Configurar o MLflow para rastreamento de ciclo de vida e experimentos em armazenamento local (`./mlruns`).
- Criar o módulo `src/credit/observability.py` com logging estruturado e integração de métricas de saúde operacional (latência por etapa, volume de amostras, alertas).
- Criar o orquestrador unificado `src/credit/pipeline.py` para executar a esteira ponta a ponta vinculada a uma run do MLflow.
- Anexar relatórios estáticos (`reports/drift_report.html` e `models/credit_baseline_metrics.json`) como artefatos rastreáveis na run.

**Non-Goals:**
- Provisionar infraestruturas pagas de observabilidade externa (Datadog ou provedores de nuvem que exijam chaves pagas).
- Modificar os contratos de dados já consolidados na Etapa 1.

## Decisions

### 1. MLflow local via `./mlruns`
- **Decisão:** Utilizar o tracking backend local padrão do MLflow apontando para a pasta `./mlruns`.
- **Justificativa:** Não exige provisionamento de bancos relacionais adicionais ou dependências em nuvem; permite reprodutibilidade imediata no ambiente local e inicialização visual pelo comando `uv run mlflow ui`.
- **Alternativa considerada:** Datadog ou Grafana Cloud. Descartada por exigir contas corporativas e credenciais sensíveis no ambiente.

### 2. Orquestrador único `src/credit/pipeline.py`
- **Decisão:** Criar um ponto único de entrada para execução completa de sustentação e confiabilidade.
- **Justificativa:** Agrupa as etapas de validação por contrato (Pandera), split, baseline, injeção de drift e Evidently dentro de um único contexto de run (`with mlflow.start_run()`), garantindo rastreabilidade cronológica dos parâmetros às métricas de drift.

### 3. Log explícito de alertas e métricas de saúde
- **Decisão:** Calcular e logar métricas operacionais dedicadas:
  - `latency_validation_seconds`, `latency_training_seconds`, `latency_drift_seconds`;
  - `processed_rows_reference`, `processed_rows_production`;
  - `drift_critical_alerts_count` (contagem de variáveis com PSI >= 0.25).
- **Justificativa:** Cumpre diretamente a exigência de "Métricas de Saúde Operacionais" detalhada no enunciado da disciplina.

## Risks / Trade-offs

- **[Tamanho do artefato HTML do Evidently]** → O relatório do Evidently tem ~4MB. Salvar como artefato no MLflow local é suportado perfeitamente sem impactar o tempo de inferência ou causar overhead significativo.
- **[Concorrência de logs]** → O módulo de logging utilizará formatters estruturados padrão do Python (`logging.getLogger("credit_pipeline")`), garantindo saída clara em console e persistência em arquivo de log operacional.

