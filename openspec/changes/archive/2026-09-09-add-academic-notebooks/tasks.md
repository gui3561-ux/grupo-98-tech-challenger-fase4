## 1. Ambiente

- [x] 1.1 Adicionar extra opcional `[notebooks]` em `pyproject.toml` com jupyter e matplotlib e verificar que `pip install -e ".[notebooks]"` conclui e que o `Dockerfile` continua instalando só `pip install .` (sem o extra)
- [x] 1.2 Criar `notebooks/` e verificar que `01_exploracao_petr4.ipynb` e `02_treino_e_avaliacao.ipynb` existem nesse diretório

## 2. Notebooks

- [x] 2.1 Implementar `01_exploracao_petr4.ipynb` importando `src.data` (coleta/cache, limpeza, split) e verificar que o notebook plota o Close no tempo e marca treino/validação/teste em ordem cronológica
- [x] 2.2 Implementar `02_treino_e_avaliacao.ipynb` lendo `models/metrics.json` e usando `src` para o gráfico D+1 vs real, e verificar que MAE/RMSE/MAPE do LSTM e da naive aparecem lado a lado e que o texto aponta `python -m src.model.train` como treino oficial

## 3. Documentação

- [x] 3.1 Incluir no README a pasta `notebooks/`, o papel de cada arquivo, `pip install -e ".[notebooks]"` e que isso não entra no Docker, e verificar que um leitor reproduz o fluxo acadêmico só com o README
