## 1. Verificação de Integridade e Artefatos da Fase 4

- [x] 1.1 Validar a integridade estrutural da change executando `openspec validate specs-fase4-credit-scoring --json` e confirmando zero erros
- [x] 1.2 Verificar conformidade dos dados brutos e divididos inspecionando `data/reference/reference.csv` e `data/production/production_raw.csv` quanto a formato e proporções do target
- [x] 1.3 Verificar conformidade do modelo baseline inspecionando `models/credit_baseline.joblib` e `models/credit_baseline_metrics.json` quanto à presença de métricas out-of-sample
- [x] 1.4 Verificar conformidade dos relatórios de observabilidade checando existência e consistência de `reports/drift_report.html`, `reports/drift_stats.csv` e `reports/drift_summary.md`

## 2. Testes Unitários e Automação da Fase 4

- [x] 2.1 Implementar testes unitários para preparação e particionamento de dados em `tests/test_credit_data.py` e verificar aprovação via `uv run pytest tests/test_credit_data.py`
- [x] 2.2 Implementar testes unitários para pipeline e inferência do modelo baseline em `tests/test_credit_baseline.py` e verificar aprovação via `uv run pytest tests/test_credit_baseline.py`
- [x] 2.3 Implementar testes unitários para simulação e cálculo estatístico de drift (PSI/KS) em `tests/test_credit_drift.py` e verificar aprovação via `uv run pytest tests/test_credit_drift.py`
- [x] 2.4 Executar a suíte de testes com `uv run pytest tests/` assegurando que tanto os novos testes de crédito quanto os testes legados continuam passando sem regressões

## 3. Sincronização e Consolidação no OpenSpec

- [x] 3.1 Sincronizar as delta specs para as especificações vigentes em `openspec/specs/` (`credit-data-pipeline`, `credit-baseline-model`, `credit-drift-monitoring` e delta de `academic-notebooks`)
- [x] 3.2 Executar `openspec validate --specs --json` para garantir que todas as especificações vigentes do repositório estão válidas e consistentes

