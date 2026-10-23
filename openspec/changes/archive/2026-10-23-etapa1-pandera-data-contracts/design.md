## Context

Ver `proposal.md` para motivação.
O projeto utiliza o dataset German Credit (UCI id=144) com 10 atributos (3 numéricos, 6 categóricos e 1 target binário). A Etapa 1 do desafio exige o estabelecimento de contratos de dados formais via Pandera e a demonstração empírica de bloqueio de ingestão quando um lote defeituoso for submetido.

## Goals / Non-Goals

**Goals:**
- Implementar o esquema formal com Pandera (`DataFrameSchema`) cobrindo tipos, limites e domínios de todas as colunas.
- Criar a barreira de validação com verificação preguiçosa (`lazy=True`), acumulando todas as não-conformidades em um relatório estruturado de exceção (`DataContractViolationError`).
- Implementar um gerador de lote com erros propositais (menor de idade, crédito negativo, categoria desconhecida, valor nulo onde proibido).
- Criar script operante da Etapa 1 demonstrando a aprovação do dataset limpo e o bloqueio com log explicativo do lote com anomalias.
- Prover cobertura abrangente de testes unitários.

**Non-Goals:**
- Alterar o pipeline de modelagem (`baseline.py`) ou a simulação de drift da Etapa 2.
- Adicionar dependências externas além do Pandera (já listado no `pyproject.toml`).
- Tratar observabilidade contínua com MLflow (escopo da Etapa 3).

## Decisions

### 1. `DataFrameSchema` com validação preguiçosa (`lazy=True`)
- **Decisão:** Instanciar o contrato com `lazy=True` no método `schema.validate(df, lazy=True)`.
- **Justificativa:** Se houver múltiplos erros simultâneos (ex.: idade negativa e categoria inexistente), o validador expõe todos os defeitos em uma única checagem (`failure_cases`), facilitando a auditoria e correção pela equipe de dados.
- **Alternativa considerada:** Falhar no primeiro erro (`lazy=False`). Descartada por fornecer feedback parcial ao operador do pipeline.

### 2. Regras rígidas de domínio de crédito
- **Decisão:** Configurar checagens estritas:
  - `Age`: `>= 18` e `<= 120`, sem valores nulos.
  - `Credit amount`: `> 0`, sem valores nulos.
  - `Duration`: `> 0`, sem valores nulos.
  - `Sex`: apenas `['male', 'female']`.
  - `Job`: apenas `[0, 1, 2, 3]`.
  - `Housing`: apenas `['own', 'rent', 'free']`.
  - `Saving accounts` e `Checking account`: apenas categorias oficiais ou `'no_account'`.
  - `Risk`: apenas `['good', 'bad']`.
- **Justificativa:** Regras aderentes ao negócio bancário e às boas práticas obrigatórias do enunciado (idade mínima legal, ausência de nulos em dados críticos e limites financeiros válidos).

### 3. Script executável da Etapa 1 (`src/credit/run_etapa1.py`)
- **Decisão:** Fornecer um script dedicado `run_etapa1.py` que executa:
  1. Validação com sucesso do dataset de referência;
  2. Submissão de um lote corrompido com interceptação comprovada via `try/except` e log de bloqueio;
  3. Verificação de treino do modelo baseline.
- **Justificativa:** Atende ao entregável formal do PDF ("Script de validação de dados operante e modelo baseline treinado") e serve como roteiro direto para o vídeo demonstrativo de 5 minutos.

## Risks / Trade-offs

- **[Compatibilidade de dtypes com Pandas 3]** → O Pandera 0.34 e Pandas 3 tratam inteiros de forma estrita. Utilizaremos checagens numéricas flexíveis (`pa.Int` ou coerção numérica) para evitar falsos positivos de tipos equivalentes (`int64` vs `int32`).
- **[Interceptação sem quebrar a execução geral do orquestrador]** → A barreira de validação levanta uma exceção específica (`DataContractViolationError`), permitindo que orquestradores tratem e registrem o bloqueio preventivo de dados ruins sem crash silencioso.

