## Why

O Tech Challenge pede código, documentação e um vídeo da API, mas a banca de Machine Learning também espera ver exploração da série e o raciocínio do modelo. Hoje o treino e a API existem, e não há um artefato narrativo com gráficos (EDA, split temporal, LSTM vs naive) que o grupo possa usar na apresentação.

## What Changes

- Criar a pasta `notebooks/` com dois Jupyter notebooks acadêmicos: exploração da série PETR4.SA e walkthrough de treino/avaliação.
- Os notebooks reutilizam `src/` e os artefatos já gravados (`data/raw.parquet`, `models/metrics.json`); não substituem `python -m src.model.train` nem a API.
- Documentar no README como abrir e executar os notebooks e qual o papel de cada um na entrega.

## Capabilities

### New Capabilities

- `academic-notebooks`: notebooks Jupyter de exploração e de treino/avaliação para a entrega acadêmica, sem duplicar o pipeline de produção.

### Modified Capabilities

- Nenhuma. O comportamento da coleta, do LSTM, da API e do Docker permanece o mesmo.

## Impact

- Novos arquivos em `notebooks/` e uma seção no README.
- Dependências de notebook (Jupyter, matplotlib) no ambiente de desenvolvimento; a imagem Docker da API não precisa delas.
- Sem mudança de contrato HTTP, modelo persistido ou script de treino.
