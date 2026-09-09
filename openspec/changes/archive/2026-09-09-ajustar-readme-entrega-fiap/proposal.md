## Why

O README atual descreve o pipeline, mas não fecha o ciclo da banca: o `curl` de `/predict` não é JSON válido, o clone do GitHub não corresponde ao fluxo documentado (`models/` vem no git, `data/raw.parquet` não), e os entregáveis do PDF (identidade do grupo, ticker vs exemplo DIS, link de nuvem, vídeo, monitoramento) ficam implícitos. A entrega vale 90% da nota e o README é o primeiro artefato que o avaliador lê.

## What Changes

- Reescrever o README para um professor conseguir clonar, subir a API e chamar `/predict` sem adivinhar.
- Identificar **Grupo 98**, justificar **PETR4.SA** (empresa à escolha; DIS no PDF é só exemplo) e o horizonte **D+1**.
- Deixar explícito o que vem no clone: artefatos em `models/` versionados; cache `data/raw.parquet` fora do git; treino/notebooks baixam via yfinance se o cache não existir.
- Trocar o `curl` quebrado por uma chamada reproduzível (payload JSON válido de 60 fechamentos) e uma resposta de exemplo alinhada ao modelo atual.
- Documentar `/metrics` como evidência de monitoramento (latência, CPU, RSS) para o vídeo.
- Declarar o estado da nuvem: ainda sem URL pública; demo oficial via `docker compose` + `/docs`.
- Completar a estrutura do repositório e manter a honestidade da naive vs LSTM.

## Capabilities

### New Capabilities

- Nenhuma.

### Modified Capabilities

- `academic-notebooks`: a documentação acadêmica no README passa a cobrir identidade/recorte da entrega, fluxo pós-clone, chamada reproduzível de `/predict`, monitoramento visível e status dos entregáveis do PDF, além dos notebooks.

## Impact

- Arquivo principal: `README.md`.
- Possível arquivo de apoio `examples/predict_payload.json` (60 floats) para o `curl` copiar e colar.
- Sem mudança de API, modelo, Docker, notebooks ou métricas.
- Sem URL de produção inventada; sem nomes de integrantes (não estão no repositório).
