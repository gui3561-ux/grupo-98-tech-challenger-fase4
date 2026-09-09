## Context

See `proposal.md` (Why). A API já corre em Docker na porta 8000. O README já admite “sem URL pública”. O notebook 02 já mostra métricas LSTM vs naive, mas não hiperparâmetros nem a defesa explícita. Os RMs estão no `LICENSE`, não no README. O vídeo não é desta change.

## Goals / Non-Goals

**Goals:**

- README com integrantes e recorte honesto de vídeo/Render.
- Imagem pronta para a `PORT` do Render.
- Notebook 02 + README com hiperparâmetros e discussão da naive.

**Non-Goals:**

- Gravar o vídeo.
- Fazer login ou criar o serviço na conta Render.
- Retreinar o LSTM para superar a naive.
- Optuna ou busca automática no script de treino.
- Trocar o treino oficial pelo notebook.

## Decisions

- **Uma change só** (itens 2–5). Alternativa: três changes; o usuário pediu uma proposta com base em todas as informações.
- **`PORT` no CMD** (`uvicorn --port ${PORT:-8000}`) via shell form no Dockerfile, ou script de entrada. Alternativa: só documentar 8000 no painel Render; quebra se a plataforma injetar outra porta. Render injeta `PORT`.
- **`render.yaml` opcional** com `runtime: docker` e `healthCheckPath: /health`. Alternativa: só README; o yaml reduz clique errado no painel.
- **URL**: placeholder honesto até o integrante colar o `onrender.com`. Alternativa: inventar URL — proibido pela spec atual.
- **Hiperparâmetros em tabela** no notebook 02 (escolhido: 64/32, dropout 0.2, patience 5, batch 32, epochs máx. 40) vs duas alternativas (rede menor 32/16; dropout 0.4), critério = early stopping em `val_loss`, sem rodar três treinos completos nesta change. Alternativa: retreinar tudo; fora do prazo e contraria “não ganhar da naive à força”.
- **Naive**: texto no README (ligar previsão ~41 vs último close ~48) e parágrafo no notebook 02. Alternativa: mudar o alvo para retorno; muda o modelo e a API.
- **Nomes só no README** (tabela RM/nome). O `LICENSE` permanece o aviso de copyright já preenchido; não duplicar a lista em código.

## Risks / Trade-offs

- [Render free sleep] → README já prevê demo local + `/docs` para o vídeo.
- [CMD shell form no Docker] → um processo a mais; necessário para expandir `PORT`.
- [Tabela de hiperparâmetros sem reexecução] → a banca pode pedir evidência empírica; o texto deixa claro que a escolha está no artefato persistido e no early stopping, não numa grade recém-rodada.
- [URL vazia no dia da entrega] → o integrante precisa colar depois do deploy; a change só deixa o buraco explícito.

## Migration Plan

Aplicar no repo, `docker compose` local continua na 8000. Rollback: commit anterior. Deploy Render é passo humano após o apply.

## Open Questions

Nenhuma para o código. A URL pública só existe depois do integrante publicar no Render.
