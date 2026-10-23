## Context

Ver `proposal.md` para a motivação da transição para a Fase 4 (Credit Scoring MLOps).
O repositório já possui código implementado para a Etapa 0 (preparação de dados), Etapa 1 (split e baseline XGBoost) e Etapa 2 (drift e Evidently) em `src/credit/`, além do notebook exploratório `notebooks/03_eda_german_credit.ipynb`. Este documento formaliza as decisões arquiteturais e técnicas dessas etapas para orientar a sustentação e evolução do sistema.

## Goals / Non-Goals

**Goals:**
- Formalizar os padrões arquiteturais de pré-processamento, modelagem e monitoramento estatístico da Fase 4.
- Assegurar isolamento entre o código da Fase 4 (`src/credit/`) e o legado da Fase 3 (`src/api/`, `src/model/`, `src/data/`), preservando reprodutibilidade de ambas as fases.
- Estabelecer a rastreabilidade entre dados gerados (`data/`), modelos serializados (`models/`) e relatórios estatísticos (`reports/`).

**Non-Goals:**
- Reescrever ou modificar a lógica de inferência da API legada da Fase 3 (PETR4).
- Implementar novas regras de negócio para as Etapas 3 (monitoramento contínuo/alertas) ou 4 (fairness/governança) nesta change.
- Alterar o arquivo `pyproject.toml` ou adicionar dependências além das já consolidadas.

## Decisions

### 1. Isolamento modular em `src/credit/`
- **Decisão:** Manter todo o código da Fase 4 no pacote `src.credit`, com submódulos `data/`, `model/` e `drift/`.
- **Justificativa:** Evita conflito com o código da Fase 3 que ainda alimenta a imagem Docker e o serviço no Render. Permite transição suave sem quebra de testes prévios.
- **Alternativa considerada:** Sobrescrever `src/model/` e `src/data/`. Descartada para não causar breaking change imediata na entrega anterior.

### 2. Pipeline Scikit-Learn com OneHotEncoder e XGBoost
- **Decisão:** Estruturar o modelo baseline usando `Pipeline([('pre', ColumnTransformer), ('clf', XGBClassifier)])`.
- **Justificativa:** O `ColumnTransformer` aplica OneHotEncoder nas 6 variáveis categóricas com `handle_unknown="ignore"` e repassa diretamente as 3 variáveis numéricas. O XGBoost lida eficazmente com interações não lineares e desbalanceamento de crédito.
- **Alternativa considerada:** Regressão Logística simples. Descartada por menor capacidade de capturar relações complexas nas faixas de crédito e poupança.

### 3. Dupla camada de observabilidade estatística (Evidently AI + PSI/KS)
- **Decisão:** Gerar relatório visual completo via Evidently (`reports/drift_report.html`) e simultaneamente uma tabela tabular de PSI/KS (`reports/drift_stats.csv`).
- **Justificativa:** O Evidently oferece diagnóstico visual aprofundado para análise exploratória e executiva. A tabela CSV com vereditos explícitos (estável, moderado, significativo) permite asserções determinísticas e consumo programático por pipelines futuros.
- **Alternativa considerada:** Utilizar unicamente o Evidently AI. Descartada porque a tabela de métricas brutas (PSI/KS) atende diretamente aos requisitos pontuais de avaliação acadêmica.

### 4. Tratamento explícito de `no_account` para dados bancários
- **Decisão:** Preencher `NaN` de `Saving accounts` e `Checking account` com o valor literal `no_account`.
- **Justificativa:** No contexto bancário do German Credit, a ausência de saldo em conta reflete que o proponente não é correntista daquela instituição, tratando-se de uma categoria econômica válida, e não de falha de coleta.
- **Alternativa considerada:** Descarte de registros ou imputação pela moda. Descartada pois causaria perda de 30%+ dos dados ou distorção da distribuição de risco.

## Risks / Trade-offs

- **[Tamanho reduzido da amostra (1.000 observações)]** → A divisão 70/30 estratificada garante que o conjunto de produção tenha 300 instâncias com 90 casos de risco (`bad`), volume estatisticamente suficiente para o teste KS e cálculo de PSI por faixas quantílicas.
- **[Disponibilidade do dataset externo UCI]** → A rotina de montagem do dataset inclui mecanismo de fallback para download HTTP direto caso a biblioteca `ucimlrepo` enfrente instabilidade.
- **[Avaliação justa de Concept Drift]** → O benchmark de referência para comparação com a produção utiliza a acurácia e o ROC-AUC obtidos na partição de *holdout* da referência (out-of-sample), evitando métricas infladas por overfitting in-sample.

