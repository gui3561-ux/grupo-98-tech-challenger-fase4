# Relatório de Drift — Etapa 2

Comparação entre o **Dataset de Referência** (treino do baseline) e o 
**Dataset de Produção** (com degradação injetada simulando a passagem do tempo).

## Data Drift (mudança de distribuição das features)

Features com drift **significativo** (PSI ≥ 0.25): `Age`, `Credit amount`

PSI/KS por feature (detalhe em `drift_stats.csv`):

| feature | type | psi | psi_verdict | ks_statistic | ks_pvalue | ks_drift |
|---|---|---|---|---|---|---|
| Age | numeric | 1.1062 | significativo | 0.4129 | 0.0 | True |
| Credit amount | numeric | 0.415 | significativo | 0.2595 | 0.0 | True |
| Checking account | categorical | 0.11 | moderado |  |  |  |
| Duration | numeric | 0.039 | estável | 0.0324 | 0.975546 | False |
| Saving accounts | categorical | 0.0324 | estável |  |  |  |
| Purpose | categorical | 0.0253 | estável |  |  |  |
| Job | categorical | 0.0074 | estável |  |  |  |
| Housing | categorical | 0.0027 | estável |  |  |  |
| Sex | categorical | 0.0009 | estável |  |  |  |

## Concept Drift (degradação do modelo)

Referência = performance de **holdout** (out-of-sample) do treino; Produção = mesmo modelo sobre o dataset com drift (labels reais preservados).

| Métrica | Referência (holdout) | Produção | Queda |
|---|---|---|---|
| ROC-AUC | 0.7631 | 0.5623 | 0.2008 |
| Accuracy | 0.7257 | 0.6467 | 0.079 |

> O relatório visual completo do Evidently está em `drift_report.html`.
