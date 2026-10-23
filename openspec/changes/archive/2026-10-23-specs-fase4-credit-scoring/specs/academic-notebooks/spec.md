## ADDED Requirements

### Requirement: Notebook de exploração de crédito e governança
O repositório SHALL incluir um notebook acadêmico (`notebooks/03_eda_german_credit.ipynb`) dedicado à exploração dos dados de crédito, desbalanceamento de classes, levantamento de atributos sensíveis (LGPD) e prévia visual do drift.

#### Scenario: Análise de estrutura e desbalanceamento do target
- **WHEN** o notebook de exploração de crédito é executado após a geração dos dados
- **THEN** ele apresenta a distribuição do target `Risk` (~70% good e ~30% bad), detalha as variáveis categóricas e numéricas e justifica o foco em métricas além da acurácia

#### Scenario: Levantamento de atributos sensíveis e potenciais vieses
- **WHEN** o leitor percorre a seção de governança do notebook
- **THEN** são apresentadas análises comparativas de taxa de inadimplência por gênero (`Sex`) e faixa de idade (`Age`), destacando riscos de viés algorítmico e conformidade com LGPD

#### Scenario: Visualização gráfica das distribuições com drift
- **WHEN** os conjuntos de referência e produção estão gerados
- **THEN** o notebook plota gráficos de densidade e frequência comparando as distribuições de `Age`, `Credit amount` e `Checking account` entre o ambiente de referência e produção

