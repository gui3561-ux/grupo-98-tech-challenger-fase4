## Context

O pipeline (`src/data`, `src/model.train`), os artefatos em `models/` e a API já existem. A motivação está em `proposal.md`. Os notebooks são camada de apresentação acadêmica, não um terceiro runtime.

Restrições: não duplicar yfinance/scaler/LSTM; a imagem Docker da API não deve passar a treinar nem a incluir Jupyter.

## Goals / Non-Goals

**Goals:**

- Dois notebooks com papéis distintos (EDA vs treino/avaliação).
- Importar funções de `src/` e ler cache/métricas já gerados.
- Deixar explícito no README que `python -m src.model.train` continua sendo o treino oficial.

**Non-Goals:**

- Substituir o script de treino ou o Swagger da API.
- Dashboard, Streamlit ou app web.
- Commitar outputs pesados de execução (gráficos inline no `.ipynb` só o necessário para a banca abrir sem rodar).
- Incluir Jupyter na imagem Docker.

## Decisions

### 1. Dois notebooks, não um só

Um arquivo único mistura EDA e modelagem e fica longo para o vídeo. Dois arquivos batem com a entrega: “olha os dados” e “olha o modelo”.

```
notebooks/01_exploracao_petr4.ipynb
notebooks/02_treino_e_avaliacao.ipynb
```

Alternativa considerada: um notebook só. Rejeitada para a banca conseguir pular direto para métricas.

### 2. Reutilizar `src/`, não copiar o pipeline

- `01` chama `collect_prices` / `clean_series` / `chronological_split` (cache em `data/raw.parquet` se já existir).
- `02` lê `models/metrics.json` e, se o modelo estiver em disco, gera o gráfico D+1 vs real no teste via as mesmas funções de janela/scaler. Não reimplementa MinMax nem LSTM.

Se `metrics.json` ou o modelo faltarem, o notebook `02` instrui a rodar `python -m src.model.train` em vez de treinar em silêncio como caminho oficial.

### 3. Jupyter + matplotlib no extra de desenvolvimento

`jupyter` e `matplotlib` entram em dependência opcional (`pip install -e ".[notebooks]"`), não nas deps usadas pelo `Dockerfile`. Alternativa: colocar no `dependencies` principal — inflaria a imagem sem benefício para a API.

### 4. Kernel a partir da raiz do repo

Os notebooks ajustam o path para importar `src` (raiz do projeto). Alternativa: instalar o pacote e não mexer em path; também válido, mas o ajuste de path funciona no venv já usado pelo grupo.

## Risks / Trade-offs

- [Notebooks desatualizados em relação ao modelo] → Mitigação: `02` lê `models/metrics.json` gerado pelo script; README manda treinar antes se o arquivo não existir.
- [Duplicar lógica de janela no notebook] → Mitigação: só importar `src.data` e `src.model`.
- [Imagem Docker ganhar Jupyter] → Mitigação: extra opcional, fora do `pip install .` do Dockerfile.

## Migration Plan

1. Adicionar extra `[notebooks]` e a pasta.
2. Escrever os dois notebooks e a seção no README.
3. Sem migração de API ou modelo; rollback é remover a pasta e o extra.

## Open Questions

Nenhuma. O recorte (dois notebooks, script de treino oficial) está fechado.
