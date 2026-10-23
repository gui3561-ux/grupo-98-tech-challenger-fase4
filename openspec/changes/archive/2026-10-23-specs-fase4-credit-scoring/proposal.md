## Why

O projeto transitou da Fase 3 (série temporal LSTM de PETR4.SA) para a Fase 4 do Tech Challenge FIAP (camada de sustentação e confiabilidade de Credit Scoring em MLOps). Embora as Etapas 0, 1 e 2 já possuam código funcional em `src/credit/` e análise em `notebooks/03_eda_german_credit.ipynb`, as especificações formais no OpenSpec ainda refletem exclusivamente a Fase 3. Formalizar essas capacidades é necessário para consolidar o comportamento vigente, garantir rastreabilidade dos requisitos e viabilizar o desenvolvimento seguro das etapas subsequentes (Etapa 3 - monitoramento contínuo/alertas e Etapa 4 - governança e conformidade).

## What Changes

- Criação da especificação de pipeline de dados de crédito (`credit-data-pipeline`), formalizando a recuperação do target `Risk` via UCI id=144, tratamento de categorias legítimas sem conta (`no_account`) e divisão estratificada Referência × Produção.
- Criação da especificação do modelo baseline (`credit-baseline-model`), cobrindo o pipeline de pré-processamento com OneHotEncoder e XGBoost, avaliação de desempenho com foco na classe positiva/minoritária (`bad`), e persistência serializada do estimador e métricas.
- Criação da especificação de monitoramento e simulação de drift (`credit-drift-monitoring`), cobrindo a injeção determinística de anomalias (inflação em `Credit amount`, clientes mais jovens em `Age`, recessão em `Checking account`), testes estatísticos por feature via PSI e Kolmogorov-Smirnov (KS), e geração de relatórios Evidently AI e sumário de Concept Drift.
- Atualização da especificação `academic-notebooks` para incorporar requisitos do notebook `notebooks/03_eda_german_credit.ipynb` referente a análise exploratória, desbalanceamento de classes, levantamento de atributos sensíveis/PII (LGPD) e validação gráfica do drift.

## Capabilities

### New Capabilities
- `credit-data-pipeline`: Preparação do dataset base de crédito, tratamento de valores categóricos sem conta e particionamento estratificado entre ambiente de referência e produção.
- `credit-baseline-model`: Pipeline de classificação binária de risco de crédito com XGBoost, métricas focadas na classe inadimplente e exportação de artefatos.
- `credit-drift-monitoring`: Simulação controlada de degradação em produção, cálculo de estabilidade populacional (PSI/KS) e emissão de relatórios de Data Drift e Concept Drift com Evidently AI.

### Modified Capabilities
- `academic-notebooks`: Incorpora os requisitos e cenários analíticos do notebook `03_eda_german_credit.ipynb` para documentação da exploração de crédito e viés/fairness.

## Impact

- Sistema de especificações do OpenSpec atualizado e aderente ao escopo da Fase 4.
- Permite criação direcionada de testes unitários em `tests/` para o módulo `src/credit/`.
- Não altera contratos de execução pública existentes; preserva as dependências e o extra `legacy` da Fase 3.

