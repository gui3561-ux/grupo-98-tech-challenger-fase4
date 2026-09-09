## Context

See `proposal.md` (Why). A API Hobby já responde em `https://grupo-98-tech-challenger-fase4.onrender.com` (health, ready, predict ~40.9999, docs). O README ainda pede para colar a URL. O `render.yaml` não declara `plan`. O CLI `render` v2.20.0 está instalado, mas `render whoami` retorna unauthorized. O serviço no dashboard é `srv-dagm0e942hec73cu54t0`. RSS observado ~700 MB com TensorFlow; Starter/Free têm 512 MB — a instância está viva hoje, mas OOM é risco. Workspace Hobby ≠ compute Standard.

## Goals / Non-Goals

**Goals:**

- README com a URL real e o recorte Hobby (sleep + fallback local).
- Inspeção CLI autenticada antes de qualquer mudança de `plan`/env.
- Qualquer ajuste operacional cabe em `free` ou `starter` / `0.5c-512mb`.

**Non-Goals:**

- Gravar o vídeo.
- Upgrade para `1c-2g` (Standard) ou maior.
- Retreinar o LSTM ou mudar `/predict`.
- Inventar hostname (`petr4-lstm-api.onrender.com` deu timeout; não usar).

## Decisions

- **URL canônica** = hostname do repositório GitHub, já verificado com curl. Alternativa: o `name` do Blueprint (`petr4-lstm-api`); não resolve publicamente.
- **Hobby** = workspace/compute atual; pin no `render.yaml` só depois de `render services --output json` (ou equivalente) mostrar o `plan` real. Alternativa: escrever `plan: starter` no escuro; pode rebaixar ou divergir do painel.
- **CLI** = `render login` (passo humano) e depois comandos não interativos de inspeção. Ajustes permitidos: health path, variáveis de runtime leves (threads TF) se a inspeção mostrar restart/OOM. Alternativa: só README; não cobre OOM se ele existir.
- **Sem upgrade de RAM** mesmo com RSS ~700 MB. Alternativa: Standard 2 GB; o usuário vetou. Linux overcommit + serviço Live justificam não mexer no modelo.
- **Vídeo** permanece “depois”, agora podendo usar a URL pública ou o Docker local.

## Risks / Trade-offs

- [CLI sem login] → o apply pede autenticação humana; sem ela, só README, sem pin de `plan`.
- [Hobby dorme] → README + `curl /health` antes da banca; fallback `docker compose`.
- [OOM em 512 MB] → não subir plano; só env/threads se logs mostrarem kill. Se persistir, a demo oficial volta a ser local.
- [Blueprint `plan` errado] → não adicionar `plan` até a inspeção confirmar o valor Hobby.

## Migration Plan

Editar README (e `render.yaml` só se o CLI confirmar). Push para `main` dispara redeploy; health `/health` não muda. Rollback: revert do commit. Sem mudança de contrato HTTP.

## Open Questions

Nenhuma que altere spec ou tarefas: o `plan` exato (`free` vs `starter`) só é lido no apply, depois do login.
