## Why

A Etapa 1 do Tech Challenge (Fase 4) possui peso de 25% na avaliação e exige a criação de contratos de qualidade de dados (Data Contracts) com a biblioteca Pandera ou Great Expectations para garantir que dados inconsistentes não ingressem no modelo ("lixo não entra no modelo"). Além disso, o enunciado exige explicitamente a demonstração de um lote de dados com erros forçando a falha do contrato e o consequente bloqueio da ingestão. Atualmente, o pipeline realiza apenas preenchimentos básicos via pandas, sem um contrato formal de esquema nem barreira de interceptação de dados corrompidos.

## What Changes

- Criação do módulo de contratos de dados em `src/credit/data/contracts.py` com Pandera (`DataFrameSchema`), estabelecendo regras rígidas de tipagem, intervalos válidos (`Age >= 18`, `Credit amount > 0`, `Duration > 0`), domínios categóricos estritos e veto a nulos em atributos obrigatórios.
- Implementação de mecanismo de barreira de ingestão (`validate_credit_data`) que inspeciona dataframes e bloqueia a passagem levantando exceções estruturadas (`DataContractViolationError`) com o sumário das violações.
- Criação de gerador de lote corrompido e script de demonstração (`src/credit/data/corrupted_batch.py` ou runner de validação) para comprovar publicamente a interceptação de dados ruins.
- Integração da validação por contrato no fluxo de split e pré-processamento de `src/credit/data/preprocess.py`.

## Capabilities

### New Capabilities
<!-- Nenhuma nova capacidade raiz criada; o comportamento expande a capacidade existente -->

### Modified Capabilities
- `credit-data-pipeline`: Adiciona os requisitos formais de validação estrita por contrato de dados com Pandera e interceptação ativa de lotes corrompidos com bloqueio de ingestão.

## Impact

- Garante conformidade técnica estrita com a Etapa 1 (25% da nota da Fase 4).
- Adiciona o módulo `src/credit/data/contracts.py` e testes automatizados dedicados em `tests/test_credit_contracts.py`.
- Bloqueia a execução do treinamento ou particionamento se o dataset base violar o contrato de dados.

