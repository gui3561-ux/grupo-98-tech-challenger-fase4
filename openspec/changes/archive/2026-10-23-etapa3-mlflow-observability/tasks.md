## 1. Módulo de Observabilidade e Dependências

- [x] 1.1 Adicionar dependência `mlflow` ao projeto e instalar no ambiente virtual com `uv`
- [x] 1.2 Implementar `src/credit/observability.py` com configuração de logger estruturado e funções auxiliares de rastreamento do MLflow
- [x] 1.3 Adicionar `.mlruns/` e `mlflow.db` ao `.gitignore` para manter o versionamento limpo

## 2. Orquestrador de Pipeline Integrado

- [x] 2.1 Implementar `src/credit/pipeline.py` orquestrando o fluxo completo dentro de uma run do MLflow (Pandera -> Split -> Baseline -> Drift -> Evidently)
- [x] 2.2 Coletar e registrar métricas operacionais (latências, volume de registros, alertas de drift) e persistir o relatório HTML como artefato

## 3. Testes Automatizados e Execução da Etapa 3

- [x] 3.1 Implementar testes unitários em `tests/test_credit_observability.py` cobrindo o logger estruturado e a extração de métricas de saúde
- [x] 3.2 Executar `uv run python -m src.credit.pipeline` comprovando a execução integrada de ponta a ponta e a criação da run no MLflow
- [x] 3.3 Executar a suíte de testes `uv run pytest tests/` assegurando que todas as rotinas passam sem falhas

