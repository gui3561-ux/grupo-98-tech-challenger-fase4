# credit-drift-monitoring Specification

## Purpose

Simula a passagem do tempo e cenários macroeconômicos adversos em produção, aplicando testes de hipótese e gerando relatórios de Data Drift e Concept Drift.

## Requirements

### Requirement: Simulação controlada de degradação em produção
O sistema SHALL criar o dataset de produção injetando alterações determinísticas na distribuição de variáveis críticas: aumento inflacionário com ruído em `Credit amount`, redução média de idade em `Age` e reamostragem simulando recessão com menor liquidez em `Checking account`.

#### Scenario: Injeção de drift preservando semente determinística
- **WHEN** a rotina de simulação de drift processa o dataset de produção-base
- **THEN** o sistema grava `data/production/production.csv` com distribuições estatisticamente deslocadas para `Credit amount`, `Age` e `Checking account`

### Requirement: Cálculo de estatísticas de estabilidade populacional
O sistema SHALL calcular o Population Stability Index (PSI) para todas as variáveis preditoras e o teste bicaudal de Kolmogorov-Smirnov (KS) para as variáveis numéricas, classificando a estabilidade em faixas estável (< 0.10), moderada (0.10–0.25) e significativa (> 0.25).

#### Scenario: Avaliação de estabilidade por feature
- **WHEN** os dados de referência e produção são comparados
- **THEN** o sistema exporta `reports/drift_stats.csv` com colunas de feature, tipo, PSI, veredito de estabilidade e p-valor do teste KS

### Requirement: Geração de relatórios com Evidently AI e sumário de concept drift
O sistema SHALL gerar um relatório visual HTML utilizando os presets de Data Drift e Classificação da biblioteca Evidently, além de um sumário em Markdown contrastando o ROC-AUC e acurácia de holdout da referência com o desempenho observado em produção.

#### Scenario: Exportação do relatório visual e sumário executivo
- **WHEN** o orquestrador de relatórios de drift é executado com as predições de referência e produção
- **THEN** são gerados os arquivos `reports/drift_report.html` com os dashboards interativos e `reports/drift_summary.md` documentando o declínio de desempenho decorrente do drift

