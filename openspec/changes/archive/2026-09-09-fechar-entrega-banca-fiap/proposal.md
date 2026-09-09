## Why

A revisão contra o Tech Challenge da Fase 4 mostrou que o pipeline (dados, LSTM, API, Docker, README) já existe, mas a banca ainda não vê identidade completa do grupo, o item de hiperparâmetros, a defesa do LSTM frente à naive, nem um caminho concreto de nuvem no Render. O vídeo fica a cargo de um integrante depois e não entra nesta change.

## What Changes

- Listar no README os integrantes do Grupo 98 (RM e nome), a partir do `LICENSE`.
- Preparar o serviço para Render: a API passa a escutar a porta da plataforma; o README descreve o deploy Docker e só publica URL pública quando ela existir (sem inventar link).
- Documentar o ajuste de hiperparâmetros (unidades, dropout, early stopping) no notebook de avaliação e no README, sem transformar o notebook no treino oficial.
- Explicitar no README e no notebook por que o LSTM perde da naive em preço absoluto e por que o artefato mesmo assim é o da entrega (sem retreinar só para “ganhar” da baseline).
- Atualizar a tabela de entregáveis: vídeo gravado posteriormente por um integrante; nuvem = Render (URL quando houver).

## Capabilities

### New Capabilities

- Nenhuma.

### Modified Capabilities

- `academic-notebooks`: identidade com integrantes; hiperparâmetros visíveis; discussão LSTM vs naive; entregáveis (vídeo depois, Render).
- `production-ops`: API utilizável em nuvem Docker (porta da plataforma) e documentação do deploy no Render.
- `lstm-forecast`: o recorte de hiperparâmetros escolhidos fica observável na entrega acadêmica (sem mudar a arquitetura persistida).

## Impact

- `README.md`, `notebooks/02_treino_e_avaliacao.ipynb`, `Dockerfile` (e possivelmente `render.yaml`).
- Sem retreino obrigatório; `models/` permanece o artefato atual.
- Sem gravação de vídeo e sem login na conta Render nesta change: o integrante sobe o serviço e cola a URL no README depois.
- O `LICENSE` já traz os RMs; a identidade acadêmica visível à banca vai no README.
