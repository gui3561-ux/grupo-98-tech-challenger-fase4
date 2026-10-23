## Purpose

Centraliza logs operacionais de ingestão, transformação e qualidade, registrando experimentos, métricas de saúde e artefatos de drift no MLflow.

## ADDED Requirements

### Requirement: Rastreamento centralizado do ciclo de vida com MLflow
O sistema SHALL registrar as execuções do pipeline em um servidor/repositório local de tracking do MLflow, catalogando hiperparâmetros do baseline, métricas de holdout (ROC-AUC, acurácia, F1), métricas estatísticas de drift (PSI por feature e p-valores de KS) e salvando artefatos gerados.

#### Scenario: Execução completa registra parâmetros, métricas e artefatos
- **WHEN** o orquestrador do pipeline de crédito é executado de ponta a ponta
- **THEN** uma nova run é aberta no MLflow contendo parâmetros do modelo, métricas de avaliação, status do contrato de dados e métricas de estabilidade de produção

#### Scenario: Relatório interativo do Evidently é salvo como artefato da run
- **WHEN** o relatório de drift em formato HTML for gerado
- **THEN** o arquivo `reports/drift_report.html` é persistido como artefato na run correspondente do MLflow para consulta visual no dashboard

### Requirement: Centralização de logs operacionais e métricas de saúde
O sistema SHALL emitir logs estruturados e padronizados registrando o status de cada etapa do pipeline (tempo de execução, contagem de registros processados, falhas de ingestão) e registrar métricas de saúde operacional e quantidade de variáveis em alerta de drift significativo.

#### Scenario: Logs estruturados registram cada fase do pipeline
- **WHEN** o pipeline executa as etapas de validação Pandera, divisão, treinamento e monitoramento
- **THEN** cada estágio emite logs estruturados com carimbo de tempo, nível de severidade e duração em segundos

#### Scenario: Alertas de drift disparam indicadores operacionais
- **WHEN** o cálculo de PSI identificar features com mudança de distribuição acima do limiar crítico (PSI >= 0.25)
- **THEN** o sistema registra a contagem total de variáveis sob alerta como métrica operacional da run para visibilidade no painel

