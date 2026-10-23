# credit-baseline-model Specification

## Purpose

Treina, avalia e serializa o modelo baseline de classificação de risco de crédito treinado no conjunto de referência para servir de referencial de desempenho e detecção de concept drift.

## Requirements

### Requirement: Pipeline supervisionado de classificação de crédito
O sistema SHALL estruturar um pipeline composto por codificação categórica One-Hot (ignorando categorias desconhecidas em inferência), repasse direto de atributos numéricos e estimador XGBoost para classificar clientes em risco bom (`good`) ou mau (`bad`).

#### Scenario: Ajuste do pipeline sobre o conjunto de referência
- **WHEN** o pipeline de treino é alimentado com as variáveis preditoras numéricas e categóricas do conjunto de referência
- **THEN** o pipeline produz predições probabilísticas e rótulos discretos sem vazamento entre partições

### Requirement: Avaliação com métricas orientadas à classe positiva
O sistema SHALL calcular métricas de ROC-AUC, acurácia e F1-score atribuindo a classe minoritária e de maior risco financeiro (`bad`) como classe positiva (`pos_label=1`).

#### Scenario: Cálculo de métricas em holdout estratificado
- **WHEN** o modelo baseline é avaliado em holdout de 25% extraído do conjunto de referência
- **THEN** o sistema reporta ROC-AUC, acurácia global e relatório de classificação completo por classe

### Requirement: Persistência serializada de modelo e métricas
O sistema SHALL salvar o pipeline ajustado no dataset completo de referência e o relatório de métricas obtidas na partição de holdout em caminhos de arquivo padronizados.

#### Scenario: Gravação dos artefatos de modelo em disco
- **WHEN** o treinamento do baseline for concluído com sucesso
- **THEN** o arquivo de estimador `models/credit_baseline.joblib` e o arquivo JSON `models/credit_baseline_metrics.json` são atualizados no diretório de modelos

