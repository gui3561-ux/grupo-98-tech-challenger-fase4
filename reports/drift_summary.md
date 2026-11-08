# Relatório de Drift — Etapa 2

Comparação entre o **Dataset de Referência** (treino do baseline) e o 
**Dataset de Produção** (com degradação injetada simulando a passagem do tempo).

## Data Drift (mudança de distribuição das features)

Features com drift **significativo** (PSI ≥ 0.25): `Age`, `Credit amount`

PSI/KS por feature (detalhe em `drift_stats.csv`):

| feature | type | psi | psi_verdict | ks_statistic | ks_pvalue | ks_drift |
|---|---|---|---|---|---|---|
| Age | numeric | 1.0821 | significativo | 0.4189 | 0.0 | True |
| Credit amount | numeric | 0.4531 | significativo | 0.267 | 0.0 | True |
| Checking account | categorical | 0.1413 | moderado |  |  |  |
| Duration | numeric | 0.0637 | estável | 0.0398 | 0.069933 | False |
| Purpose | categorical | 0.0341 | estável |  |  |  |
| Saving accounts | categorical | 0.0321 | estável |  |  |  |
| Job | categorical | 0.0037 | estável |  |  |  |
| Housing | categorical | 0.0031 | estável |  |  |  |
| Sex | categorical | 0.0004 | estável |  |  |  |

## Concept Drift (degradação do modelo)

Referência = performance de **holdout** (out-of-sample) do treino; Produção = mesmo modelo sobre o dataset com drift (labels reais preservados).

| Métrica | Referência (holdout) | Produção | Queda |
|---|---|---|---|
| ROC-AUC | 0.8528 | 0.5757 | 0.2771 |
| Accuracy | 0.7851 | 0.6327 | 0.1524 |

> O relatório visual completo do Evidently está em `drift_report.html`.
