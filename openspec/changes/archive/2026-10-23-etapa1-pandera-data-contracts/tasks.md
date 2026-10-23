## 1. Contrato Pandera e Barreira de Ingestão

- [x] 1.1 Implementar `src/credit/data/contracts.py` contendo o esquema estrito `CreditDataContract` com Pandera (`DataFrameSchema`) e a exceção customizada `DataContractViolationError`
- [x] 1.2 Implementar a função de barreira `validate_credit_data(df, lazy=True)` em `contracts.py` formatando detalhadamente as violações
- [x] 1.3 Implementar `build_corrupted_batch()` em `contracts.py` gerando um lote de teste com erros propositais (idade < 18, montante <= 0, nulos proibidos e categoria desconhecida)

## 2. Integração e Script de Demonstração da Etapa 1

- [x] 2.1 Integrar a validação do contrato em `src/credit/data/preprocess.py` assegurando que dados brutos passem pelo contrato antes do particionamento
- [x] 2.2 Criar o script operante `src/credit/run_etapa1.py` demonstrando a validação do dataset de referência, a interceptação do lote corrompido com logs e o treino/validação do baseline

## 3. Testes Automatizados e Execução Comprovada

- [x] 3.1 Implementar testes unitários em `tests/test_credit_contracts.py` cobrindo aprovação de dados válidos, bloqueio por idade, valores financeiros e categorias inválidas
- [x] 3.2 Executar `uv run pytest tests/test_credit_contracts.py` e a suíte completa de testes `uv run pytest tests/` confirmando 100% de aprovação
- [x] 3.3 Executar `uv run python -m src.credit.run_etapa1` para comprovar em terminal a interceptação e o bloqueio do lote anômalo

